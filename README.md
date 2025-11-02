# 🤖 Noddy Bot - AI Resume Analyzer

An intelligent resume analysis system powered by Groq's LLaMA 3.3, HuggingFace embeddings, and Pinecone vector database.

## ✨ Features

- 📄 **Multi-PDF Upload**: Upload and analyze multiple resumes simultaneously
- 🔍 **Smart Retrieval**: Balanced document retrieval across all uploaded resumes
- 💬 **Interactive Chat**: Natural language queries about candidates
- 🎯 **Accurate Analysis**: Extract skills, experience, education, and more
- 🚀 **Fast & Free**: Uses free-tier APIs (Groq + local embeddings)

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **LLM**: Groq API (llama-3.3-70b-versatile)
- **Embeddings**: HuggingFace (sentence-transformers/all-MiniLM-L6-v2)
- **Vector DB**: Pinecone (Serverless)
- **Framework**: LangChain

## 📋 Prerequisites

- Python 3.8+
- Groq API Key ([Get it here](https://console.groq.com))
- Pinecone API Key ([Get it here](https://www.pinecone.io))

## 🚀 Local Setup

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd deployment
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
cp .env.example .env
```

Edit `.env` and add your API keys:
```
GROQ_API_KEY=your_groq_api_key_here
PINECONE_API_KEY=your_pinecone_api_key_here
PINECONE_INDEX_NAME=babybot-medical-index
PINECONE_ENVIRONMENT=us-east-1
```

4. **Run the application**
```bash
streamlit run app.py
```

The app will open at `http://localhost:8501`

## 🌐 Deploy to Streamlit Cloud

1. **Push to GitHub**
```bash
git add .
git commit -m "Initial commit"
git push origin main
```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Click "New app"
   - Select your repository
   - Set main file path: `app.py`
   - Add secrets in "Advanced settings":
     ```toml
     GROQ_API_KEY = "your_groq_api_key"
     PINECONE_API_KEY = "your_pinecone_api_key"
     PINECONE_INDEX_NAME = "babybot-medical-index"
     PINECONE_ENVIRONMENT = "us-east-1"
     ```
   - Click "Deploy"

## 📖 Usage

1. **Upload Resumes**: Use the sidebar to upload PDF resumes
2. **Ask Questions**: Type questions like:
   - "Name all candidates"
   - "Compare the skills of all candidates"
   - "Who has AI/ML experience?"
   - "Rate each candidate for a senior developer position"
3. **View Sources**: Click "View Sources" to see which resumes were referenced

## 🔧 Configuration

- **Chunk Size**: 500 characters (in `modules/vectorstore.py`)
- **Chunk Overlap**: 50 characters
- **Top-K Retrieval**: 20 chunks (in `modules/query_handler.py`)
- **Chunks per Document**: 3-10 (balanced selection)
- **Embedding Dimension**: 384

## 📁 Project Structure

```
deployment/
├── app.py                  # Main Streamlit app
├── components/
│   ├── upload.py          # PDF upload UI
│   └── chat.py            # Chat interface
├── modules/
│   ├── vectorstore.py     # Pinecone + embeddings
│   ├── query_handler.py   # Query processing
│   └── llm.py             # LLM chain setup
├── uploaded_docs/         # Stored PDFs
├── requirements.txt       # Dependencies
├── .env.example          # Environment template
└── README.md             # This file
```

## 🐛 Troubleshooting

**Issue: "No documents found"**
- Check if PDFs are uploaded successfully
- Verify Pinecone index exists and has data

**Issue: "API quota exceeded"**
- Groq free tier: 30 requests/minute
- Wait a minute and try again

**Issue: "Only retrieving from one resume"**
- This is fixed! The app now uses balanced multi-document retrieval

## 👨‍💻 Developer

Developed by **Abeer Kapoor**

## 📄 License

MIT License
