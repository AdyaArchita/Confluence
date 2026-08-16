from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from storage import load_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/stats")
def get_dashboard_stats():
    db = load_db()
    
    total_rsvps = len([u for u in db.values() if u.get("rsvp", {}).get("status", "").lower() == "confirmed"])
    escalations = [u for u in db.values() if u.get("escalated") == True]
    
    # Calculate T-shirt sizes
    tshirt_counts = {"S": 0, "M": 0, "L": 0, "XL": 0}
    for u in db.values():
        size = u.get("rsvp", {}).get("tshirt")
        if size in tshirt_counts:
            tshirt_counts[size] += 1
            
    # Calculate active channels
    channels = set()
    for u in db.values():
        if "channel" in u:
            channels.add(u["channel"])
            
    # Convert dict to array for frontend
    attendees_list = []
    for user_id, data in db.items():
        # exclude full history from API response to save bandwidth
        clean_data = {k: v for k, v in data.items() if k != "history"}
        clean_data["id"] = user_id
        attendees_list.append(clean_data)
        
    attendees_list.sort(key=lambda x: x.get("registered_at", ""), reverse=True)
    
    return {
        "total_rsvps": total_rsvps,
        "escalations_count": len(escalations),
        "tshirt_counts": tshirt_counts,
        "active_channels": list(channels),
        "attendees": attendees_list
    }
