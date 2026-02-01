# Tsigkros CRM for NYC

A lightweight CRM built with Flask. This project was created by Tsigkros Nikolaos for the New York College course \"Web Design and Programming\" (University of Greater Manchester). It combines server-rendered HTML pages with JSON/API endpoints, uses SQLAlchemy for data storage (SQLite by default), and supports role-based access with secure password hashing.

![Preview](/assets//preview.png)

## Tech Stack

- **Python 3 + Flask**: Web framework and routing
- **Jinja2 templates**: Server-rendered HTML
- **SQLAlchemy**: ORM for database access
- **SQLite**: Default local database (configurable)
- **Flask-Login**: Session and authentication handling
- **Werkzeug security**: Password hashing
- **Vanilla CSS + JS**: Styling and small frontend interactions

## Local Development

### Prerequisites

- Python 3.11+ (3.12 recommended)

### Setup

```sh
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### Run

```sh
python app.py
```

By default the app runs at http://127.0.0.1:5000

### Environment Variables (optional)

- `SECRET_KEY` (defaults to `dev-secret-key`)
- `DATABASE_URL` (defaults to `sqlite:///crm.db`)
- `CRM_ADMIN_USERNAME` (defaults to `admin`)
- `CRM_ADMIN_PASSWORD` (defaults to `admin123`)

## Project Structure

```
app/
  __init__.py        App factory, SQLAlchemy + LoginManager setup, DB init
  constants.py       Role and category constants
  routes.py          Frontend (HTML) routes and dashboards
  api.py             Backend (JSON/form) endpoints
  models.py          SQLAlchemy models
  utils.py           Shared helpers (e.g., role checks)
  templates/         Jinja2 templates (HTML pages)
  static/
    app.css          Vanilla CSS styling
    app.js           Small client-side behaviors
app.py               Entry point (create and run the app)
requirements.txt     Python dependencies
README.md            Project docs
```

### Layering Overview

- **Presentation layer**: Jinja templates in `app/templates/` and CSS/JS in `app/static/`
- **Web routes (FE)**: `app/routes.py` serves HTML pages and dashboards
- **API routes (BE)**: `app/api.py` handles form submissions and JSON endpoints
- **Domain/data layer**: `app/models.py` defines SQLAlchemy models and relationships
- **Shared utilities**: `app/utils.py` for auth and role-based helpers

## Authentication & Security

- Passwords are hashed using Werkzeug (`generate_password_hash` / `check_password_hash`).
- Sessions are managed by Flask-Login.
- Role-based access is enforced via `@login_required` and the `role_required` helper.

## Notes

- The first run will create the SQLite DB and seed an admin user using the `CRM_ADMIN_*` env vars.
- Use the Flask CLI instead of `app.py` if you want to override host/port easily:

```sh
flask --app app:create_app run --port 5001
```
