# Deployment Guide: Executive Productivity Agent — AIONOS

This guide outlines multiple deployment options for taking the Executive Productivity Agent live.

---

## 🌟 Option 1: 1-Click Free Cloud Deployment on Render (Recommended)

Render offers a free tier for FastAPI/Python web services:

1. **Push your code to a GitHub repository**:
   ```bash
   git remote add origin https://github.com/<your-username>/executive-productivity-agent.git
   git branch -M main
   git push -u origin main
   ```
2. **Deploy on Render**:
   - Go to [dashboard.render.com](https://dashboard.render.com) and click **New + > Web Service**.
   - Connect your GitHub repository.
   - Configure the following settings:
     - **Name**: `aionos-executive-agent`
     - **Runtime**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn backend.main:app --host 0.0.0.0 --port $PORT`
     - **Environment Variable**: `PYTHON_VERSION=3.11.9`
3. Click **Deploy Web Service**.
4. Once deployed, Render will provide a live HTTPS URL (e.g. `https://aionos-executive-agent.onrender.com`) where the executive dashboard and API are accessible.

---

## 🚀 Option 2: Deploy with Railway

1. Go to [railway.app](https://railway.app) and click **New Project > Deploy from GitHub repo**.
2. Select your repository. Railway will automatically detect the `Procfile` and `requirements.txt`.
3. In project settings, click **Generate Domain**.
4. Your application will be live immediately.

---

## 🐳 Option 3: Deploy with Docker / Docker Compose

For deploying on any Linux VPS, AWS EC2, DigitalOcean Droplet, or local container runtime:

```bash
# Build and run the containerized service
docker-compose up --build -d
```

- Port `8000` will be exposed.
- Access the dashboard at `http://<your-server-ip>:8000`.

---

## 🌐 Option 4: Instant Public URL via Cloudflare Tunnel / ngrok

If you want an immediate temporary public HTTPS URL directly from your local machine:

### Using Cloudflared:
```bash
# In Terminal 1: Start the server
python run.py

# In Terminal 2: Expose via Cloudflare
cloudflared tunnel --url http://localhost:8000
```

### Using ngrok:
```bash
ngrok http 8000
```

---

## 📦 Verified Deployment Files in Repository

- [`render.yaml`](../render.yaml): Render Blueprint definition
- [`Procfile`](../Procfile): Standard cloud process definition
- [`Dockerfile`](../Dockerfile): Production container configuration
- [`docker-compose.yml`](../docker-compose.yml): Multi-container orchestration config
- [`requirements.txt`](../requirements.txt): Pinned dependencies
- [`run.py`](../run.py): Production ASGI server launcher with automatic port fallback
