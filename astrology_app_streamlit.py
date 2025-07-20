#!/usr/bin/env python3
# Astrology App - Streamlit Web Version
# Converted from CLI to beautiful web interface

import streamlit as st
import datetime
import random
import ephem
import math
import os
import json
from typing import Dict, List, Optional
import plotly.graph_objects as go
import plotly.express as px

# Page configuration
st.set_page_config(
    page_title="🌟 Astrology App - AI Powered",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for beautiful styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #FF6B6B;
        text-align: center;
        margin-bottom: 2rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    .sub-header {
        font-size: 1.5rem;
        color: #4ECDC4;
        margin-bottom: 1rem;
    }
    .feature-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 1rem 0;
    }
    .planet-card {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 10px;
        color: white;
        margin: 0.5rem 0;
    }
    .kundali-chart {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'current_kundali' not in st.session_state:
    st.session_state.current_kundali = None
if 'user_name' not in st.session_state:
    st.session_state.user_name = "User"

# Zodiac signs and their date ranges
zodiac_signs = {
    "Aries": (datetime.date(2000, 3, 21), datetime.date(2000, 4, 19)),
    "Taurus": (datetime.date(2000, 4, 20), datetime.date(2000, 5, 20)),
    "Gemini": (datetime.date(2000, 5, 21), datetime.date(2000, 6, 20)),
    "Cancer": (datetime.date(2000, 6, 21), datetime.date(2000, 7, 22)),
    "Leo": (datetime.date(2000, 7, 23), datetime.date(2000, 8, 22)),
    "Virgo": (datetime.date(2000, 8, 23), datetime.date(2000, 9, 22)),
    "Libra": (datetime.date(2000, 9, 23), datetime.date(2000, 10, 22)),
    "Scorpio": (datetime.date(2000, 10, 23), datetime.date(2000, 11, 21)),
    "Sagittarius": (datetime.date(2000, 11, 22), datetime.date(2000, 12, 21)),
    "Capricorn": (datetime.date(2000, 12, 22), datetime.date(2001, 1, 19)),
    "Aquarius": (datetime.date(2000, 1, 20), datetime.date(2000, 2, 18)),
    "Pisces": (datetime.date(2000, 2, 19), datetime.date(2000, 3, 20))
}

# Vedic astrology planets and their Sanskrit names
vedic_planets = {
    "Sun": {"sanskrit": "Surya", "element": "Fire", "nature": "Benefic", "significance": "Soul, father, authority, ego", "color": "#FFD700"},
    "Moon": {"sanskrit": "Chandra", "element": "Water", "nature": "Benefic", "significance": "Mind, mother, emotions, intuition", "color": "#C0C0C0"},
    "Mars": {"sanskrit": "Mangal", "element": "Fire", "nature": "Malefic", "significance": "Energy, courage, brother, aggression", "color": "#FF4500"},
    "Mercury": {"sanskrit": "Budh", "element": "Earth", "nature": "Neutral", "significance": "Communication, intelligence, business", "color": "#32CD32"},
    "Jupiter": {"sanskrit": "Guru", "element": "Ether", "nature": "Benefic", "significance": "Wisdom, teacher, children, spirituality", "color": "#FF8C00"},
    "Venus": {"sanskrit": "Shukra", "element": "Water", "nature": "Benefic", "significance": "Love, beauty, relationships, arts", "color": "#FF69B4"},
    "Saturn": {"sanskrit": "Shani", "element": "Air", "nature": "Malefic", "significance": "Discipline, karma, obstacles, lessons", "color": "#708090"}
}

# Vedic zodiac signs (Rashis) and their characteristics
vedic_rashis = {
    "Aries": {"sanskrit": "Mesha", "element": "Fire", "ruler": "Mars", "quality": "Cardinal", "characteristics": "Pioneering, energetic, impulsive"},
    "Taurus": {"sanskrit": "Vrishabha", "element": "Earth", "ruler": "Venus", "quality": "Fixed", "characteristics": "Stable, patient, sensual"},
    "Gemini": {"sanskrit": "Mithuna", "element": "Air", "ruler": "Mercury", "quality": "Mutable", "characteristics": "Versatile, curious, communicative"},
    "Cancer": {"sanskrit": "Karka", "element": "Water", "ruler": "Moon", "quality": "Cardinal", "characteristics": "Nurturing, emotional, protective"},
    "Leo": {"sanskrit": "Simha", "element": "Fire", "ruler": "Sun", "quality": "Fixed", "characteristics": "Confident, creative, generous"},
    "Virgo": {"sanskrit": "Kanya", "element": "Earth", "ruler": "Mercury", "quality": "Mutable", "characteristics": "Analytical, practical, perfectionist"},
    "Libra": {"sanskrit": "Tula", "element": "Air", "ruler": "Venus", "quality": "Cardinal", "characteristics": "Diplomatic, balanced, relationship-oriented"},
    "Scorpio": {"sanskrit": "Vrishchika", "element": "Water", "ruler": "Mars", "quality": "Fixed", "characteristics": "Intense, mysterious, transformative"},
    "Sagittarius": {"sanskrit": "Dhanu", "element": "Fire", "ruler": "Jupiter", "quality": "Mutable", "characteristics": "Optimistic, adventurous, philosophical"},
    "Capricorn": {"sanskrit": "Makara", "element": "Earth", "ruler": "Saturn", "quality": "Cardinal", "characteristics": "Ambitious, disciplined, responsible"},
    "Aquarius": {"sanskrit": "Kumbha", "element": "Air", "ruler": "Saturn", "quality": "Fixed", "characteristics": "Innovative, independent, humanitarian"},
    "Pisces": {"sanskrit": "Meena", "element": "Water", "ruler": "Jupiter", "quality": "Mutable", "characteristics": "Compassionate, artistic, spiritual"}
}

# House significations in Vedic astrology
house_significations = {
    1: "Self, personality, appearance, health, vitality",
    2: "Wealth, family, speech, face, food, values",
    3: "Communication, siblings, courage, short journeys, hands",
    4: "Home, mother, property, vehicles, comfort, emotions",
    5: "Children, creativity, intelligence, romance, speculation",
    6: "Health, enemies, obstacles, service, pets, debts",
    7: "Marriage, partnerships, spouse, business relations",
    8: "Longevity, transformation, occult, inheritance, obstacles",
    9: "Religion, guru, higher education, foreign travel, luck",
    10: "Career, profession, authority, reputation, father",
    11: "Income, gains, friends, elder siblings, desires",
    12: "Expenses, losses, spirituality, foreign lands, sleep"
}

# Zodiac sign characteristics
zodiac_traits = {
    "Aries": "Bold, ambitious, and energetic. Natural leaders with a pioneering spirit.",
    "Taurus": "Patient, reliable, and determined. Love comfort and have a strong work ethic.",
    "Gemini": "Adaptable, curious, and quick-witted. Excellent communicators and social butterflies.",
    "Cancer": "Nurturing, protective, and intuitive. Deeply emotional and family-oriented.",
    "Leo": "Confident, creative, and generous. Natural performers who love being in the spotlight.",
    "Virgo": "Analytical, kind, and hardworking. Perfectionists with a practical approach to life.",
    "Libra": "Diplomatic, gracious, and fair-minded. Seek balance and harmony in all relationships.",
    "Scorpio": "Passionate, determined, and magnetic. Deep thinkers with strong intuition.",
    "Sagittarius": "Optimistic, adventurous, and honest. Love freedom and exploring new horizons.",
    "Capricorn": "Responsible, disciplined, and ambitious. Natural leaders with strong determination.",
    "Aquarius": "Original, independent, and humanitarian. Forward-thinking visionaries.",
    "Pisces": "Compassionate, artistic, and intuitive. Deeply spiritual and empathetic."
}

# Compatibility matrix for zodiac signs
compatibility_matrix = {
    "Aries": ["Leo", "Sagittarius", "Gemini", "Aquarius"],
    "Taurus": ["Virgo", "Capricorn", "Cancer", "Pisces"],
    "Gemini": ["Libra", "Aquarius", "Aries", "Leo"],
    "Cancer": ["Scorpio", "Pisces", "Taurus", "Virgo"],
    "Leo": ["Aries", "Sagittarius", "Gemini", "Libra"],
    "Virgo": ["Taurus", "Capricorn", "Cancer", "Scorpio"],
    "Libra": ["Gemini", "Aquarius", "Leo", "Sagittarius"],
    "Scorpio": ["Cancer", "Pisces", "Virgo", "Capricorn"],
    "Sagittarius": ["Aries", "Leo", "Libra", "Aquarius"],
    "Capricorn": ["Taurus", "Virgo", "Scorpio", "Pisces"],
    "Aquarius": ["Gemini", "Libra", "Aries", "Sagittarius"],
    "Pisces": ["Cancer", "Scorpio", "Taurus", "Capricorn"]
}

class HuggingFaceAstrologyInterpreter:
    """AI-powered astrology interpreter using Hugging Face models"""
    
    def __init__(self):
        # Hugging Face API token (optional for free tier)
        self.api_token = st.secrets.get("HUGGINGFACE_API_TOKEN", os.getenv('HUGGINGFACE_API_TOKEN'))
        self.model_name = "mistralai/Mistral-7B-Instruct-v0.2"  # Free model
        self.api_url = f"https://api-inference.huggingface.co/models/{self.model_name}"
        
        # Note: API token is optional - works with free tier
    
    def create_astrology_prompt(self, kundali_data: Dict, question: str) -> str:
        """Create a detailed prompt for astrology interpretation"""
        
        planets_info = []
        for planet, data in kundali_data['planets'].items():
            vedic_info = vedic_planets.get(planet, {})
            sign_info = vedic_rashis.get(data['sign'], {})
            house_info = house_significations.get(data['house'], "")
            
            planet_desc = f"{planet} ({vedic_info.get('sanskrit', '')}) in {data['sign']} ({sign_info.get('sanskrit', '')}) in House {data['house']} ({house_info})"
            planets_info.append(planet_desc)
        
        prompt = f"""<s>[INST] You are an expert Vedic astrologer with deep knowledge of both Western and Indian astrology. Analyze the following birth chart (Kundali) and provide insightful, personalized interpretations.

BIRTH CHART DATA:
- Ascendant (Lagna): {kundali_data['ascendant']['sign']}
- Birth Date: {kundali_data['birth_data']['day']}/{kundali_data['birth_data']['month']}/{kundali_data['birth_data']['year']}
- Birth Time: {kundali_data['birth_data']['hour']:02d}:{kundali_data['birth_data']['minute']:02d}

PLANETARY POSITIONS:
{chr(10).join(planets_info)}

USER QUESTION: {question}

Please provide a comprehensive, insightful interpretation that:
1. Addresses the specific question asked
2. Integrates Vedic and Western astrological principles
3. Provides practical, actionable insights
4. Uses a warm, supportive tone
5. Includes both strengths and growth opportunities
6. Relates to real-life situations and experiences

Format your response in a clear, structured way with relevant sections and bullet points where appropriate. [/INST]"""
        
        return prompt
    
    def get_ai_interpretation(self, kundali_data: Dict, question: str) -> str:
        """Get AI interpretation for astrology question using Hugging Face"""
        
        try:
            import requests
            import json
            import time
            
            prompt = self.create_astrology_prompt(kundali_data, question)
            
            headers = {
                "Content-Type": "application/json"
            }
            
            if self.api_token:
                headers["Authorization"] = f"Bearer {self.api_token}"
            
            payload = {
                "inputs": prompt,
                "parameters": {
                    "max_new_tokens": 800,  # Reduced to avoid rate limits
                    "temperature": 0.7,
                    "top_p": 0.9,
                    "do_sample": True
                }
            }
            
            # Try up to 3 times with exponential backoff
            for attempt in range(3):
                try:
                    response = requests.post(self.api_url, headers=headers, json=payload, timeout=30)
                    
                    if response.status_code == 200:
                        result = response.json()
                        if isinstance(result, list) and len(result) > 0:
                            return result[0].get('generated_text', '').replace(prompt, '').strip()
                        else:
                            return str(result)
                    elif response.status_code == 429:
                        if attempt < 2:  # Don't wait on last attempt
                            wait_time = (2 ** attempt) * 2  # 2, 4, 8 seconds
                            st.info(f"🤖 AI is busy, waiting {wait_time} seconds...")
                            time.sleep(wait_time)
                            continue
                        else:
                            st.info("🤖 AI service is currently busy. Here's a detailed astrological interpretation based on your chart:")
                            return self.get_fallback_interpretation(kundali_data, question)
                    else:
                        st.info(f"🤖 AI service temporarily unavailable. Here's a detailed astrological interpretation:")
                        return self.get_fallback_interpretation(kundali_data, question)
                        
                except requests.exceptions.Timeout:
                    if attempt < 2:
                        st.info("🤖 AI is taking longer than expected, retrying...")
                        time.sleep(2)
                        continue
                    else:
                        st.info("🤖 AI service is slow. Here's a detailed astrological interpretation:")
                        return self.get_fallback_interpretation(kundali_data, question)
                        
            return self.get_fallback_interpretation(kundali_data, question)
                
        except ImportError:
            st.error("⚠️ Requests library not installed. Install with: pip install requests")
            return self.get_fallback_interpretation(kundali_data, question)
        except Exception as e:
            st.info("🤖 AI service temporarily unavailable. Here's a detailed astrological interpretation:")
            return self.get_fallback_interpretation(kundali_data, question)
    
    def get_fallback_interpretation(self, kundali_data: Dict, question: str) -> str:
        """Provide detailed fallback interpretation without AI"""
        
        sun_sign = kundali_data['planets']['Sun']['sign']
        moon_sign = kundali_data['planets']['Moon']['sign']
        ascendant = kundali_data['ascendant']['sign']
        
        # Enhanced interpretation based on the question
        question_lower = question.lower()
        
        interpretation = f"""
🌟 DETAILED ASTROLOGICAL INTERPRETATION 🌟

Based on your birth chart analysis:

☀️ SUN SIGN ({sun_sign}): {zodiac_traits[sun_sign]}
🌙 MOON SIGN ({moon_sign}): {zodiac_traits[moon_sign]}
🌅 ASCENDANT ({ascendant}): {zodiac_traits[ascendant]}

KEY INSIGHTS:
• Your core personality is influenced by {sun_sign} energy
• Your emotional nature is shaped by {moon_sign} characteristics  
• How you appear to others is colored by {ascendant} traits

PLANETARY INFLUENCES:
"""
        
        for planet, data in kundali_data['planets'].items():
            vedic_info = vedic_planets.get(planet, {})
            house_info = house_significations.get(data['house'], "")
            interpretation += f"• {planet} in {data['sign']} (House {data['house']}): {vedic_info.get('significance', '')} - {house_info}\n"
        
        # Add specific insights based on question keywords
        if any(word in question_lower for word in ['career', 'job', 'work', 'profession']):
            interpretation += f"""
💼 CAREER INSIGHTS:
• Your {sun_sign} energy suggests leadership and initiative in professional settings
• {moon_sign} emotional patterns influence your work relationships
• {ascendant} qualities help you make strong first impressions in interviews
• Focus on developing your natural {sun_sign} strengths in your career path
"""
        elif any(word in question_lower for word in ['love', 'relationship', 'marriage', 'partner']):
            interpretation += f"""
💕 RELATIONSHIP INSIGHTS:
• Your {moon_sign} emotional nature shapes how you express love and affection
• {sun_sign} energy influences what you seek in a partner
• {ascendant} qualities determine how you appear to potential partners
• Your Venus placement in {kundali_data['planets']['Venus']['sign']} shows your approach to romance
"""
        elif any(word in question_lower for word in ['health', 'wellness', 'fitness']):
            interpretation += f"""
🏥 HEALTH INSIGHTS:
• Your {sun_sign} vitality and {moon_sign} emotional balance affect your overall health
• Pay attention to the house where your Sun is placed (House {kundali_data['planets']['Sun']['house']})
• Regular exercise that aligns with your {sun_sign} energy will be most beneficial
• Emotional wellness through {moon_sign} activities will support your health
"""
        else:
            interpretation += f"""
💡 GENERAL RECOMMENDATIONS:
• Focus on developing your {sun_sign} strengths and natural talents
• Work with your {moon_sign} emotional patterns for inner harmony
• Express your {ascendant} qualities authentically in all areas of life
• Your planetary positions suggest a balanced approach to personal growth
"""
        
        interpretation += f"""
🔮 SPECIAL COMBINATIONS:
"""
        
        # Check for special planetary combinations
        sun_house = kundali_data['planets']['Sun']['house']
        moon_house = kundali_data['planets']['Moon']['house']
        
        if sun_house == moon_house:
            interpretation += "• Sun-Moon Conjunction: Strong willpower and determination\n"
        
        if kundali_data['planets']['Jupiter']['house'] == 1:
            interpretation += "• Jupiter in 1st House: Wisdom and spiritual growth\n"
        
        if kundali_data['planets']['Saturn']['house'] == 1:
            interpretation += "• Saturn in 1st House: Discipline and life lessons\n"
        
        interpretation += f"""
✨ NEXT STEPS:
• Embrace your {sun_sign} leadership qualities
• Nurture your {moon_sign} emotional intelligence  
• Express your {ascendant} authentic personality
• Trust your intuition and inner wisdom

This interpretation is based on traditional Vedic and Western astrological principles.
"""
        
        return interpretation

def get_zodiac_sign(birth_date):
    """Determine zodiac sign based on birth date"""
    normalized_date = datetime.date(2000, birth_date.month, birth_date.day)
    
    for sign, (start_date, end_date) in zodiac_signs.items():
        if start_date <= normalized_date <= end_date:
            return sign
    return None

def get_zodiac_from_longitude(longitude):
    """Get zodiac sign from celestial longitude"""
    sign_num = int(longitude / 30)
    signs = list(zodiac_signs.keys())
    return signs[sign_num % 12]

def calculate_house_position(ascendant_longitude, planet_longitude):
    """Calculate which house a planet is in"""
    diff = (planet_longitude - ascendant_longitude) % 360
    house = int(diff / 30) + 1
    return house if house <= 12 else house - 12

def calculate_kundali(birth_data):
    """Calculate Kundali (birth chart) with planetary positions"""
    with st.spinner("🔮 Calculating your Kundali (Birth Chart)..."):
        observer = ephem.Observer()
        observer.lat = str(birth_data['latitude'])
        observer.lon = str(birth_data['longitude'])
        
        birth_datetime = datetime.datetime(
            birth_data['year'], 
            birth_data['month'], 
            birth_data['day'],
            birth_data['hour'], 
            birth_data['minute']
        )
        observer.date = birth_datetime
        
        planets_data = {}
        planet_objects = {
            'Sun': ephem.Sun(),
            'Moon': ephem.Moon(),
            'Mars': ephem.Mars(),
            'Mercury': ephem.Mercury(),
            'Jupiter': ephem.Jupiter(),
            'Venus': ephem.Venus(),
            'Saturn': ephem.Saturn()
        }
        
        for planet_name, planet_obj in planet_objects.items():
            planet_obj.compute(observer)
            longitude = math.degrees(planet_obj.hlong)
            latitude = math.degrees(planet_obj.hlat)
            
            planets_data[planet_name] = {
                'longitude': longitude,
                'latitude': latitude,
                'sign': get_zodiac_from_longitude(longitude),
                'sanskrit_name': vedic_planets[planet_name]['sanskrit'],
                'element': vedic_planets[planet_name]['element'],
                'nature': vedic_planets[planet_name]['nature']
            }
        
        ascendant_longitude = math.degrees(observer.radec_of(0, 0)[0])
        
        for planet_name in planets_data:
            house = calculate_house_position(ascendant_longitude, planets_data[planet_name]['longitude'])
            planets_data[planet_name]['house'] = house
        
        return {
            'planets': planets_data,
            'ascendant': {
                'longitude': ascendant_longitude,
                'sign': get_zodiac_from_longitude(ascendant_longitude)
            },
            'birth_data': birth_data
        }

def create_kundali_chart(kundali_data):
    """Create an interactive Kundali chart visualization"""
    
    # Create a circular chart representing the 12 houses
    fig = go.Figure()
    
    # Define house positions (12 houses in a circle)
    house_angles = [i * 30 for i in range(12)]
    house_labels = [f"House {i+1}" for i in range(12)]
    
    # Add house circles
    for i, angle in enumerate(house_angles):
        x = math.cos(math.radians(angle))
        y = math.sin(math.radians(angle))
        
        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode='markers+text',
            marker=dict(size=20, color='lightblue'),
            text=[house_labels[i]],
            textposition="middle center",
            name=f"House {i+1}",
            showlegend=False
        ))
    
    # Add planets to their respective houses
    for planet, data in kundali_data['planets'].items():
        house = data['house'] - 1  # Convert to 0-based index
        angle = house * 30 + 15  # Center planet in house
        x = 0.7 * math.cos(math.radians(angle))
        y = 0.7 * math.sin(math.radians(angle))
        
        fig.add_trace(go.Scatter(
            x=[x],
            y=[y],
            mode='markers+text',
            marker=dict(
                size=25, 
                color=vedic_planets[planet]['color'],
                symbol='star'
            ),
            text=[planet],
            textposition="middle center",
            name=planet,
            hovertemplate=f"{planet}<br>Sign: {data['sign']}<br>House: {data['house']}<extra></extra>"
        ))
    
    # Add ascendant
    asc_angle = 0  # Ascendant is always at 0 degrees
    fig.add_trace(go.Scatter(
        x=[0.9 * math.cos(math.radians(asc_angle))],
        y=[0.9 * math.sin(math.radians(asc_angle))],
        mode='markers+text',
        marker=dict(size=30, color='red', symbol='diamond'),
        text=['ASC'],
        textposition="middle center",
        name='Ascendant',
        hovertemplate=f"Ascendant: {kundali_data['ascendant']['sign']}<extra></extra>"
    ))
    
    # Update layout
    fig.update_layout(
        title="🌟 Your Kundali (Birth Chart) 🌟",
        xaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        yaxis=dict(showgrid=False, zeroline=False, showticklabels=False),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        width=600,
        height=600,
        showlegend=True,
        legend=dict(x=1.1, y=0.5)
    )
    
    return fig

