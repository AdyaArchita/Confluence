import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
from caspian_sdk import CommClient
from storage import get_user_history, update_user_state
from actions import parse_and_execute_tags

load_dotenv(override=True)

# Setup Keys
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
CASPIAN_API_KEY = os.getenv("CASPIAN_API_KEY")

if not OPENROUTER_API_KEY:
    print("Error: OPENROUTER_API_KEY is missing in your .env file.")
    sys.exit(1)

# Initialize OpenRouter Client
llm_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
    default_headers={
        "HTTP-Referer": "https://github.com/trycaspian/caspian-sdk",
        "X-Title": "Confluence Event Coordinator"
    }
)

# Initialize Caspian Client
client = CommClient()

# Load Prompts
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    raw_prompt = f.read()

with open("knowledge_base.txt", "r", encoding="utf-8") as f:
    knowledge_base = f.read()

system_prompt = raw_prompt.replace("{{KNOWLEDGE_BASE}}", knowledge_base)
system_prompt += "\n\n" + client.behavior_prompt()

@client.on_message
def handle(message):
    user_id = (message.sender or {}).get("address", "unknown")
    user_name = (message.sender or {}).get("name", "User")
    channel = message.channel
    conv_id = message.conversation_id
    
    # Send typing indicator (moved to global listener)
    
    print(f"<- [{channel}] {user_name}: {message.text!r}")
    
    # 1. Update State & Get sliding window history (cap to 10 turns)
    update_user_state(
        user_id=user_id,
        name=user_name,
        channel=channel,
        conversation_id=conv_id,
        history_append={"role": "user", "content": message.text}
    )
    history = get_user_history(user_id, max_turns=10)
    
    # 2. Build full LLM prompt array
    messages = [{"role": "system", "content": system_prompt}] + history
    
    try:
        # 3. Call OpenRouter
        response = llm_client.chat.completions.create(
            model="google/gemini-2.5-flash", 
            messages=messages,
            max_tokens=2000,
        )
        raw_text = response.choices[0].message.content
        
        # 4. Parse & Execute Tags
        clean_text, blocks = parse_and_execute_tags(raw_text, user_id, user_name)
        
        # 5. Append Assistant Response to History
        update_user_state(user_id=user_id, history_append={"role": "assistant", "content": raw_text})
        
        print(f"-> Agent: {clean_text!r}")
        
        # 6. Reply to user
        if blocks:
            message.reply(text=clean_text, blocks=blocks)
        else:
            message.reply(text=clean_text)
            
    except Exception as e:
        print(f"Error calling LLM: {e}")
        message.reply("Sorry, I encountered an internal error. Please try again in a moment.")

if __name__ == "__main__":
    # Connect channels via env variables
    if os.getenv("TELEGRAM_BOT_TOKEN"):
        client.connect_telegram(bot_token=os.getenv("TELEGRAM_BOT_TOKEN"))
        print("Connected to Telegram")
        
    if os.getenv("DISCORD_TOKEN"):
        client.install_discord(bot_token=os.getenv("DISCORD_TOKEN"))
        print("Connected to Discord")
        
    # Email connects instantly and automatically
    email = client.connect_email(username="confluence-desk")
    print(f"Connected to Email: {email['address']}")
    
    print("Agent is ready. Starting listener (Ctrl+C to stop)...")
    client.listen(ack="Thinking...")
