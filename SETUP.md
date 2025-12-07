# MedLink Agent - Setup Guide

## 📦 Requirements

### Python Version
- Python 3.9 or higher

### Dependencies
```
streamlit>=1.28.0      # Web UI framework
google-genai>=1.0.0    # Gemini AI SDK
Pillow>=10.0.0         # Image processing
python-dotenv>=1.0.0   # Environment variables
```

### Install All Dependencies
```bash
pip install -r requirements.txt
```

---

## 🔑 API Keys Required

### 1. Google Gemini API Key (REQUIRED)

This is the **ONLY** API key you need!

**How to get it:**
1. Go to [Google AI Studio](https://aistudio.google.com/)
2. Sign in with your Google account
3. Click "Get API Key" in the left sidebar
4. Click "Create API Key"
5. Copy the key

**Setup:**
```bash
# Create .env file in project root
echo GOOGLE_API_KEY=your_api_key_here > .env
```

Or manually create `.env` file:
```
GOOGLE_API_KEY=AIzaSy...your_key_here
```

---

## 🚀 Quick Start

```bash
# 1. Clone/navigate to project
cd c:\Users\mrkri\Desktop\MedLinkAI

# 2. Install dependencies
pip install -r requirements.txt

# 3. Create .env with your API key
# Edit .env and add: GOOGLE_API_KEY=your_key

# 4. Run the app
python -m streamlit run app.py

# 5. Open browser to http://localhost:8501
```

---

## ✅ Verification Checklist

- [ ] Python 3.9+ installed
- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] `.env` file created with `GOOGLE_API_KEY`
- [ ] App runs with `python -m streamlit run app.py`
- [ ] Browser opens to `http://localhost:8501`

---

## ❓ Troubleshooting

| Issue | Solution |
|-------|----------|
| `streamlit not found` | Run: `pip install streamlit` |
| `google-genai not found` | Run: `pip install google-genai` |
| API errors | Check your GOOGLE_API_KEY in .env |
| Port 8501 in use | Run: `streamlit run app.py --server.port 8502` |

---

## 💰 Cost

- **Gemini API**: Free tier available (sufficient for hackathon demo)
- **No other paid services required**
