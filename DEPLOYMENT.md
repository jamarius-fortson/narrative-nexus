# Deployment Guide

# 🚀 Deploying NarrativeNexus
### *Production Deployment Guide for Enterprise Agent Orchestration*

## 🚀 Quick Deploy Options

### 1. Streamlit Community Cloud (Easiest)

**Best for**: Quick demos, personal projects, portfolio showcases

1. **Push to GitHub** (already done!)
2. **Visit** [share.streamlit.io](https://share.streamlit.io)
3. **Sign in** with your GitHub account
4. **Click** "New app"
5. **Select** your repository: `nadir-sheikh09/Content-Generation-Pipeline-Agent`
6. **Set** Main file path: `app.py`
7. **Add Secrets** (click Advanced settings):
   ```toml
   DEEPSEEK_API_KEY = "your_api_key_here"
   ```
8. **Deploy!** 🎉

**Pros**: Free, automatic HTTPS, zero configuration
**Cons**: Limited resources, public by default

---

### 2. Docker Deployment

**Best for**: Production environments, self-hosting, cloud VMs

#### Prerequisites
- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose (included with Docker Desktop)

#### Quick Start
```bash
# 1. Clone the repository
git clone https://github.com/nadir-sheikh09/Content-Generation-Pipeline-Agent.git
cd Content-Generation-Pipeline-Agent

# 2. Create .env file
echo "DEEPSEEK_API_KEY=your_api_key_here" > .env

# 3. Build and run
docker-compose up -d

# 4. Access at http://localhost:8501
```

#### Manual Docker Commands
```bash
# Build the image
docker build -t ai-content-pipeline .

# Run the container
docker run -d \
  -p 8501:8501 \
  -e DEEPSEEK_API_KEY=your_api_key_here \
  --name content-pipeline \
  ai-content-pipeline

# View logs
docker logs -f content-pipeline

# Stop the container
docker stop content-pipeline
```

---

### 3. Railway Deployment

**Best for**: Hobby projects, automatic deployments from GitHub

1. **Visit** [railway.app](https://railway.app/)
2. **Click** "Start a New Project"
3. **Select** "Deploy from GitHub repo"
4. **Choose** `Content-Generation-Pipeline-Agent`
5. **Add Environment Variables**:
   - Key: `DEEPSEEK_API_KEY`
   - Value: Your API key
6. **Deploy** automatically!

**Cost**: ~$5/month for hobby tier

---

### 4. Render Deployment

**Best for**: Free tier, automatic SSL, custom domains

1. **Visit** [render.com](https://render.com/)
2. **Click** "New +" → "Web Service"
3. **Connect** your GitHub repository
4. **Configure**:
   - Name: `ai-content-pipeline`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`
5. **Add Environment Variable**:
   - Key: `DEEPSEEK_API_KEY`
   - Value: Your API key
6. **Create Web Service**

**Free Tier**: Available with limitations

---

### 5. AWS / GCP / Azure

**Best for**: Enterprise deployments, high traffic

#### AWS Elastic Beanstalk
```bash
# Install EB CLI
pip install awsebcli

# Initialize
eb init -p python-3.12 ai-content-pipeline

# Create environment
eb create production-env

# Set environment variables
eb setenv DEEPSEEK_API_KEY=your_api_key_here

# Deploy
eb deploy
```

#### Google Cloud Run
```bash
# Build and push to Container Registry
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/ai-content-pipeline

# Deploy to Cloud Run
gcloud run deploy ai-content-pipeline \
  --image gcr.io/YOUR_PROJECT_ID/ai-content-pipeline \
  --platform managed \
  --region us-central1 \
  --set-env-vars DEEPSEEK_API_KEY=your_api_key_here
```

---

## 🔒 Security Best Practices

1. **Never commit `.env` files** (already in `.gitignore`)
2. **Use environment variables** for all secrets
3. **Enable HTTPS** in production (automatic on most platforms)
4. **Implement rate limiting** if exposing publicly
5. **Monitor API usage** to prevent unexpected costs

---

## 📊 Monitoring & Logs

### Docker Logs
```bash
docker logs -f content-pipeline
```

### Streamlit Cloud
- View logs in the Streamlit Cloud dashboard
- Check "Manage app" → "Logs"

### Production Monitoring
Consider adding:
- [Sentry](https://sentry.io/) for error tracking
- [Datadog](https://www.datadoghq.com/) for performance monitoring
- [Uptime Robot](https://uptimerobot.com/) for availability checks

---

## 🆘 Troubleshooting

### App won't start
- Check that `DEEPSEEK_API_KEY` is set correctly
- Verify Python version is 3.12+
- Review logs for specific error messages

### API errors
- Verify your DeepSeek API key is valid
- Check your API balance at [platform.deepseek.com](https://platform.deepseek.com)
- Ensure you're not hitting rate limits

### Docker issues
- Make sure Docker daemon is running
- Try rebuilding: `docker-compose build --no-cache`
- Check port 8501 isn't already in use

---

## 📞 Support

For deployment issues, please:
1. Check the [GitHub Issues](https://github.com/nadir-sheikh09/Content-Generation-Pipeline-Agent/issues)
2. Review the troubleshooting section above
3. Open a new issue with deployment logs

---

**Happy Deploying! 🚀**
