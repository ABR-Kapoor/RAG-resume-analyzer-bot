# 🚀 Streamlit Cloud Deployment Guide

## Step-by-Step Deployment Instructions

### 1️⃣ Prepare Your Repository

1. **Create a GitHub repository** (if you haven't already):
   - Go to https://github.com/new
   - Name it: `resume-analyzer-bot` (or any name you prefer)
   - Make it **Public** (required for Streamlit Cloud free tier)
   - Don't initialize with README (we already have one)

2. **Push this deployment folder to GitHub**:

```bash
# Navigate to the deployment folder
cd G:\timepass\RAG-ResumeApp\deployment

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial deployment setup"

# Add your GitHub repository as remote
git remote add origin https://github.com/YOUR_USERNAME/resume-analyzer-bot.git

# Push to GitHub
git push -u origin main
```

### 2️⃣ Get Your API Keys Ready

You'll need these before deployment:

**Groq API Key:**
1. Go to https://console.groq.com
2. Sign up/Login
3. Go to "API Keys"
4. Click "Create API Key"
5. Copy the key (starts with `gsk_...`)

**Pinecone API Key:**
1. Go to https://www.pinecone.io
2. Sign up/Login
3. Go to "API Keys"
4. Copy your API key

### 3️⃣ Deploy to Streamlit Cloud

1. **Go to Streamlit Cloud**:
   - Visit https://share.streamlit.io
   - Click "Sign up" or "Sign in" with GitHub

2. **Create New App**:
   - Click "New app" button
   - Select your repository: `YOUR_USERNAME/resume-analyzer-bot`
   - Branch: `main`
   - Main file path: `app.py`

3. **Configure Advanced Settings**:
   - Click "Advanced settings"
   - Add secrets in the "Secrets" section:

```toml
GROQ_API_KEY = "gsk_your_actual_groq_api_key_here"
PINECONE_API_KEY = "your_actual_pinecone_api_key_here"
PINECONE_INDEX_NAME = "babybot-medical-index"
PINECONE_ENVIRONMENT = "us-east-1"
```

4. **Deploy**:
   - Click "Deploy!"
   - Wait 2-5 minutes for deployment
   - Your app will be live at: `https://YOUR_USERNAME-resume-analyzer-bot.streamlit.app`

### 4️⃣ Test Your Deployed App

1. Open your deployed URL
2. Upload a test PDF resume
3. Ask a question: "What is the candidate's name?"
4. Verify the response is correct

### 5️⃣ Update Your App (Future Changes)

Whenever you make changes:

```bash
# Make your code changes
# Then commit and push:
git add .
git commit -m "Description of changes"
git push origin main
```

Streamlit Cloud will **automatically redeploy** within 1-2 minutes!

## 🔧 Troubleshooting

### Error: "No module named 'sentence_transformers'"
- **Fix**: Already handled in `requirements.txt`

### Error: "GROQ_API_KEY not found"
- **Fix**: Double-check secrets in Streamlit Cloud settings
- Make sure there are no extra spaces or quotes

### Error: "Index not found"
- **Fix**: The app will auto-create the Pinecone index on first upload
- Make sure `PINECONE_INDEX_NAME` matches in secrets

### App is slow on first load
- **Normal**: Streamlit Cloud apps sleep after inactivity
- First load takes 10-30 seconds (cold start)
- Subsequent loads are instant

### Want to use a custom domain?
- **Free tier**: Use the default `.streamlit.app` domain
- **Paid tier** ($20/month): Add custom domain in settings

## 📊 Resource Limits (Free Tier)

- **RAM**: 1 GB
- **CPU**: Shared
- **Storage**: 1 GB
- **Apps**: Up to 3 public apps
- **Uptime**: Apps sleep after 7 days of inactivity

## 🎉 You're Done!

Your AI Resume Analyzer is now live on the internet! Share the URL with anyone.

**Example Questions to Try:**
- "Name all candidates"
- "Compare their technical skills"
- "Who has the most experience?"
- "Rate each candidate for an AI engineer position"

---

**Need Help?**
- Streamlit Docs: https://docs.streamlit.io
- Streamlit Community: https://discuss.streamlit.io
- Groq Docs: https://console.groq.com/docs
- Pinecone Docs: https://docs.pinecone.io
