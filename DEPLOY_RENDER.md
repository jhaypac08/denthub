# Deploying the Backend to Render (step-by-step)

This guide walks through deploying the Django backend to Render and configuring GitHub Actions to trigger an automatic deploy.

1) Prepare your GitHub repository
- Push the repository to GitHub (if not already).

2) Create a Render account and new Web Service
- Sign in to https://render.com and create a new Web Service.
- Connect your GitHub repo and pick the repository and branch (`main`).
- Choose "Python" as the environment.

Build Command:

```
pip install -r backend/requirements.txt
python backend/manage.py migrate --noinput
python backend/manage.py collectstatic --noinput
```

Start Command:

```
gunicorn denthub_project.wsgi --chdir backend --log-file -
```

Render will detect the `Procfile` if present. The `Procfile` included in this repo runs gunicorn with the correct working directory.

3) Configure environment variables on Render
Set these env vars in the Render service settings (Environment > Environment Variables):

- `SECRET_KEY` — a secure random string
- `DEBUG` — `False`
- `ALLOWED_HOSTS` — your domain(s), comma-separated (e.g. `example.com,api.example.com`)
- `DATABASE_URL` — e.g. `mysql://dbuser:dbpassword@host:3306/denthub_db` (or use Render Managed DB credentials)
- `CORS_ALLOW_ALL_ORIGINS` — `False` (or `True` for testing)
- `CORS_ALLOW_CREDENTIALS` — `True`
- `CSRF_TRUSTED_ORIGINS` — comma-separated origins (e.g. `https://your-frontend.com`)
- `SESSION_COOKIE_SECURE` / `CSRF_COOKIE_SECURE` — `True`

If you want Render to provision a managed database, create a Render PostgreSQL/MySQL service and provide its connection URL as `DATABASE_URL`.

4) (Optional) Use Managed Database
- Create a new Managed Database in Render and attach it to the Web Service. Update `DATABASE_URL` accordingly.

5) GitHub Actions automatic deploy (already added)
- This repo contains `.github/workflows/deploy-backend-render.yml` which triggers on pushes to `main`.
- It posts to Render's Deploy API; to allow the workflow to trigger a deploy, set these GitHub repository secrets:
  - `RENDER_API_KEY` — create a Render Account API Key (Personal > API Keys)
  - `RENDER_SERVICE_ID` — your Render Service ID (found in service settings or from the Render API)

To get `RENDER_SERVICE_ID` via API (replace `<api-key>`):

```bash
curl -H "Authorization: Bearer <api-key>" https://api.render.com/v1/services
```

Find the service `id` in the output JSON for your backend service.

6) Domain & HTTPS
- Add your custom domain in Render (Settings > Custom Domains). Render provides automatic HTTPS via Let's Encrypt.

7) Static & Media
- `collectstatic` will collect static files to `STATIC_ROOT` and WhiteNoise will serve them. For user-uploaded media consider configuring an external store (S3, DigitalOcean Spaces) and set `MEDIA_URL` accordingly.

8) Final checklist
- Set production secrets and DB URL on Render.
- Ensure `DEBUG=False` and `SECRET_KEY` is secure.
- Add `CSRF_TRUSTED_ORIGINS` with your frontend domain.
- Add GitHub secrets `RENDER_API_KEY` and `RENDER_SERVICE_ID` if you want automatic deploys on push.

9) Trigger a manual deploy
- After configuring, push to `main` or trigger the deploy from the Render dashboard.

10) Troubleshooting
- Check Render service logs for errors (Build / Start / Live Logs).
- Make sure migration ran and static files were collected.

---

Frontend recommendation: Vercel (easy, reliable)

- Recommended: Deploy the `frontend/` project to Vercel (or Netlify). Vercel provides a smooth Git integration, automatic builds on push, automatic HTTPS, and environment variable support. Set `VITE_API_BASE` or similar to the backend API URL.

Vercel quick steps:

1. Sign up at https://vercel.com and import the GitHub repo.
2. Select the `frontend/` project folder as the root.
3. Build command: `npm install && npm run build`
4. Output directory: `dist`
5. Set env var `VITE_API_BASE` to your API base (e.g. `https://api.your-domain.com`)

Vercel will auto-deploy on push. Netlify is a good alternative with similar ease-of-use.
