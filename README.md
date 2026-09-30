# Confluence Event Coordinator

An AI-powered, multi-channel event coordinator for "Confluence '26". This project features a smart agent that handles attendee RSVPs, answers questions, and smartly escalates issues across Telegram, Discord, and Email. It also includes a Next.js dashboard to monitor registrations and escalations in real-time.

## Overview
Managing attendees across different platforms can be chaotic. This project solves that by centralizing communication through an AI agent that speaks on multiple channels, strictly follows an event knowledge base, and logs registrations to a unified JSON database. The companion dashboard provides organizers with a clean UI to track RSVP stats and handle manual escalations.

## Live Demo / Screenshots
<!-- TODO: Add a link to a live demo if available -->
<!-- TODO: Add a screenshot of the Next.js dashboard here -->
> **[TODO: Insert Dashboard Screenshot]**

## Key Features
- **Multi-Channel AI Agent**: Operates concurrently on Telegram, Discord, and Email using the Caspian SDK.
- **Automated RSVP Flow**: The agent walks users through registration and automatically issues a digital ticket using `[ACTION: SAVE_RSVP]`.
- **Smart Escalations**: If the agent cannot answer a question based on its knowledge base, it triggers `[ACTION: ESCALATE]` to flag the user for human review on the dashboard.
- **Knowledge-Base Driven**: Agent responses are grounded in a configurable `knowledge_base.txt` to prevent hallucinating incorrect event details.
- **Real-Time Dashboard**: A Next.js web UI that displays total RSVPs, T-shirt size distribution, active channels, and highlights users needing manual intervention.
- **Broadcast System**: A command-line script to instantly message all confirmed attendees across all platforms.

## Tech Stack
### Backend
- **Python 3**
- **FastAPI & Uvicorn**: Serves the REST API for the dashboard.
- **OpenAI SDK / OpenRouter**: Connects to the LLM (`google/gemini-2.5-flash`).
- **Caspian SDK**: Handles multi-channel messaging (Telegram, Discord, Email).
- **JSON Storage**: Thread-safe file-based data persistence (`rsvps.json`).

### Frontend (`dashboard/`)
- **Next.js 16 (App Router)**
- **React 19**
- **Tailwind CSS v4**
- **Lucide React & shadcn/ui**: For icons and UI components.

## Project Structure
```text
.
├── actions.py           # Parses LLM output to execute backend triggers (SAVE_RSVP, ESCALATE)
├── agent.py             # Main AI agent listener; handles state, prompt construction, and messaging
├── api.py               # FastAPI backend serving '/api/stats' to the frontend
├── broadcast.py         # CLI tool to send announcements to all confirmed attendees
├── storage.py           # Thread-safe JSON database implementation for user states
├── system_prompt.txt    # Base instructions and behavior rules for the LLM
├── knowledge_base.txt   # Ground-truth event details (venue, schedule, etc.)
├── rsvps.json           # The database (generated at runtime)
├── .env.example         # Template for required environment variables
├── requirements.txt     # Python dependencies
└── dashboard/           # Next.js frontend application
    ├── src/app/         # Next.js routes and pages (page.tsx, layout.tsx)
    ├── package.json     # Node.js dependencies and scripts
    └── ...
```

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js (npm, yarn, or pnpm)
- API Keys for OpenRouter and Caspian

### Environment Variables
Create a `.env` file in the root directory by copying `.env.example`:
```bash
cp .env.example .env
```

| Variable | Description |
|---|---|
| `OPENROUTER_API_KEY` | **Required.** Your OpenRouter API key for LLM access. |
| `CASPIAN_API_KEY` | **Required.** Your Caspian SDK key for messaging routing. |
| `TELEGRAM_BOT_TOKEN` | *Optional.* Token from BotFather to enable Telegram. |
| `DISCORD_TOKEN` | *Optional.* Discord bot token to enable Discord. |

*(Note: Email channel connects automatically via `confluence-desk` username in `agent.py`)*

### Installation & Running

**1. Start the Backend API (for Dashboard)**
```bash
pip install -r requirements.txt
uvicorn api:app --reload --port 8000
```
*The API will be available at `http://127.0.0.1:8000/api/stats`*

**2. Start the AI Agent Listener**
Open a new terminal and run:
```bash
python agent.py
```
*The agent will connect to configured channels and start listening.*

**3. Start the Dashboard (Frontend)**
Open a new terminal and run:
```bash
cd dashboard
npm install
npm run dev
```
*The dashboard will be available at `http://localhost:3000`*

## Available Commands / Scripts

**Broadcast an Announcement**
To send a message to all *confirmed* attendees across all active channels:
```bash
python broadcast.py "Your announcement message here"
```

**Frontend Scripts (in `/dashboard`)**
- `npm run dev`: Starts the Next.js development server.
- `npm run build`: Builds the Next.js app for production.
- `npm run start`: Runs the built Next.js production server.
- `npm run lint`: Runs ESLint.

## Customization
- **Event Details:** Edit `knowledge_base.txt` to update the venue, dates, FAQ, or contact info. The agent will adapt immediately on its next reply.
- **Agent Behavior:** Edit `system_prompt.txt` to change the agent's persona or add new rules.
- **New Actions:** Add new tag parsing logic to `actions.py` if you want the LLM to trigger new backend processes.

## Testing
There is no automated test suite included in the repository at this time. 

## Deployment
- **Backend/Agent:** Deploy to any Python host (e.g., Render, Railway, DigitalOcean). Run the API via `uvicorn api:app --host 0.0.0.0 --port 8000` and keep `python agent.py` running as a background worker.
- **Frontend:** The `dashboard` is a standard Next.js app, easily deployable to [Vercel](https://vercel.com).

## Roadmap / Known Limitations
- Data is currently stored in a local `rsvps.json` file, which is fine for small scale but lacks horizontal scalability.
- No authentication on the Next.js dashboard; it currently assumes a secure or local environment.
- Attendees' full history is excluded from the `/api/stats` endpoint to save bandwidth, meaning chat history isn't viewable in the dashboard yet.

---

## Contributing
<!-- TODO: Add contribution guidelines if applicable -->

## License
<!-- TODO: Add License information (e.g., MIT, Apache 2.0) -->

## Author / Contact
<!-- TODO: Add Author name, GitHub link, and contact info -->
