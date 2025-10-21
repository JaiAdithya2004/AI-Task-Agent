# Autonomous AI Agent - Deployment Guide

## 🚀 Docker Deployment

### Local Docker Build & Run

```bash
# Build the Docker image
docker build -t autonomous-ai-agent .

# Run the container locally
docker run -p 8501:8501 \
  -e GEMINI_API_KEY="your-api-key-here" \
  autonomous-ai-agent
```

### Test locally
```bash
# Access the app
open http://localhost:8501
```

## 🌐 Render Deployment

### Prerequisites
1. GitHub repository with your code
2. Render account (free tier available)
3. Gemini API key

### Deployment Steps

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Add Docker deployment configuration"
   git push origin main
   ```

2. **Connect to Render**
   - Go to [render.com](https://render.com)
   - Sign up/Login with GitHub
   - Click "New +" → "Web Service"
   - Connect your GitHub repository

3. **Configure Service**
   - **Name**: `autonomous-ai-agent`
   - **Environment**: `Docker`
   - **Branch**: `main`
   - **Dockerfile Path**: `./Dockerfile`
   - **Plan**: `Starter` (free)

4. **Set Environment Variables**
   ```
   GEMINI_API_KEY = your-gemini-api-key-here
   GEMINI_MODEL = gemini-2.0-flash
   GEMINI_TEMPERATURE = 0.7
   GEMINI_MAX_TOKENS = 1000
   LOG_LEVEL = INFO
   ```

5. **Deploy**
   - Click "Create Web Service"
   - Wait for build to complete (~5-10 minutes)
   - Your app will be available at: `https://your-app-name.onrender.com`

## 📁 Production File Structure

```
AI-Agent/
│
├── Dockerfile              # Docker configuration
├── .dockerignore           # Docker ignore file
├── render.yaml             # Render deployment config
├── requirements-prod.txt   # Production dependencies
├── config.py               # Environment-based config
├── web_ui.py               # Main Streamlit app
├── run_ui.py               # Launcher script
│
├── agents/                 # Agent implementation
│   ├── __init__.py
│   └── gemini_agent.py
│
└── utils/                  # Utilities
    ├── __init__.py
    └── logger.py
```

## 🔧 Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `GEMINI_API_KEY` | Google Gemini API key | Required |
| `GEMINI_MODEL` | Gemini model to use | `gemini-2.0-flash` |
| `GEMINI_TEMPERATURE` | Model temperature | `0.7` |
| `GEMINI_MAX_TOKENS` | Max response tokens | `1000` |
| `LOG_LEVEL` | Logging level | `INFO` |

## 🎯 Production Features

- ✅ **Dockerized**: Containerized for consistent deployment
- ✅ **Environment-based**: Secure configuration management
- ✅ **Health Checks**: Built-in health monitoring
- ✅ **Optimized**: Minimal dependencies for faster builds
- ✅ **Scalable**: Ready for horizontal scaling
- ✅ **Secure**: API keys via environment variables

## 🚨 Important Notes

1. **API Key Security**: Never commit API keys to Git
2. **Free Tier Limits**: Render free tier has sleep after inactivity
3. **Build Time**: First build may take 5-10 minutes
4. **Cold Starts**: Free tier may have cold start delays

## 🔍 Troubleshooting

### Build Issues
```bash
# Check Docker build locally
docker build -t test-agent .

# Check logs
docker logs <container-id>
```

### Runtime Issues
- Check Render logs in dashboard
- Verify environment variables are set
- Ensure API key is valid

### Performance
- Upgrade to paid plan for better performance
- Consider caching for frequent requests
- Monitor resource usage in Render dashboard

---

**Ready for production deployment! 🚀**
