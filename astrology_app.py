# This is a comment. Comments start with # and are ignored by Python.
# They are for humans to understand the code!

import datetime
import random
import ephem
import math
import os
import json
from typing import Dict, List, Optional

print("Hello, aspiring astrologer!")
print("Let's build an astrology app together.")

# Variables are like containers for storing data.
your_name = "User" # You can change "User" to your actual name if you like!
print(f"Welcome, {your_name}!")

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
    "Sun": {"sanskrit": "Surya", "element": "Fire", "nature": "Benefic", "significance": "Soul, father, authority, ego"},
    "Moon": {"sanskrit": "Chandra", "element": "Water", "nature": "Benefic", "significance": "Mind, mother, emotions, intuition"},
    "Mars": {"sanskrit": "Mangal", "element": "Fire", "nature": "Malefic", "significance": "Energy, courage, brother, aggression"},
    "Mercury": {"sanskrit": "Budh", "element": "Earth", "nature": "Neutral", "significance": "Communication, intelligence, business"},
    "Jupiter": {"sanskrit": "Guru", "element": "Ether", "nature": "Benefic", "significance": "Wisdom, teacher, children, spirituality"},
    "Venus": {"sanskrit": "Shukra", "element": "Water", "nature": "Benefic", "significance": "Love, beauty, relationships, arts"},
    "Saturn": {"sanskrit": "Shani", "element": "Air", "nature": "Malefic", "significance": "Discipline, karma, obstacles, lessons"}
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

class AIAstrologyInterpreter:
    """AI-powered astrology interpreter using LLM"""
    
    def __init__(self):
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            print("⚠️  OpenAI API key not found. Set OPENAI_API_KEY environment variable for AI features.")
            print("   You can still use all other features without AI.")
    
    def create_astrology_prompt(self, kundali_data: Dict, question: str) -> str:
        """Create a detailed prompt for astrology interpretation"""
        
        # Format planetary data
        planets_info = []
        for planet, data in kundali_data['planets'].items():
            vedic_info = vedic_planets.get(planet, {})
            sign_info = vedic_rashis.get(data['sign'], {})
            house_info = house_significations.get(data['house'], "")
            
            planet_desc = f"{planet} ({vedic_info.get('sanskrit', '')}) in {data['sign']} ({sign_info.get('sanskrit', '')}) in House {data['house']} ({house_info})"
            planets_info.append(planet_desc)
        
        prompt = f"""
You are an expert Vedic astrologer with deep knowledge of both Western and Indian astrology. Analyze the following birth chart (Kundali) and provide insightful, personalized interpretations.

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

Format your response in a clear, structured way with relevant sections and bullet points where appropriate.
"""
        return prompt
    
    def get_ai_interpretation(self, kundali_data: Dict, question: str) -> str:
        """Get AI interpretation for astrology question"""
        
        if not self.api_key:
            return self.get_fallback_interpretation(kundali_data, question)
        
        try:
            import openai
            client = openai.OpenAI(api_key=self.api_key)
            
            prompt = self.create_astrology_prompt(kundali_data, question)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are an expert Vedic astrologer with deep knowledge of both Western and Indian astrology. Provide insightful, personalized interpretations that are practical and supportive."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"⚠️  AI interpretation error: {e}")
            return self.get_fallback_interpretation(kundali_data, question)
    
    def get_fallback_interpretation(self, kundali_data: Dict, question: str) -> str:
        """Provide fallback interpretation without AI"""
        
        sun_sign = kundali_data['planets']['Sun']['sign']
        moon_sign = kundali_data['planets']['Moon']['sign']
        ascendant = kundali_data['ascendant']['sign']
        
        interpretation = f"""
🌟 ASTROLOGICAL INTERPRETATION 🌟

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
        
        interpretation += f"""
💡 RECOMMENDATIONS:
• Focus on developing your {sun_sign} strengths
• Work with your {moon_sign} emotional patterns
• Express your {ascendant} qualities authentically

