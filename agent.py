import os
import sys
from dotenv import load_dotenv
from openai import OpenAI
from caspian_sdk import CommClient

load_dotenv()

CASPIAN_API_KEY = os.getenv("CASPIAN_API_KEY")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not CASPIAN_API_KEY:
    print("Error: CASPIAN_API_KEY is missing in your .env file. Run `uvx --from caspian-cli caspian init` to generate one.")
    sys.exit(1)

if not OPENROUTER_API_KEY:
    print("Error: OPENROUTER_API_KEY is missing in your .env file. Please add it to proceed.")
    sys.exit(1)

# Initialize OpenAI client pointed at OpenRouter
openai_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# Load the system prompt
with open("system_prompt.txt", "r", encoding="utf-8") as f:
    system_prompt = f.read()

# Define the Event Knowledge Base to inject into the template
event_kb = """
Event Name: [Your Event Name Here]
Date & Time: [Date and Time]
Location / Venue: [Venue details]
Schedule / Agenda: [Schedule]
Transit / Directions: [Transit details]
Contact / Organizers: [Organizer contact]
FAQ: [Any FAQs]
"""

system_prompt = system_prompt.replace("{{KNOWLEDGE_BASE}}", event_kb)

client = CommClient()

# Add Caspian's per-channel etiquette to the system prompt
system_prompt += "\n\n" + client.behavior_prompt()

# Store conversation history since OpenRouter doesn't manage state for us
chat_sessions = {}

@client.on_message
def handle(message):
    conv_id = message.conversation.id
    
    # Initialize chat history if we haven't seen this conversation
    if conv_id not in chat_sessions:
        chat_sessions[conv_id] = [
            {"role": "system", "content": system_prompt}
        ]
        
    chat_history = chat_sessions[conv_id]
    
    sender_name = (message.sender or {}).get("name", "User")
    print(f"<- [{message.provider}] {sender_name}: {message.text!r}")
    
    # Add user message to history
    user_text = f"[{sender_name}]: {message.text}"
    chat_history.append({"role": "user", "content": user_text})
    
    try:
        # You can use any model from OpenRouter here (e.g. meta-llama/llama-3-8b-instruct)
        response = openai_client.chat.completions.create(
            model="openai/gpt-4o-mini", 
            messages=chat_history,
        )
        
        text = response.choices[0].message.content
        
        # Add assistant response to history
        chat_history.append({"role": "assistant", "content": text})
        
        # Parse internal action tags
        if "[ACTION: SAVE_RSVP]" in text:
            print(f"--> [HOOK] Triggering SAVE_RSVP for {sender_name}")
            
        if "[ACTION: UPDATE_RSVP]" in text:
            print(f"--> [HOOK] Triggering UPDATE_RSVP for {sender_name}")
            
        if "[ACTION: ESCALATE]" in text:
            print(f"--> [HOOK] Triggering ESCALATE for {sender_name}")
            
        if "[ACTION: FLAG_URGENT]" in text:
            print(f"--> [HOOK] Triggering FLAG_URGENT for {sender_name}")
            
        print(f"-> Agent: {text!r}")
        message.reply(text)
        
    except Exception as e:
        print(f"Error processing message: {e}")
        message.reply("Sorry, I encountered an internal error. Please try again in a moment.")
        # Remove the user message from history if the request failed
        chat_history.pop()

if __name__ == "__main__":
    # -------------------------------------------------------------
    # Connect channels here. Uncomment and configure as needed:
    # -------------------------------------------------------------
    
    # email = client.connect_email(username="my-event-agent")
    # print(f"Agent email: {email['address']}")
    
    print("Agent is ready. Starting listener (Ctrl+C to stop)...")
    client.listen()
