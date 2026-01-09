# 🎯 Hackathon Checklist: Pre-Demo Preparation

## 📋 24 Hours Before Demo

### Technical Setup

- [ ] **Get API Keys**
  - [ ] Gemini API key from https://makersuite.google.com/app/apikey
  - [ ] (Optional) Google Search API key + Engine ID
  - [ ] (Optional) Firebase project setup

- [ ] **Install Dependencies**
  ```bash
  # Backend
  cd backend
  python -m venv venv
  venv\Scripts\activate  # Windows
  pip install -r requirements.txt
  
  # Frontend
  cd frontend
  npm install
  ```

- [ ] **Configure Environment**
  - [ ] Create `backend/.env` from `.env.example`
  - [ ] Add `GEMINI_API_KEY` to `.env`
  - [ ] (Optional) Add Google Search credentials
  - [ ] (Optional) Add Firebase config

- [ ] **Test Backend**
  ```bash
  cd backend
  python app.py
  # Should start on http://localhost:5000
  ```

- [ ] **Test Frontend**
  ```bash
  cd frontend
  npm run dev
  # Should start on http://localhost:3000
  ```

- [ ] **Verify Setup**
  ```bash
  python verify_setup.py
  # Should show all green checkmarks
  ```

---

## 🎬 2 Hours Before Demo

### Practice Run

- [ ] **Profile Creation Flow**
  - [ ] Test resume upload with sample PDF
  - [ ] Test manual profile creation
  - [ ] Verify profile displays correctly

- [ ] **Opportunity Search**
  - [ ] Search for "AI hackathon"
  - [ ] Verify results load
  - [ ] Check different opportunity types

- [ ] **Eligibility Analysis**
  - [ ] Run analysis on 3 different opportunities
  - [ ] Verify "Eligible" scenario works
  - [ ] Verify "Partially Eligible" shows guidance
  - [ ] Verify "Not Yet Eligible" shows roadmap

- [ ] **UI Polish**
  - [ ] All buttons work
  - [ ] No console errors
  - [ ] Loading states display
  - [ ] Error messages are clear

### Presentation Prep

- [ ] **Review Demo Script**
  - [ ] Read `docs/DEMO_SCRIPT.md`
  - [ ] Time yourself (should be under 5 minutes)
  - [ ] Practice smooth transitions

- [ ] **Prepare Talking Points**
  - [ ] "This is NOT a filter—it's a mentor"
  - [ ] "Eligibility is a journey, not a gate"
  - [ ] "Real data from Google Search"
  - [ ] "AI-powered guidance at scale"

- [ ] **Backup Plan**
  - [ ] Screenshots of working system
  - [ ] Sample API responses ready
  - [ ] Architecture diagram accessible

---

## 🚀 30 Minutes Before Demo

### Environment Check

- [ ] **Backend Running**
  ```bash
  cd backend
  python app.py
  # Terminal should show: "Server starting on http://localhost:5000"
  ```

- [ ] **Frontend Running**
  ```bash
  cd frontend
  npm run dev
  # Browser should open to http://localhost:3000
  ```

- [ ] **Browser Ready**
  - [ ] Open http://localhost:3000
  - [ ] Clear cache (Ctrl+Shift+Delete)
  - [ ] Close unnecessary tabs
  - [ ] Zoom level at 100%
  - [ ] Full screen mode ready (F11)

- [ ] **Internet Connection**
  - [ ] Stable WiFi/Ethernet
  - [ ] VPN off (if not needed)
  - [ ] Test Google Search API

### Demo Preparation

- [ ] **Sample Data Ready**
  - [ ] Sample profile data for quick input
  - [ ] Know your search queries ("AI hackathon", "ML internship")

- [ ] **Know Your Timings**
  - Opening: 30 seconds
  - Profile: 1 minute
  - Search: 1 minute
  - Analysis: 2 minutes ⭐
  - Scenarios: 1 minute
  - Closing: 30 seconds

- [ ] **Key Screens Bookmarked**
  - Homepage
  - Architecture diagram (if needed)
  - Prompt templates (if needed)

---

## 🎤 During Demo

### Opening (30 seconds)

- [ ] Start with problem statement
- [ ] Show homepage with tagline
- [ ] State core philosophy

### Act 1: Profile (1 minute)

- [ ] Choose upload OR manual (pick one, stick with it)
- [ ] Show AI parsing in action
- [ ] Highlight structured output

### Act 2: Search (1 minute)

- [ ] Type search query clearly
- [ ] While loading: mention real-time Google Search
- [ ] Show multiple result types

### Act 3: Analysis ⭐ (2 minutes - MOST IMPORTANT)

- [ ] Click "Check Eligibility"
- [ ] Point to status badge + confidence
- [ ] Expand detailed analysis
- [ ] **HIGHLIGHT "Next Steps"** - this is the differentiator
- [ ] Read one complete next step aloud
- [ ] Emphasize: "Not just 'no'—it's 'here's how'"

### Act 4: Scenarios (1 minute)

- [ ] Scroll through other opportunities
- [ ] Point to different colored badges
- [ ] Show how system handles each case

### Closing (30 seconds)

- [ ] Summarize: "Converts rejection into direction"
- [ ] Mention Google technologies used
- [ ] End with tagline

