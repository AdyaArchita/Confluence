import re
from caspian_sdk import blocks as b
from storage import update_user_state

# Flexible match for [ACTION: SAVE_RSVP], [ action : save_rsvp ], etc.
TAG_PATTERN = re.compile(r"\[\s*ACTION\s*:\s*([A-Za-z_]+)\s*\]", re.IGNORECASE)

def parse_and_execute_tags(response_text, user_id, user_name="Attendee"):
    tags = TAG_PATTERN.findall(response_text)
    tags = [t.upper() for t in tags]
    
    blocks = None
    
    if "SAVE_RSVP" in tags:
        print(f"--> [HOOK] Triggering SAVE_RSVP for {user_id}")
        update_user_state(user_id, rsvp_update={"status": "confirmed"})
        
        # Build digital ticket
        blocks = [
            b.card(
                title=f"🎟️ Official Pass - Confluence '26",
                subtitle=f"Attendee: {user_name}",
                text="Show this ticket at the registration desk on event day.",
                buttons=[
                    {"label": "Add to Calendar", "url": "https://example.com/calendar"},
                    {"label": "Get Directions", "url": "https://example.com/map"}
                ]
            )
        ]
        
    if "ESCALATE" in tags:
        print(f"--> [HOOK] Triggering ESCALATE for {user_id}")
        update_user_state(user_id, set_escalated=True)
        
    # Clean text by removing all matched tag patterns
    clean_text = TAG_PATTERN.sub("", response_text).strip()
    return clean_text, blocks
