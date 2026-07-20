# GRC Implementation Lab

A hands-on lab that implements a Governance, Risk, and Compliance (GRC) plan as a
running web application — built with **Flask**, **Python**, **HTML/CSS**, and
containerized with **Docker**.

It turns the static GRC plan (Category / Sub-Category / GRC Item / Owner / Status /
Risk Level / etc.) into a working system with three simulated controls:

| Module | GRC control it demonstrates |
|---|---|
| **GRC Register** | Full CRUD register of Governance, Risk Management, and Compliance items — the plan itself, trackable and filterable. |
| **Policies** | Policy Management control: publish a policy and track employee acknowledgment (with a live completion bar). |
| **Incidents** | Incident Response control: log an incident, triage its severity, and move it through Open → Investigating → Contained → Resolved. |
| **Dashboard** | Live rollup of items by Category, Status, and Risk Level, plus open High/Critical risk and open incident counts. |

## Run it

Requires Docker and Docker Compose.

```bash
docker compose up --build
```

Then open **http://localhost:5000** in your browser.

The app seeds itself with realistic mock data on first run (GRC items, policies,
and sample incidents) stored in a SQLite database in a named Docker volume
(`grc_data`), so your data persists across restarts.

To stop:

```bash
docker compose down
```

To wipe the seeded data and start fresh:

```bash
docker compose down -v
```

## Project structure

```
grc-lab/
├── docker-compose.yml     # one-command orchestration
├── Dockerfile             # Python 3.11-slim + Flask app image
├── requirements.txt       # Flask, Flask-SQLAlchemy, Werkzeug
├── app.py                 # Flask routes / application entry point
├── models.py               # SQLAlchemy models (GRCItem, Policy, Acknowledgment, Incident)
├── seed.py                # Mock data seeding
├── static/css/style.css   # Styling
├── templates/             # Jinja2 HTML templates
└── data/                  # SQLite database (mounted as a Docker volume)
```

## Tech stack

- **Python 3.11 / Flask** — application server and routing
- **Flask-SQLAlchemy / SQLite** — data model and persistence
- **HTML5 + Jinja2** — server-rendered templates
- **CSS3** — custom styling (no external frameworks required)
- **Docker / Docker Compose** — single-command reproducible environment

## Notes

This is a training/demo lab. Data is illustrative mock data, not a real
production GRC system — but the workflows (register tracking, policy
acknowledgment, incident triage) mirror how these controls operate in practice.
