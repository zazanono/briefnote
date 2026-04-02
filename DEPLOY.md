# Deployment

## Development

```bash
# Terminal 1 — Backend
cd backend && source venv/bin/activate && uvicorn main:app --reload --port 8000

# Terminal 2 — Frontend
cd frontend && npm run dev
```

Open `http://localhost:5173`

## Production

### Build

```bash
cd frontend && npm run build
```

The built files go to `frontend/dist/`.

### Backend env vars

Create `backend/.env`:

```
OPENROUTER_API_KEY=your_openrouter_key
OPENROUTER_BASE_URL=https://openrouter.ai/api/v1
OPENROUTER_MODEL=qwen/qwen3.6-plus:free
```

### Run backend

```bash
cd backend && source venv/bin/activate
pip install -e .
uvicorn main:app --host 0.0.0.0 --port 8000
```

### Serve frontend

Serve `frontend/dist/` with any static file server. The frontend expects the backend at `/api`.

**nginx example:**

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    location / {
        root /path/to/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    location /api/ {
        proxy_pass http://localhost:8000;
    }
}
```

### CORS

The backend allows requests from `http://localhost:5173` (dev) and needs to be updated for production. Edit the `CORSMiddleware` in `backend/main.py` to add your production domain.

### OpenAI/OpenRouter

The backend makes requests to OpenRouter. Ensure the server has internet access. No API keys are needed on the frontend.
