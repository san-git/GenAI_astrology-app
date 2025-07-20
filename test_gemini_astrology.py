#!/usr/bin/env python3
# Test Gemini AI Astrology Features

import datetime
import ephem
import math
import os

def get_zodiac_from_longitude(longitude):
    """Get zodiac sign from celestial longitude"""
    zodiac_signs = ["Aries", "Taurus", "Gemini", "Cancer", "Leo", "Virgo",
                   "Libra", "Scorpio", "Sagittarius", "Capricorn", "Aquarius", "Pisces"]
    sign_num = int(longitude / 30)
    return zodiac_signs[sign_num % 12]

def calculate_house_position(ascendant_longitude, planet_longitude):
    """Calculate which house a planet is in"""
    diff = (planet_longitude - ascendant_longitude) % 360
    house = int(diff / 30) + 1
    return house if house <= 12 else house - 12

def test_gemini_astrology():
    print("🤖 GEMINI AI ASTROLOGY FEATURE TEST")
    print("="*50)
    
    # Sample birth data
    birth_data = {
        'year': 1990,
        'month': 6,
        'day': 15,
        'hour': 14,
        'minute': 30,
        'latitude': 28.6139,
        'longitude': 77.2090
    }
    
    print(f"📅 Sample Birth: {birth_data['day']}/{birth_data['month']}/{birth_data['year']}")
    print(f"⏰ Time: {birth_data['hour']:02d}:{birth_data['minute']:02d}")
    print(f"📍 Location: Delhi")
    
    # Calculate Kundali
    observer = ephem.Observer()
    observer.lat = str(birth_data['latitude'])
    observer.lon = str(birth_data['longitude'])
    observer.date = datetime.datetime(
        birth_data['year'], birth_data['month'], birth_data['day'],
        birth_data['hour'], birth_data['minute']
    )
    
    # Calculate planetary positions
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
            'sign': get_zodiac_from_longitude(longitude)
        }
    
    # Calculate Ascendant
    ascendant_longitude = math.degrees(observer.radec_of(0, 0)[0])
    ascendant_sign = get_zodiac_from_longitude(ascendant_longitude)
    
    # Calculate houses
    for planet_name in planets_data:
        house = calculate_house_position(ascendant_longitude, planets_data[planet_name]['longitude'])
        planets_data[planet_name]['house'] = house
    
    kundali_data = {
        'planets': planets_data,
        'ascendant': {
            'longitude': ascendant_longitude,
            'sign': ascendant_sign
        },
        'birth_data': birth_data
    }
    
    print(f"\n🌅 Ascendant: {ascendant_sign}")
    print("\n🪐 Planetary Positions:")
    for planet, data in planets_data.items():
        print(f"  {planet}: {data['sign']} (House {data['house']})")
    
    # Test Gemini AI interpretation
    print("\n" + "="*50)
    print("🤖 GEMINI AI INTERPRETATION TEST")
    print("="*50)
    
    # Check if Google API key is available
    api_key = os.getenv('GOOGLE_API_KEY')
    if api_key:
        print("✅ Google API key found - Gemini AI features available!")
        print("💡 You can now ask questions like:")
        print("   • 'What does my Mars in Gemini placement mean for my career?'")
        print("   • 'How do my planetary positions affect my relationships?'")
        print("   • 'Give me insights about my past, present, and future'")
        print("   • 'What does my Jupiter in the 4th house indicate?'")
    else:
        print("⚠️  Google API key not found")
        print("💡 To enable Gemini AI features, set your Google API key:")
        print("   export GOOGLE_API_KEY='your-api-key-here'")
        print("   Or run: GOOGLE_API_KEY='your-key' python3 astrology_app_gemini.py")
    
    print("\n🌟 Sample Questions You Can Ask Gemini:")
    print("1. 'Summarize my astrological profile'")
    print("2. 'What does my Mars in Gemini placement mean for my career drive?'")
    print("3. 'How do my planetary positions affect my relationships?'")
    print("4. 'What are my strengths and challenges based on my chart?'")
    print("5. 'Give me insights about my past, present, and future'")
    print("6. 'What does my Jupiter in the 4th house indicate?'")
    print("7. 'How can I work with my Saturn placement for personal growth?'")
    print("8. 'What career paths would suit my planetary configuration?'")
    print("9. 'How do my planetary aspects influence my communication style?'")
    print("10. 'What spiritual practices would benefit me based on my chart?'")
    
    print("\n🎯 To use Gemini AI features:")
    print("1. Run: python3 astrology_app_gemini.py")
    print("2. Choose option 5 to generate your Kundali")
    print("3. Choose option 6 for Gemini AI consultation")
    print("4. Ask any astrology question!")
    
    print("\n🔑 To get your Google API key:")
    print("1. Go to: https://makersuite.google.com/app/apikey")
    print("2. Create a new API key")
    print("3. Set it as environment variable: export GOOGLE_API_KEY='your-key'")

if __name__ == "__main__":
    test_gemini_astrology() 