def display_kundali_web(kundali_data):
    """Display the Kundali chart in web format"""
    
    st.markdown("## 🌟 YOUR KUNDALI (BIRTH CHART) 🌟")
    
    birth = kundali_data['birth_data']
    
    # Display basic info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("📅 Birth Date", f"{birth['day']}/{birth['month']}/{birth['year']}")
    with col2:
        st.metric("⏰ Birth Time", f"{birth['hour']:02d}:{birth['minute']:02d}")
    with col3:
        st.metric("🌅 Ascendant", kundali_data['ascendant']['sign'])
    
    # Create and display Kundali chart
    chart = create_kundali_chart(kundali_data)
    st.plotly_chart(chart, use_container_width=True)
    
    # Planetary positions table
    st.markdown("### 🪐 Planetary Positions")
    
    planet_data = []
    for planet_name, data in kundali_data['planets'].items():
        planet_data.append({
            "Planet": planet_name,
            "Sanskrit": data['sanskrit_name'],
            "Sign": data['sign'],
            "House": data['house'],
            "Element": data['element'],
            "Nature": data['nature']
        })
    
    st.dataframe(planet_data, use_container_width=True)
    
    # House analysis
    st.markdown("### 📊 House Analysis")
    
    houses = {}
    for planet_name, data in kundali_data['planets'].items():
        house = data['house']
        if house not in houses:
            houses[house] = []
        houses[house].append(planet_name)
    
    house_cols = st.columns(4)
    for i, house_num in enumerate(range(1, 13)):
        col_idx = i % 4
        with house_cols[col_idx]:
            planets_in_house = houses.get(house_num, [])
            if planets_in_house:
                st.info(f"🏠 House {house_num}: {', '.join(planets_in_house)}")
            else:
                st.info(f"🏠 House {house_num}: Empty")
    
    # Basic interpretations
    st.markdown("### 💫 Kundali Insights")
    
    sun_sign = kundali_data['planets']['Sun']['sign']
    moon_sign = kundali_data['planets']['Moon']['sign']
    ascendant_sign = kundali_data['ascendant']['sign']
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="planet-card">
        <h4>☀️ Sun Sign (Atman)</h4>
        <p><strong>{sun_sign}</strong><br>{zodiac_traits[sun_sign]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="planet-card">
        <h4>🌙 Moon Sign (Mind)</h4>
        <p><strong>{moon_sign}</strong><br>{zodiac_traits[moon_sign]}</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="planet-card">
        <h4>🌅 Ascendant (Personality)</h4>
        <p><strong>{ascendant_sign}</strong><br>{zodiac_traits[ascendant_sign]}</p>
        </div>
        """, unsafe_allow_html=True)

def gemini_astrology_consultation_web(kundali_data):
    """AI-powered astrology consultation web interface"""
    
    st.markdown("## 🤖 AI ASTROLOGY CONSULTATION")
    
    interpreter = HuggingFaceAstrologyInterpreter()
    
    st.markdown("""
    💭 **You can ask questions like:**
    - 'Summarize my astrological profile'
    - 'What does my Mars in Gemini placement mean for my career?'
    - 'How do my planetary positions affect my relationships?'
    - 'What are my strengths and challenges based on my chart?'
    - 'Give me insights about my past, present, and future'
    - 'What does my Jupiter in the 4th house indicate?'
    - 'How can I work with my Saturn placement for personal growth?'
    """)
    
    # Question input
    question = st.text_area("Ask your astrology question:", height=100)
    
    if st.button("🔮 Get AI Interpretation", type="primary"):
        if question.strip():
            with st.spinner("🤖 Generating AI interpretation..."):
                interpretation = interpreter.get_ai_interpretation(kundali_data, question)
            
            st.markdown("## 🌟 AI ASTROLOGICAL INTERPRETATION")
            st.markdown(interpretation)
        else:
            st.warning("Please enter a question.")

def basic_astrology_reading_web():
    """Perform basic astrology reading web interface"""
    
    st.markdown("## 🌟 Basic Zodiac & Horoscope")
    
    # Date input with extended year range
    current_year = datetime.date.today().year
    birth_date = st.date_input(
        "Enter your birth date:",
        min_value=datetime.date(1900, 1, 1),
        max_value=datetime.date(current_year, 12, 31),
        value=datetime.date(1990, 6, 15)
    )
    
    if birth_date:
        zodiac_sign = get_zodiac_sign(birth_date)
        
        if zodiac_sign:
            st.success(f"🎯 Your Zodiac Sign: **{zodiac_sign}**")
            
            # Display traits
            st.markdown(f"**✨ Your Traits:** {zodiac_traits[zodiac_sign]}")
            
            # Generate horoscope
            horoscope = generate_horoscope(zodiac_sign)
            st.markdown(f"**🔮 Your Daily Horoscope:**\n\n*\"{horoscope}\"*")
            
            # Additional info
            col1, col2, col3 = st.columns(3)
            
            with col1:
                today = datetime.date.today()
                age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
                st.metric("📊 Age", f"{age} years")
            
            with col2:
                lucky_number = random.randint(1, 100)
                st.metric("🍀 Lucky Number", lucky_number)
            
            with col3:
                numerology_number = calculate_numerology(birth_date)
                st.metric("🔢 Life Path Number", numerology_number)
            
            # Compatibility
            compatible_signs = compatibility_matrix.get(zodiac_sign, [])
            st.markdown(f"**💕 Your Best Matches:** {', '.join(compatible_signs)}")
            
            # Birth stone
            birth_stone = get_birth_stone(birth_date.month)
            st.markdown(f"**💎 Your Birth Stone:** {birth_stone}")
        else:
            st.error("Sorry, I couldn't determine your zodiac sign. Please check your birth date.")

def compatibility_checker_web():
    """Check compatibility between two zodiac signs web interface"""
    
    st.markdown("## 💕 Zodiac Compatibility Checker")
    
    col1, col2 = st.columns(2)
    
    with col1:
        sign1 = st.selectbox("Select first zodiac sign:", list(zodiac_signs.keys()), key="sign1")
    
    with col2:
        sign2 = st.selectbox("Select second zodiac sign:", list(zodiac_signs.keys()), key="sign2")
    
    if st.button("🔮 Check Compatibility", type="primary"):
        compatibility = get_compatibility(sign1, sign2)
        
        st.markdown("## 💫 Compatibility Analysis")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"**Sign 1:** {sign1}")
            st.markdown(f"*{zodiac_traits[sign1]}*")
        
        with col2:
            st.markdown(f"**Sign 2:** {sign2}")
            st.markdown(f"*{zodiac_traits[sign2]}*")
        
        with col3:
            st.success(f"**Result:** {compatibility}")

def daily_crystal_reading_web():
    """Generate a daily crystal recommendation web interface"""
    
    st.markdown("## 💎 Daily Crystal Recommendation")
    
    crystals = [
        "Clear Quartz - Amplifies energy and intentions",
        "Amethyst - Promotes peace and spiritual growth",
        "Rose Quartz - Opens the heart to love and healing",
        "Citrine - Attracts abundance and positive energy",
        "Black Tourmaline - Protects against negative energy",
        "Lapis Lazuli - Enhances wisdom and communication",
        "Green Aventurine - Brings luck and prosperity",
        "Selenite - Clears energy and promotes clarity",
        "Carnelian - Boosts creativity and motivation",
        "Moonstone - Connects with intuition and emotions"
    ]
    
    tips = [
        "Hold it in your hand during meditation",
        "Place it under your pillow for peaceful sleep",
        "Carry it in your pocket for protection",
        "Place it on your desk for focus and clarity",
        "Use it during your morning routine for positive energy"
    ]
    
    if st.button("🔮 Get Crystal of the Day", type="primary"):
        crystal = random.choice(crystals)
        tip = random.choice(tips)
        
        st.markdown("## 🔮 Your Crystal of the Day")
        st.success(f"**💎 {crystal}**")
        st.info(f"**💡 Tip:** {tip}")

def generate_horoscope(zodiac_sign):
    """Generate a personalized horoscope for the zodiac sign"""
    horoscopes = {
        "Aries": [
            "Your fiery energy will help you overcome any obstacles today. Take bold action!",
            "Leadership opportunities are coming your way. Trust your instincts and lead with confidence.",
            "Your competitive spirit will drive you to success in challenging situations."
        ],
        "Taurus": [
            "Your patience and determination will be rewarded today. Stay focused on your goals.",
            "Financial opportunities may arise. Trust your practical judgment.",
            "Your love for beauty and comfort will bring you joy and relaxation."
        ],
        "Gemini": [
            "Your communication skills will shine today. Share your ideas with others.",
            "New connections and conversations will bring exciting opportunities.",
            "Your curiosity will lead you to discover something fascinating."
        ],
        "Cancer": [
            "Your intuition is strong today. Trust your gut feelings about important decisions.",
            "Family and home matters will bring you happiness and fulfillment.",
            "Your caring nature will be appreciated by those around you."
        ],
        "Leo": [
            "Your natural charisma will attract positive attention today. Shine bright!",
            "Creative projects will flourish under your passionate leadership.",
            "Your generosity will be returned to you in unexpected ways."
        ],
        "Virgo": [
            "Your attention to detail will help you excel in your work today.",
            "Organizing and planning will bring you satisfaction and success.",
            "Your practical advice will be valuable to friends and colleagues."
        ],
        "Libra": [
            "Your diplomatic skills will help resolve conflicts and bring harmony.",
            "Partnerships and relationships will be highlighted in positive ways.",
            "Your sense of justice will guide you to make fair decisions."
        ],
        "Scorpio": [
            "Your deep intuition will reveal hidden truths and opportunities.",
            "Your determination will help you achieve your most challenging goals.",
            "Your magnetic personality will draw people to you today."
        ],
        "Sagittarius": [
            "Your adventurous spirit will lead you to exciting new experiences.",
            "Learning and expanding your horizons will bring you joy.",
            "Your optimism will inspire others and attract good fortune."
        ],
        "Capricorn": [
            "Your disciplined approach will help you achieve long-term success.",
            "Career opportunities may arise. Trust your professional judgment.",
            "Your responsible nature will earn you respect and recognition."
        ],
        "Aquarius": [
            "Your innovative ideas will inspire others and create positive change.",
            "Your humanitarian nature will bring you meaningful connections.",
            "Your unique perspective will help solve complex problems."
        ],
        "Pisces": [
            "Your artistic talents will flourish today. Express your creativity freely.",
            "Your compassion will bring comfort to those in need.",
            "Your spiritual connection will guide you to inner peace and wisdom."
        ]
    }
    
    return random.choice(horoscopes.get(zodiac_sign, ["Today is a day for new beginnings and positive energy!"]))

def get_compatibility(sign1, sign2):
    """Get compatibility between two zodiac signs"""
    if sign1 in compatibility_matrix and sign2 in compatibility_matrix[sign1]:
        return "High Compatibility! 🌟"
    elif sign1 == sign2:
        return "Same Sign - Deep Understanding! 💫"
    else:
        return "Moderate Compatibility - Growth Opportunity! 🌱"

def calculate_numerology(birth_date):
    """Calculate numerology based on birth date"""
    date_str = birth_date.strftime("%Y%m%d")
    total = sum(int(digit) for digit in date_str)
    
    while total > 9 and total not in [11, 22, 33]:
        total = sum(int(digit) for digit in str(total))
    
    return total

def get_birth_stone(birth_month):
    """Get birth stone for the month"""
    birth_stones = {
        1: "Garnet - Symbolizes protection and strength",
        2: "Amethyst - Promotes peace and balance",
        3: "Aquamarine - Enhances communication and courage",
        4: "Diamond - Represents love and clarity",
        5: "Emerald - Brings wisdom and growth",
        6: "Pearl - Symbolizes purity and innocence",
        7: "Ruby - Enhances passion and energy",
        8: "Peridot - Promotes healing and abundance",
        9: "Sapphire - Brings wisdom and truth",
        10: "Opal - Enhances creativity and imagination",
        11: "Topaz - Promotes strength and intelligence",
        12: "Turquoise - Brings good fortune and protection"
    }
    return birth_stones.get(birth_month, "A special stone for your unique energy!")

def main():
    # Main header
    st.markdown('<h1 class="main-header">🌟 ASTROLOGY APP - AI POWERED 🌟</h1>', unsafe_allow_html=True)
    
    # Sidebar for navigation
    st.sidebar.markdown("## 🔮 Navigation")
    
    # User name input
    user_name = st.sidebar.text_input("What's your name?", value=st.session_state.user_name)
    if user_name:
        st.session_state.user_name = user_name
    
    st.sidebar.markdown(f"**Hello, {st.session_state.user_name}!** ✨")
    
    # Main menu
    option = st.sidebar.selectbox(
        "Choose an option:",
        [
            "🌟 Basic Zodiac Reading & Daily Horoscope",
            "💕 Zodiac Compatibility Checker", 
            "💎 Daily Crystal Recommendation",
            "🔮 All-in-One Reading (Complete Profile)",
            "🕉️ Generate Kundali (Birth Chart)",
            "🤖 AI Astrology Consultation (Ask Questions)"
        ]
    )
    
    # Handle different options
    if option == "🌟 Basic Zodiac Reading & Daily Horoscope":
        basic_astrology_reading_web()
        
    elif option == "💕 Zodiac Compatibility Checker":
        compatibility_checker_web()
        
    elif option == "💎 Daily Crystal Recommendation":
        daily_crystal_reading_web()
        
    elif option == "🔮 All-in-One Reading (Complete Profile)":
        st.markdown("## 🔮 COMPLETE ASTROLOGICAL PROFILE")
        
        # Get birth date for complete profile with extended year range
        current_year = datetime.date.today().year
        birth_date = st.date_input(
            "Enter your birth date for complete profile:",
            min_value=datetime.date(1900, 1, 1),
            max_value=datetime.date(current_year, 12, 31),
            value=datetime.date(1990, 6, 15)
        )
        
        if birth_date:
            zodiac_sign = get_zodiac_sign(birth_date)
            if zodiac_sign:
                st.success(f"🎯 Your Zodiac Sign: **{zodiac_sign}**")
                st.markdown(f"**✨ Your Traits:** {zodiac_traits[zodiac_sign]}")
                
                # Horoscope
                horoscope = generate_horoscope(zodiac_sign)
                st.markdown(f"**🔮 Your Daily Horoscope:**\n\n*\"{horoscope}\"*")
                
                # Crystal recommendation
                crystals = [
                    "Clear Quartz - Amplifies energy and intentions",
                    "Amethyst - Promotes peace and spiritual growth",
                    "Rose Quartz - Opens the heart to love and healing",
                    "Citrine - Attracts abundance and positive energy",
                    "Black Tourmaline - Protects against negative energy",
                    "Lapis Lazuli - Enhances wisdom and communication",
                    "Green Aventurine - Brings luck and prosperity",
                    "Selenite - Clears energy and promotes clarity",
                    "Carnelian - Boosts creativity and motivation",
                    "Moonstone - Connects with intuition and emotions"
                ]
                crystal = random.choice(crystals)
                st.markdown(f"**💎 Your Crystal of the Day:** {crystal}")
                
                # Additional insights
                st.markdown("### 💫 Additional Insights:")
                st.markdown("""
                - Your energy is aligned with the current moon phase
                - Mercury retrograde periods may affect your communication
                - Venus transits influence your relationships and creativity
                - Mars energy supports your actions and courage
                """)
        
    elif option == "🕉️ Generate Kundali (Birth Chart)":
        st.markdown("## 🕉️ KUNDALI GENERATION")
        
        # Birth details form
        st.markdown("### 📝 Enter Your Birth Details")
        
        col1, col2 = st.columns(2)
        
        with col1:
            current_year = datetime.date.today().year
            year = st.number_input("Birth Year", min_value=1900, max_value=current_year, value=1990)
            month = st.number_input("Birth Month", min_value=1, max_value=12, value=6)
            day = st.number_input("Birth Day", min_value=1, max_value=31, value=15)
        
        with col2:
            hour = st.number_input("Birth Hour (0-23)", min_value=0, max_value=23, value=14)
            minute = st.number_input("Birth Minute (0-59)", min_value=0, max_value=59, value=30)
        
        # Location input
        st.markdown("### 📍 Birth Location")
        col1, col2 = st.columns(2)
        
        with col1:
            latitude = st.number_input("Latitude (e.g., 28.6139 for Delhi)", value=28.6139, format="%.4f")
        
        with col2:
            longitude = st.number_input("Longitude (e.g., 77.2090 for Delhi)", value=77.2090, format="%.4f")
        
        if st.button("🔮 Generate Kundali", type="primary"):
            birth_data = {
                'year': year, 'month': month, 'day': day,
                'hour': hour, 'minute': minute,
                'latitude': latitude, 'longitude': longitude
            }
            
            kundali_data = calculate_kundali(birth_data)
            st.session_state.current_kundali = kundali_data
            
            display_kundali_web(kundali_data)
            
    elif option == "🤖 AI Astrology Consultation (Ask Questions)":
        if st.session_state.current_kundali is None:
            st.warning("⚠️ You need to generate your Kundali first (option 5).")
            st.info("Please go to '🕉️ Generate Kundali (Birth Chart)' to create your birth chart first.")
        else:
            gemini_astrology_consultation_web(st.session_state.current_kundali)

if __name__ == "__main__":
    main() 