---

## 💡 Judge Questions - Preparation

### Technical Questions

**"How accurate is the AI?"**
> We show confidence scores for transparency. Gemini's semantic understanding is robust, but we encourage students to verify. The value is in the guidance, not just the judgment.

**"What prevents AI hallucinations?"**
> Structured prompts with JSON schema, explicit rules, and result caching for consistency.

**"How does it scale?"**
> Cloud-native architecture, caching reduces API costs, stateless design enables horizontal scaling.

### Product Questions

**"What's your competitive advantage?"**
> We're not competing with job boards. We're adding the intelligence layer they lack—the "why" and "how to improve."

**"Who are your users?"**
> Primary: Students in Tier-2/3 colleges (millions in India). Secondary: Self-taught learners, career switchers.

**"How would you monetize?"**
> B2B to colleges, freemium for students, or partnerships with opportunity platforms.

### Impact Questions

**"What problem does this solve?"**
> Students lack mentorship and clear guidance. We provide AI-powered, transparent, actionable guidance at scale.

**"Why is this better than existing solutions?"**
> Most platforms filter. We mentor. We treat eligibility as a journey and provide roadmaps for growth.

**"What's the social impact?"**
> Education equity. Students in underserved areas get the same quality guidance as those with access to expensive coaching.

---

## ⚠️ Common Issues & Fixes

### Backend Issues

**Port already in use:**
```bash
# Change port in app.py
port = int(os.getenv('PORT', 5001))
```

**Gemini API error:**
- Verify API key in `.env`
- Check quota at https://makersuite.google.com/
- Enable billing if needed

**Firebase connection error:**
- System works with mock data if Firebase isn't configured
- For demo, Firebase is optional

### Frontend Issues

**Blank screen:**
- Check browser console for errors
- Verify backend is running
- Check CORS settings

**API connection failed:**
- Ensure backend is on port 5000
- Check `vite.config.js` proxy settings

**Slow performance:**
- First AI call takes longer (model initialization)
- Subsequent calls are faster
- Results are cached

---

## 📊 Success Metrics (Judge Perspective)

### They Should Understand:

- [ ] **Problem**: Students lack guidance on eligibility
- [ ] **Solution**: AI-powered reasoning + actionable guidance
- [ ] **Differentiator**: "Journey, not gate" philosophy
- [ ] **Technical**: Uses Gemini, Google Search, Firebase
- [ ] **Impact**: Scales mentorship to underserved students

### They Should Be Impressed By:

- [ ] Real-time data integration
- [ ] Quality of AI reasoning
- [ ] Detailed, actionable guidance
- [ ] Clear, intuitive UI
- [ ] Social impact potential

---

## 🎯 Post-Demo

### If Time Permits

- [ ] Show architecture diagram
- [ ] Explain prompt engineering
- [ ] Demonstrate batch analysis
- [ ] Discuss future roadmap

### Collect Feedback

- [ ] Note judge questions
- [ ] Record suggestions
- [ ] Get contact info if interested

---

## 📝 Emergency Backup

### If Demo Breaks

**Have ready:**
- [ ] Screenshots of working system
- [ ] `ARCHITECTURE.md` diagram
- [ ] Sample API responses in `docs/SAMPLE_DATA.md`
- [ ] Walk through prompt engineering in `GEMINI_PROMPTS.md`

**Pivot to:**
> "Let me walk you through how the system works architecturally..."

Show that you understand:
- The technical implementation
- The AI reasoning process
- The product vision
- The social impact

---

## ✅ Final Checklist (5 Minutes Before)

- [ ] Backend running ✓
- [ ] Frontend running ✓
- [ ] Browser open to http://localhost:3000 ✓
- [ ] Internet connected ✓
- [ ] Demo script reviewed ✓
- [ ] Talking points memorized ✓
- [ ] Sample data ready ✓
- [ ] Timer ready ✓
- [ ] Confidence high ✓

---

## 🏆 Remember

### Your Strengths:

1. **Clear Problem**: Education inequality is real and relatable
2. **Strong Solution**: AI mentorship at scale is innovative
3. **Technical Depth**: Prompt engineering shows sophistication
4. **Product Vision**: "Journey, not gate" is memorable
5. **Execution**: Working prototype demonstrates capability

### Your Message:

> "We're not building a filter. We're building a mentor. This system doesn't decide who deserves opportunities—it helps students understand how to prepare for them."

---

## 🎬 You've Got This!

You've built a sophisticated AI application that:
- ✅ Solves a real problem
- ✅ Uses cutting-edge technology
- ✅ Has clear social impact
- ✅ Works as demonstrated

**Trust your preparation. Trust your product. Show your passion.**

**The goal isn't perfection—it's to show judges that you can:**
1. Identify important problems
2. Design innovative solutions
3. Execute with technical skill
4. Articulate impact clearly

You've done all four. Now go show them!

🎯 **Break a leg!**

---

## 📞 Last-Minute Help

If something breaks:
1. Don't panic
2. Refer to `QUICKSTART.md`
3. Check `README.md` troubleshooting
4. Use backup plan (show architecture, explain vision)
5. Pivot gracefully

**Remember**: Judges care about your thinking and problem-solving, not just working code.
