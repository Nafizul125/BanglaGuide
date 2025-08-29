# BanglaGuide

## Development Environment

Recommended minimal Python dependencies (currently used in code):

```
Django==5.0.7
psycopg2-binary==2.9.10   # PostgreSQL driver
django-tailwind==4.2.0     # Tailwind CSS integration
asgiref==3.9.1             # Django runtime dep (installed automatically)
sqlparse==0.5.3            # Django runtime dep (installed automatically)
tzdata==2025.2             # Timezone data (auto on Windows)
```

Optional (only add when actually needed in code):
- Pillow (image handling if you add `ImageField` later)
- python-slugify (if you introduce slugs manually)
- requests / httpx (external API calls)
- django-environ (for .env based settings management)

The repository originally contained a committed `venv/` – remove it locally and rely on a fresh virtual environment that is excluded via `.gitignore`.

## Setup Steps

1. Create & activate virtual environment (PowerShell on Windows):
	```powershell
	py -3.11 -m venv .venv
	.\.venv\Scripts\Activate.ps1
	```
2. Install deps:
	```powershell
	pip install Django==5.0.7 psycopg2-binary django-tailwind
	pip freeze > requirements.txt
	```
3. PostgreSQL: Ensure a local DB named `BanglaGuide` exists and credentials in `banglaguide/settings.py` match your local setup.
4. Run migrations & create superuser:
	```powershell
	python manage.py migrate
	python manage.py createsuperuser --email admin@example.com
	```
5. (Tailwind) Install Node.js (ensure `npm` path matches `NPM_BIN_PATH` in settings) then initialize Tailwind app if not done:
	```powershell
	python manage.py tailwind init
	python manage.py tailwind install
	python manage.py tailwind build   # or: python manage.py tailwind dev
	```
6. Run server:
	```powershell
	python manage.py runserver
	```

## Environment Variables / Secrets
Replace the placeholder `SECRET_KEY` and `WEATHER_API_KEY` with secure values. Prefer using environment variables (e.g. via `django-environ`) instead of hard‑coding in `settings.py`.

## Next Improvements
- Externalize secrets using `.env`.
- Add tests for custom user model.
- Add Pillow & media handling once image uploads are introduced.

## Notes
If you change dependencies, re-run `pip freeze > requirements.txt` (or hand curate only top-level requirements for a leaner file).