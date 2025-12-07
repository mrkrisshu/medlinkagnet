# MedLink Agent 🏥

**Your Health Navigator | English • ಕನ್ನಡ • हिंदी**

> 6-Agent System | Gemini AI + ADK | 3-Hour Hackathon Build

---

## 🚀 Quick Start (2 minutes)

```bash
# 1. Install
pip install -r requirements.txt

# 2. Set API Key
# Create .env file with: GOOGLE_API_KEY=your_key_here

# 3. Run
streamlit run app.py
```

---

## 🎯 6 Agents

| # | Agent | What It Does |
|---|-------|--------------|
| 1 | 📄 **Report Extractor** | Extracts data from lab reports/prescriptions using Gemini Vision |
| 2 | 💊 **Medicine Safety** | Checks drug interactions, timing, do's & don'ts |
| 3 | 📅 **Timeline Builder** | Creates health journey timeline with trends |
| 4 | ⏰ **Reminder** | Generates medicine schedules |
| 5 | 🩹 **First-Aid** | General first-aid guidance (NO diagnosis) |
| 6 | 👨‍⚕️ **Doctor Compare** | Compares 2-4 doctor opinions objectively |

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────┐
│           STREAMLIT UI (6 Tabs)             │
└─────────────────────┬───────────────────────┘
                      │
        ┌─────────────┼─────────────┐
        ▼             ▼             ▼
┌─────────────┐ ┌───────────┐ ┌───────────┐
│Report Agent │ │Med Agent  │ │Timeline   │
│(Vision API) │ │(Safety)   │ │Agent      │
└─────────────┘ └───────────┘ └───────────┘
        ▼             ▼             ▼
┌─────────────┐ ┌───────────┐ ┌───────────┐
│Reminder     │ │Symptom    │ │Doctor     │
│Agent        │ │First-Aid  │ │Compare    │
└─────────────┘ └───────────┘ └───────────┘
                      │
              ┌───────┴───────┐
              │ Gemini 2.0    │
              │ Flash/Vision  │
              └───────────────┘
                      │
              ┌───────┴───────┐
              │ JSON Storage  │
              └───────────────┘
```

---

## 🔐 Safety Rules

| ❌ We DON'T | ✅ We DO |
|-------------|----------|
| Diagnose diseases | Extract existing data |
| Recommend medicines | Show timing guidance |
| Replace doctors | Help organize information |
| Make medical decisions | Provide first-aid tips |

---

## 🎤 Demo Script (3 Minutes)

### Minute 1: Problem (60 sec)
> "Meet Ravi, 55, managing diabetes with high BP. He has:
> - 5 lab reports from different hospitals
> - 8 medicines from 3 doctors
> - No idea if medicines conflict
> - Forgot yesterday's dose
> - Doctor opinions that contradict each other
> 
> **73% of Indians struggle to manage multiple prescriptions.**"

### Minute 2: Solution (60 sec)
> "MedLink Agent - 6 AI agents that:
> 1. **Extract** any report in seconds (Vision AI)
> 2. **Check** medicine conflicts automatically
> 3. **Build** your health timeline
> 4. **Remind** you to take medicines
> 5. **Guide** first-aid safely
> 6. **Compare** doctor opinions objectively
> 
> **All in 3 languages: English, Kannada, Hindi**"

### Minute 3: Live Demo (60 sec)
1. Upload blood test → Show trilingual extraction
2. Add 3 medicines → Show conflict detection
3. Type "headache, nausea" → Show first-aid
4. Compare 2 doctor opinions → Show agreement

---

## 🏆 Why We Win

| Feature | Others | MedLink |
|---------|--------|---------|
| Languages | 1 | 3 (EN/KN/HI) |
| Vision AI | ❌ | ✅ Gemini 2.0 |
| Drug Conflicts | ❌ | ✅ Real-time |
| Doctor Compare | ❌ | ✅ Objective |
| Safety Layer | ❌ | ✅ No diagnosis |
| Agents | 1-2 | 6 specialized |

---

## ⏱️ 3-Hour Build Plan

| Time | Task |
|------|------|
| 0:00-0:30 | Setup + Install + Test API |
| 0:30-1:00 | Build Report + Medicine agents |
| 1:00-1:30 | Build Timeline + Reminder agents |
| 1:30-2:00 | Build Symptom + Doctor Compare agents |
| 2:00-2:30 | Build UI + Integrate all agents |
| 2:30-3:00 | Debug + Rehearse demo |

---

## 📁 Project Structure

```
medlink-agent/
├── app.py                      # Streamlit UI (6 tabs)
├── agents/
│   ├── report_agent.py         # Vision extraction
│   ├── medicine_agent.py       # Drug safety
│   ├── timeline_agent.py       # Health timeline
│   ├── reminder_agent.py       # Schedules
│   ├── symptom_agent.py        # First-aid
│   └── doctor_compare_agent.py # Compare opinions
├── prompts/
│   └── system_prompts.py       # Trilingual prompts
├── data/                       # JSON storage
└── requirements.txt
```

---

## 🌟 Stretch Features

- [ ] Voice input (regional languages)
- [ ] WhatsApp integration
- [ ] Family health dashboard
- [ ] PDF export of timeline
- [ ] Real-time notification system

---

Built with ❤️ for Hackathon | Powered by Google Gemini + ADK
