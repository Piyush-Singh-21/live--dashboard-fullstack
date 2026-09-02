# Instant Mechanic Live Operations Dashboard

A full-stack operations workspace for monitoring vehicle-service bookings, mechanics, customers, and revenue. It pairs a responsive Next.js frontend with a Django API and relational database.

## Stack

- Frontend: Next.js 16, React 19, TypeScript, CSS, Recharts, Lucide icons
- Backend: Python 3, Django 6, JSON API
- Database: SQLite locally; change Django's `DATABASES` setting to PostgreSQL for deployment

## Architecture

`Next.js UI -> Django /api endpoints -> Django ORM -> SQLite/PostgreSQL`

The UI automatically refreshes every 15 seconds so operational changes appear without a full page reload.

## Local setup

1. Install backend packages: `python -m pip install -r backend/requirements.txt`
2. Prepare and seed data:

   ```powershell
   cd backend
   python manage.py makemigrations operations
   python manage.py migrate
   python manage.py seed_data
   python manage.py runserver
   ```

3. Start the frontend in another terminal:

   ```powershell
   cd frontend
   npm run dev
   ```

Visit `http://localhost:3000`.

## API

- `GET /api/dashboard/` - KPI cards and chart series
- `GET /api/bookings/?search=&status=&page=&page_size=` - paginated bookings
- `GET /api/bookings/:id/` - booking detail
- `GET /api/bookings/export/` - CSV export
- `GET /api/mechanics/`, `GET /api/customers/` - operations resources

Set `NEXT_PUBLIC_API_URL` when the backend is deployed. In production, provide a secure Django secret, allowed hosts, CORS origins, and database credentials through environment variables.

## Deployment

Deploy `frontend/` to Vercel and `backend/` to AWS with PostgreSQL. Add the Vercel address to Django CORS origins and set `NEXT_PUBLIC_API_URL` to the public API URL.

## AI usage

Codex assisted with the initial UI, API, seed fixture, tests, and documentation. Review and understand each part before submitting, especially the API/ORM relationships and deployment configuration.
