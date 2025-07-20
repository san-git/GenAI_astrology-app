# 🌟 Astrology App - AI Powered

A comprehensive astrology application with AI-powered interpretations using Google's Gemini Pro. Features include zodiac readings, Kundali (birth chart) generation, compatibility checking, and personalized AI consultations.

## 🚀 Features

### ✨ Core Features
- **🌟 Basic Zodiac Reading & Daily Horoscope** - Get your zodiac sign, traits, and daily horoscope
- **💕 Zodiac Compatibility Checker** - Check compatibility between any two zodiac signs
- **💎 Daily Crystal Recommendation** - Get personalized crystal recommendations
- **🔮 All-in-One Reading** - Complete astrological profile with all insights
- **🕉️ Generate Kundali (Birth Chart)** - Create detailed Vedic birth charts with planetary positions
- **🤖 Gemini AI Astrology Consultation** - Ask personalized questions about your chart

### 🎯 AI-Powered Features
- **Past, Present, Future Analysis** - Deep insights about your life journey
- **Planetary Placement Analysis** - What each planet in each sign/house means
- **Career Guidance** - Based on your Mars, Jupiter, and 10th house placements
- **Relationship Insights** - Venus, Moon, and 7th house analysis
- **Personal Growth** - Saturn and challenging placements guidance
- **Spiritual Development** - Jupiter, Neptune, and 12th house insights

## 📁 App Versions

1. **`astrology_app.py`** - Original CLI version with OpenAI integration
2. **`astrology_app_gemini.py`** - CLI version with Google Gemini Pro integration
3. **`astrology_app_streamlit.py`** - **Web app version** with beautiful UI and Gemini Pro

## 🛠️ Installation

### Prerequisites
- Python 3.7 or higher
- Google API key for Gemini Pro

### Setup

1. **Clone or download the project**
2. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

3. **Set up Google API key:**
   ```bash
   export GOOGLE_API_KEY='your-api-key-here'
   ```
   
   Or create a `.env` file:
   ```
   GOOGLE_API_KEY=your-api-key-here
   ```

## 🚀 Running the Apps

### Web App (Recommended)
```bash
streamlit run astrology_app_streamlit.py
```
This will open a beautiful web interface in your browser!

### CLI Versions
```bash
# Original version with OpenAI
python3 astrology_app.py

# Gemini version
python3 astrology_app_gemini.py
```

## 🌐 Deployment Options

### 1. Streamlit Cloud (Recommended)
1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy automatically!

### 2. Heroku
1. Create a `Procfile`:
   ```
   web: streamlit run astrology_app_streamlit.py --server.port=$PORT --server.address=0.0.0.0
   ```
2. Deploy to Heroku with your requirements.txt

### 3. Railway
1. Connect your GitHub repository
2. Railway will automatically detect and deploy your Streamlit app

### 4. Local Network
```bash
streamlit run astrology_app_streamlit.py --server.address=0.0.0.0 --server.port=8501
```

## 🔑 Getting Google API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Create a new API key
3. Set it as environment variable or in Streamlit secrets

## 📊 Sample Questions for AI Consultation

- "Summarize my astrological profile"
- "What does my Mars in Gemini placement mean for my career?"
- "How do my planetary positions affect my relationships?"
- "What are my strengths and challenges based on my chart?"
- "Give me insights about my past, present, and future"
- "What does my Jupiter in the 4th house indicate?"
- "How can I work with my Saturn placement for personal growth?"
- "What career paths would suit my planetary configuration?"
- "How do my planetary aspects influence my communication style?"
- "What spiritual practices would benefit me based on my chart?"

## 🎨 Features of the Web App

### Beautiful UI
- **Responsive design** - Works on desktop, tablet, and mobile
- **Interactive charts** - Visual Kundali birth chart with clickable planets
- **Gradient styling** - Beautiful color schemes and animations
- **Sidebar navigation** - Easy access to all features

### Interactive Elements
- **Date pickers** - Easy birth date selection
- **Form inputs** - Structured data entry for birth details
- **Real-time calculations** - Instant planetary position calculations
- **AI chat interface** - Natural language questions and answers

### Data Visualization
- **Kundali chart** - Interactive circular birth chart
- **Planetary positions table** - Detailed planet information
- **House analysis** - Visual representation of house placements
- **Compatibility matrix** - Easy-to-read compatibility results

## 🔧 Technical Details

### Dependencies
- **Streamlit** - Web framework
- **Plotly** - Interactive charts
- **Ephem** - Astronomical calculations
- **Google Generative AI** - Gemini Pro integration
- **Pandas** - Data manipulation
- **NumPy** - Numerical computations

### Architecture
- **Modular design** - Separate functions for each feature
- **Session state management** - Persistent user data
- **Error handling** - Graceful fallbacks for API issues
- **Responsive layout** - Adapts to different screen sizes

## 🌟 Usage Examples

### Basic Zodiac Reading
1. Select "🌟 Basic Zodiac Reading & Daily Horoscope"
2. Enter your birth date
3. Get instant zodiac sign, traits, and horoscope

### Kundali Generation
1. Select "🕉️ Generate Kundali (Birth Chart)"
2. Enter birth details (date, time, location)
3. View interactive birth chart and planetary positions

### AI Consultation
1. Generate your Kundali first
2. Select "🤖 Gemini AI Astrology Consultation"
3. Ask any astrology question
4. Get personalized AI interpretation

## 🎯 Future Enhancements

- **User accounts** - Save and load birth charts
- **Transit calculations** - Current planetary transits
- **Relationship compatibility** - Detailed partner analysis
- **Remedial measures** - Gemstones, mantras, and rituals
- **Mobile app** - Native iOS/Android versions
- **Multi-language support** - Hindi, Spanish, French, etc.

## 📞 Support

For issues or questions:
1. Check the error messages in the app
2. Verify your API key is set correctly
3. Ensure all dependencies are installed
4. Check your internet connection for AI features

## 📄 License

This project is open source and available under the MIT License.

---

**🌟 May the stars guide your path! ✨** 