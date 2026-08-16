import json
import os
import threading
import datetime

DB_FILE = "rsvps.json"
_lock = threading.Lock()

def load_db():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_db(data):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

def get_user_state(user_id):
    with _lock:
        db = load_db()
        if user_id not in db:
            db[user_id] = {
                "name": user_id,
                "history": [],
                "rsvp": {},
                "escalated": False,
                "registered_at": datetime.datetime.now().isoformat()
            }
            save_db(db)
        return db[user_id]

def update_user_state(user_id, history_append=None, rsvp_update=None, set_escalated=None, name=None, channel=None, conversation_id=None):
    with _lock:
        db = load_db()
        if user_id not in db:
            db[user_id] = {
                "name": name or user_id,
                "history": [],
                "rsvp": {},
                "escalated": False,
                "registered_at": datetime.datetime.now().isoformat()
            }
            
        user = db[user_id]
        
        if name:
            user["name"] = name
        if channel:
            user["channel"] = channel
        if conversation_id:
            user["last_conversation_id"] = conversation_id
            
        if history_append:
            user["history"].append(history_append)
            
        if rsvp_update is not None:
            user["rsvp"].update(rsvp_update)
            
        if set_escalated is not None:
            user["escalated"] = set_escalated
            
        db[user_id] = user
        save_db(db)

def get_user_history(user_id, max_turns=10):
    user_state = get_user_state(user_id)
    return user_state.get("history", [])[-max_turns:]
