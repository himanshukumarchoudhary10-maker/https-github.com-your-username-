# Phone Details Lookup

Simple Python script to lookup phone number details. Runs in demo mode if no API key is configured.

Prerequisites:
- Python 3.x
- Install dependencies: `pip install -r requirements.txt`

Usage:

```powershell
python phone_details.py --number "+15551234567"
```

To use a real API, set environment variables:

```powershell
$env:NUMBERLOOKUP_API_KEY = "your_api_key_here"
$env:NUMBERLOOKUP_API_URL = "https://api.example.com/lookup"
```

Twilio Lookup example:

1. Create a Twilio account and get your Account SID and Auth Token.
2. Set environment variables in PowerShell:

```powershell
$env:TWILIO_ACCOUNT_SID = "your_account_sid"
$env:TWILIO_AUTH_TOKEN = "your_auth_token"
```

3. Run the script (Twilio will be used automatically when credentials are present):

```powershell
python phone_details.py --number "+15551234567"
```

Notes:
- Without Twilio or another provider configured the script runs in demo mode.
- To use another provider set `NUMBERLOOKUP_API_KEY` and `NUMBERLOOKUP_API_URL`.
 
## Deployment via GitHub + Render

This repository includes a GitHub Actions workflow that can automatically trigger a deploy on Render when you push to `main`.

Steps to get a live URL using GitHub + Render:

1. Create a GitHub repository and push these files to it (`git init`, add, commit, push to `origin main`).
2. Create a Web Service on Render and connect it to your GitHub repository. Select "Web Service" and set the build command to `pip install -r requirements.txt` and start command to `gunicorn app:app --bind 0.0.0.0:$PORT` (or leave defaults if Render auto-detects).
3. In your GitHub repository, go to Settings → Secrets → Actions and add two secrets:
	- `RENDER_API_KEY` — your Render API key (Account → API Keys)
	- `RENDER_SERVICE_ID` — the Render service id (found in the Render dashboard URL for the service)
4. Push to `main`. The GitHub Actions workflow `.github/workflows/deploy.yml` will POST a deploy to Render which will build and start the service. Render provides a public URL for the service.

Notes:
- If you prefer, you can deploy the project to Replit or Railway — instructions differ slightly (I can add those if you prefer).
- I cannot push to your GitHub or create the Render service without your account/credentials, but once you follow the steps above the site will be live and accessible from any phone/browser.

Commands you can run locally to push:

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/<your-username>/<your-repo>.git
git push -u origin main
```

## Alternative: Deploy on Railway or Replit (no ngrok/authtoken needed)

These platforms provide a public URL after you deploy; follow the steps below. The app will run in demo mode unless you set Twilio or another provider's credentials in the service secrets.

Railway (recommended quick deploy):

1. Create a Railway account at https://railway.app and click "New Project" → "Deploy from GitHub".
2. Connect your GitHub repo and select this repository and the `main` branch.
3. Railway will detect Python. Set the start command to:

	`gunicorn app:app --bind 0.0.0.0:$PORT`

4. (Optional) In Railway project settings → Environment, add secrets if you want real lookups:
	- `TWILIO_ACCOUNT_SID` and `TWILIO_AUTH_TOKEN` (for Twilio), or
	- `NUMBERLOOKUP_API_KEY` and `NUMBERLOOKUP_API_URL` (for another provider).
5. Deploy — Railway will build and give you a public URL you can open on any phone/browser.

Replit (instant import + run):

1. Go to https://replit.com, create a new Repl and choose "Import from GitHub", then paste your repo URL.
2. In the Replit UI, open "Secrets (Environment Variables)" and add the same secrets as above if you want real lookups.
3. Set the run command to:

	`gunicorn app:app --bind 0.0.0.0:$PORT`

4. Click "Run" — Replit will provide a public URL to share.

Notes:
- The app runs in demo mode by default (no API keys), so you can make it public immediately and test the UI from your phone.
- To perform live lookups, set the Twilio or provider credentials in the platform's environment/secret settings.
- If you want, I can also add a small `Dockerfile` so services that prefer Docker can deploy easily.

## Docker (build and run locally)

You can build and run the app locally in a container.

Build the image:

```bash
docker build -t phone-lookup:latest .
```

Run the container (maps port 5000):

```bash
docker run -p 5000:5000 --env PORT=5000 --name phone-lookup phone-lookup:latest
```

Open http://localhost:5000 on your phone (if your machine is reachable) or adapt port forwarding.

Push image to Docker Hub (example):

```bash
docker tag phone-lookup:latest <your-dockerhub-username>/phone-lookup:latest
docker push <your-dockerhub-username>/phone-lookup:latest
```

You can then deploy this image to any container hosting provider (AWS ECS, DigitalOcean App Platform, Railway with container, etc.).



