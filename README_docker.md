# Docker Guide for LuminaryDeutsch

## Prerequisites
- Docker installed on your system
- Docker Compose (For linux I use V2)

## Environment Configurations

This project includes two Docker Compose configurations:

### 🛠️ Development (`docker-compose-dev.yml`)
- **Live code reloading** - Changes to source files are reflected immediately
- Volume mounts for `src/`, `main.py`, and `requirements.txt`
- File watcher enabled for automatic Streamlit reloads
- Interactive terminal support

### 🚀 Production (`docker-compose-prod.yml`)
- **No volume mounts** - Code is baked into the image
- Resource limits (2 CPU cores, 2GB RAM max)
- Health checks enabled
- Always restart policy
- Usage statistics disabled

---

## Development Workflow

### First Time Setup
Build and start the development environment:
```bash
docker compose -f docker-compose-dev.yml up --build
```

### Subsequent Runs
```bash
docker compose -f docker-compose-dev.yml up
```

### Running in Background
```bash
docker compose -f docker-compose-dev.yml up -d
```

### View Logs
```bash
docker compose -f docker-compose-dev.yml logs -f
```

### Stop Development Container
```bash
docker compose -f docker-compose-dev.yml down
```

---

## Production Deployment

### First Time Setup
Build and start the production environment:
```bash
docker compose -f docker-compose-prod.yml up --build -d
```

### Subsequent Runs
```bash
docker compose -f docker-compose-prod.yml up -d
```

### View Logs
```bash
docker compose -f docker-compose-prod.yml logs -f
```

### Stop Production Container
```bash
docker compose -f docker-compose-prod.yml down
```

### Restart Production Container
```bash
docker compose -f docker-compose-prod.yml restart
```

---

## Accessing the Application

Once running, open your browser and navigate to:
- **Local**: http://localhost:8501
- **Network**: http://YOUR_IP:8501

---

## Rebuilding After Changes

### Development
Changes to files in `src/` and `main.py` are automatically reflected (no rebuild needed).

If you modify `requirements.txt` or `Dockerfile`:
```bash
docker compose -f docker-compose-dev.yml up --build
```

### Production
Any code changes require a rebuild:
```bash
docker compose -f docker-compose-prod.yml up --build -d
```

---

## Troubleshooting

### Port Already in Use
If port 8501 is already in use, edit `docker-compose.yml` and change:
```yaml
ports:
  - "8502:8501"  # Use 8502 instead
```

### Docker Authentication Issues
If you encounter Docker Hub authentication errors:
```bash
docker logout
docker compose up --build
```

### View Container Status
```bash
docker compose ps
```

### Execute Commands in Container
```bash
docker compose exec luminary-deutsch bash
```
*I use this for debugging and checking if files were copied correctly*

## Development Mode

The `docker-compose.yml` includes a volume mount for live code reloading during development. Changes to files in `./src` will be reflected immediately.
