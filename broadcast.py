import os
import sys
from dotenv import load_dotenv
from caspian_sdk import CommClient
from storage import load_db

load_dotenv()
caspian = CommClient()

def send_announcement(announcement_text):
    db = load_db()
    sent_count = 0
    for user_id, user_data in db.items():
        if user_data.get("rsvp", {}).get("status", "").lower() == "confirmed":
            conversation_id = user_data.get("last_conversation_id")
            if conversation_id:
                try:
                    caspian.send_message(
                        conversation_id=conversation_id, 
                        text=f"📢 **Event Update**: {announcement_text}"
                    )
                    sent_count += 1
                    print(f"Sent to {user_data.get('name', user_id)}")
                except Exception as e:
                    print(f"Failed to send to {user_id}: {e}")
                    
    print(f"Broadcast complete. Sent {sent_count} messages.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python broadcast.py 'Your announcement message'")
        sys.exit(1)
        
    announcement = " ".join(sys.argv[1:])
    send_announcement(announcement)