Note: For more detailed AI-powered interpretations, set your OpenAI API key.
"""
        
        return interpretation

def get_zodiac_sign(birth_date):
    """Determine zodiac sign based on birth date"""
    # Normalize the birth date to year 2000 for comparison
    normalized_date = datetime.date(2000, birth_date.month, birth_date.day)
    
    for sign, (start_date, end_date) in zodiac_signs.items():
        if start_date <= normalized_date <= end_date:
            return sign
    return None

def get_zodiac_from_longitude(longitude):
    """Get zodiac sign from celestial longitude"""
    # Each sign is 30 degrees
    sign_num = int(longitude / 30)
    signs = list(zodiac_signs.keys())
    return signs[sign_num % 12]

def calculate_house_position(ascendant_longitude, planet_longitude):
    """Calculate which house a planet is in"""
    # Calculate the difference from ascendant
    diff = (planet_longitude - ascendant_longitude) % 360
    # Each house is 30 degrees
    house = int(diff / 30) + 1
    return house if house <= 12 else house - 12

def get_birth_details():
    """Get detailed birth information for Kundali"""
    print("\n--- Enter Your Birth Details for Kundali ---")
    
    while True:
        try:
            year = int(input("Birth Year (e.g., 1990): "))
            month = int(input("Birth Month (1-12): "))
            day = int(input("Birth Day (1-31): "))
            hour = int(input("Birth Hour (0-23, e.g., 14 for 2 PM): "))
            minute = int(input("Birth Minute (0-59): "))
            break
        except ValueError:
            print("Please enter valid numbers.")
    
    while True:
        try:
            latitude = float(input("Birth Latitude (e.g., 28.6139 for Delhi): "))
            longitude = float(input("Birth Longitude (e.g., 77.2090 for Delhi): "))
            break
        except ValueError:
            print("Please enter valid coordinates.")
    
    return {
        'year': year, 'month': month, 'day': day,
        'hour': hour, 'minute': minute,
        'latitude': latitude, 'longitude': longitude
    }

def calculate_kundali(birth_data):
    """Calculate Kundali (birth chart) with planetary positions"""
    print("\n🔮 Calculating your Kundali (Birth Chart)...")
    
    # Create observer location
    observer = ephem.Observer()
    observer.lat = str(birth_data['latitude'])
    observer.lon = str(birth_data['longitude'])
    
    # Create datetime object properly
    birth_datetime = datetime.datetime(
        birth_data['year'], 
        birth_data['month'], 
        birth_data['day'],
        birth_data['hour'], 
        birth_data['minute']
    )
    observer.date = birth_datetime
    
    # Calculate planetary positions
    planets_data = {}
    
    # Main planets
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
    
    # Calculate Ascendant (Lagna)
    ascendant_longitude = math.degrees(observer.radec_of(0, 0)[0])
    
    # Calculate houses for each planet
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

def display_kundali(kundali_data):
    """Display the Kundali chart"""
    print("\n" + "="*60)
    print("🌟 YOUR KUNDALI (BIRTH CHART) 🌟")
    print("="*60)
    
    birth = kundali_data['birth_data']
    print(f"📅 Birth Date: {birth['day']}/{birth['month']}/{birth['year']}")
    print(f"⏰ Birth Time: {birth['hour']:02d}:{birth['minute']:02d}")
    print(f"📍 Birth Place: Lat {birth['latitude']:.4f}, Lon {birth['longitude']:.4f}")
    print(f"🌅 Ascendant (Lagna): {kundali_data['ascendant']['sign']}")
    print("-" * 60)
    
    print("\n🪐 PLANETARY POSITIONS:")
    print("-" * 60)
    print(f"{'Planet':<12} {'Sanskrit':<10} {'Sign':<12} {'House':<6} {'Element':<8} {'Nature':<10}")
    print("-" * 60)
    
    for planet_name, data in kundali_data['planets'].items():
        print(f"{planet_name:<12} {data['sanskrit_name']:<10} {data['sign']:<12} {data['house']:<6} {data['element']:<8} {data['nature']:<10}")
    
    print("\n" + "="*60)
    print("📊 HOUSE ANALYSIS:")
    print("-" * 60)
    
    # Group planets by houses
    houses = {}
    for planet_name, data in kundali_data['planets'].items():
        house = data['house']
        if house not in houses:
            houses[house] = []
        houses[house].append(planet_name)
    
    for house_num in range(1, 13):
        planets_in_house = houses.get(house_num, [])
        if planets_in_house:
            print(f"🏠 House {house_num}: {', '.join(planets_in_house)}")
        else:
            print(f"🏠 House {house_num}: Empty")
    
    print("\n" + "="*60)
    print("💫 KUNDALI INSIGHTS:")
    print("-" * 60)
    
    # Basic interpretations
    sun_sign = kundali_data['planets']['Sun']['sign']
    moon_sign = kundali_data['planets']['Moon']['sign']
    ascendant_sign = kundali_data['ascendant']['sign']
    
    print(f"☀️ Sun Sign (Atman): {sun_sign} - {zodiac_traits[sun_sign]}")
    print(f"🌙 Moon Sign (Mind): {moon_sign} - {zodiac_traits[moon_sign]}")
    print(f"🌅 Ascendant (Personality): {ascendant_sign} - {zodiac_traits[ascendant_sign]}")
    
    # Check for planetary combinations (Yogas)
    print(f"\n🔮 Special Combinations:")
    
    # Check for Sun-Moon conjunction
    sun_house = kundali_data['planets']['Sun']['house']
    moon_house = kundali_data['planets']['Moon']['house']
    if sun_house == moon_house:
        print("• Sun-Moon Conjunction: Strong willpower and determination")
    
    # Check for Jupiter in 1st house
    if kundali_data['planets']['Jupiter']['house'] == 1:
        print("• Jupiter in 1st House: Wisdom and spiritual growth")
    
    # Check for Saturn in 1st house
    if kundali_data['planets']['Saturn']['house'] == 1:
        print("• Saturn in 1st House: Discipline and life lessons")
    
    print("="*60)

def ai_astrology_consultation(kundali_data):
    """AI-powered astrology consultation"""
    print("\n" + "="*60)
    print("🤖 AI ASTROLOGY CONSULTATION")
    print("="*60)
    
    interpreter = AIAstrologyInterpreter()
    
    print("\n💭 You can ask questions like:")
    print("• 'Summarize my astrological profile'")
    print("• 'What does my Mars in Gemini placement mean for my career?'")
    print("• 'How do my planetary positions affect my relationships?'")
    print("• 'What are my strengths and challenges based on my chart?'")
    print("• 'Give me insights about my past, present, and future'")
    print("• 'What does my Jupiter in the 4th house indicate?'")
    
    while True:
        print("\n" + "-" * 40)
        question = input("\nAsk your astrology question (or type 'quit' to exit): ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            break
        
        if not question:
            print("Please enter a question.")
            continue
        
        print(f"\n🔮 Analyzing your question: '{question}'")
        print("🤖 Generating AI interpretation...")
        
        interpretation = interpreter.get_ai_interpretation(kundali_data, question)
        
        print("\n" + "="*60)
        print("🌟 AI ASTROLOGICAL INTERPRETATION")
        print("="*60)
        print(interpretation)
        print("="*60)

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
    # Add all digits of the birth date
    date_str = birth_date.strftime("%Y%m%d")
    total = sum(int(digit) for digit in date_str)
    
    # Reduce to single digit (except for master numbers 11, 22, 33)
    while total > 9 and total not in [11, 22, 33]:
        total = sum(int(digit) for digit in str(total))
    
    return total

def get_numerology_meaning(number):
    """Get meaning for numerology number"""
    meanings = {
        1: "Leadership, independence, and originality. You're a natural born leader!",
        2: "Cooperation, diplomacy, and sensitivity. You excel at working with others.",
        3: "Creativity, self-expression, and joy. Your artistic talents shine bright!",
        4: "Stability, organization, and hard work. You build solid foundations.",
        5: "Freedom, adventure, and change. You thrive on new experiences.",
        6: "Nurturing, responsibility, and harmony. You care deeply for others.",
        7: "Spirituality, analysis, and wisdom. You seek deeper meaning in life.",
        8: "Power, achievement, and material success. You're ambitious and driven.",
        9: "Compassion, idealism, and universal love. You're humanitarian at heart.",
        11: "Intuition, inspiration, and spiritual insight. You're highly intuitive!",
        22: "Master builder, practical vision, and great achievements. You can manifest big dreams!",
        33: "Master teacher, healing, and spiritual guidance. You have a special mission to help others."
    }
    return meanings.get(number, "A unique and special number with your own path!")

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

def basic_astrology_reading():
    """Perform basic astrology reading"""
    print("\n--- Basic Zodiac & Horoscope ---")
    
    # Get birth date
    while True:
        try:
            birth_str = input("\nEnter your birth date (MM/DD/YYYY): ")
            birth_date = datetime.datetime.strptime(birth_str, "%m/%d/%Y").date()
            break
        except ValueError:
            print("Please enter a valid date in MM/DD/YYYY format (e.g., 12/25/1990)")
    
    # Determine zodiac sign
    zodiac_sign = get_zodiac_sign(birth_date)
    
    if zodiac_sign:
        print(f"\n🎯 Your Zodiac Sign: {zodiac_sign}")
        print(f"📅 Birth Date: {birth_date.strftime('%B %d, %Y')}")
        print(f"✨ Your Traits: {zodiac_traits[zodiac_sign]}")
        
        # Generate and display horoscope
        print(f"\n🔮 Your Daily Horoscope:")
        print(f"\"{generate_horoscope(zodiac_sign)}\"")
        
        # Calculate age
        today = datetime.date.today()
        age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
        print(f"\n📊 You are {age} years old")
        
        # Lucky number
        lucky_number = random.randint(1, 100)
        print(f"🍀 Your lucky number today: {lucky_number}")
        
        # Numerology
        numerology_number = calculate_numerology(birth_date)
        print(f"🔢 Your Life Path Number: {numerology_number}")
        print(f"📖 Numerology Meaning: {get_numerology_meaning(numerology_number)}")
        
        # Birth stone
        birth_stone = get_birth_stone(birth_date.month)
        print(f"💎 Your Birth Stone: {birth_stone}")
        
        # Compatibility
        print(f"\n💕 Your Best Matches: {', '.join(compatibility_matrix.get(zodiac_sign, []))}")
        
    else:
        print("Sorry, I couldn't determine your zodiac sign. Please check your birth date.")

def compatibility_checker():
    """Check compatibility between two zodiac signs"""
    print("\n--- Zodiac Compatibility Checker ---")
    
    print("\nAvailable zodiac signs:")
    for i, sign in enumerate(zodiac_signs.keys(), 1):
        print(f"{i:2d}. {sign}")
    
    # Get first sign
    while True:
        try:
            choice1 = int(input("\nEnter the number for the first zodiac sign: ")) - 1
            if 0 <= choice1 < len(zodiac_signs):
                sign1 = list(zodiac_signs.keys())[choice1]
                break
            else:
                print("Please enter a valid number.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Get second sign
    while True:
        try:
            choice2 = int(input("Enter the number for the second zodiac sign: ")) - 1
            if 0 <= choice2 < len(zodiac_signs):
                sign2 = list(zodiac_signs.keys())[choice2]
                break
            else:
                print("Please enter a valid number.")
        except ValueError:
            print("Please enter a valid number.")
    
    # Display compatibility
    print(f"\n💫 Compatibility Analysis:")
    print(f"Sign 1: {sign1}")
    print(f"Sign 2: {sign2}")
    print(f"Result: {get_compatibility(sign1, sign2)}")
    
    # Show traits for both signs
    print(f"\n✨ {sign1} Traits: {zodiac_traits[sign1]}")
    print(f"✨ {sign2} Traits: {zodiac_traits[sign2]}")

def daily_crystal_reading():
    """Generate a daily crystal recommendation"""
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
    print(f"\n🔮 Your Crystal of the Day:")
    print(f"💎 {crystal}")
    
    # Crystal usage tip
    tips = [
        "Hold it in your hand during meditation",
        "Place it under your pillow for peaceful sleep",
        "Carry it in your pocket for protection",
        "Place it on your desk for focus and clarity",
        "Use it during your morning routine for positive energy"
    ]
    tip = random.choice(tips)
    print(f"💡 Tip: {tip}")

def main():
    print("\n" + "="*50)
    print("🌟 WELCOME TO YOUR PERSONAL ASTROLOGY APP 🌟")
    print("="*50)
    
    # Get user's name
    name = input("\nWhat's your name? (or press Enter to use 'User'): ").strip()
    if not name:
        name = "User"
    
    print(f"\nHello, {name}! Let's explore the mystical world of astrology!")
    
    # Store Kundali data for AI consultation
    current_kundali = None
    
    while True:
        print("\n" + "="*50)
        print("Choose an option:")
        print("1. 🌟 Basic Zodiac Reading & Daily Horoscope")
        print("2. 💕 Zodiac Compatibility Checker")
        print("3. 💎 Daily Crystal Recommendation")
        print("4. 🔮 All-in-One Reading (Complete Profile)")
        print("5. 🕉️ Generate Kundali (Birth Chart)")
        print("6. 🤖 AI Astrology Consultation (Ask Questions)")
        print("7. 🚪 Exit")
        print("="*50)
        
        choice = input("Enter your choice (1-7): ").strip()
        
        if choice == '1':
            basic_astrology_reading()
            
        elif choice == '2':
            compatibility_checker()
            
        elif choice == '3':
            daily_crystal_reading()
            
        elif choice == '4':
            print("\n" + "="*50)
            print("🔮 COMPLETE ASTROLOGICAL PROFILE")
            print("="*50)
            basic_astrology_reading()
            print("\n" + "-"*30)
            daily_crystal_reading()
            print("\n" + "-"*30)
            print("💫 Additional Insights:")
            print("• Your energy is aligned with the current moon phase")
            print("• Mercury retrograde periods may affect your communication")
            print("• Venus transits influence your relationships and creativity")
            print("• Mars energy supports your actions and courage")
            
        elif choice == '5':
            print("\n" + "="*50)
            print("🕉️ KUNDALI GENERATION")
            print("="*50)
            birth_details = get_birth_details()
            current_kundali = calculate_kundali(birth_details)
            display_kundali(current_kundali)
            
        elif choice == '6':
            if current_kundali is None:
                print("\n⚠️  You need to generate your Kundali first (option 5).")
                print("   This will provide the data needed for AI analysis.")
            else:
                ai_astrology_consultation(current_kundali)
            
        elif choice == '7':
            print("\n" + "="*50)
            print("Thank you for using the Astrology App! 🌟")
            print("May the stars guide your path! ✨")
            print("="*50)
            break
            
        else:
            print("Invalid choice. Please enter a number between 1 and 7.")
        
        # Ask if user wants to continue
        if choice != '7':
            continue_choice = input("\nWould you like to explore more? (y/n): ").strip().lower()
            if continue_choice not in ['y', 'yes']:
                print("\n" + "="*50)
                print("Thank you for using the Astrology App! 🌟")
                print("May the stars guide your path! ✨")
                print("="*50)
                break

if __name__ == "__main__":
    main()