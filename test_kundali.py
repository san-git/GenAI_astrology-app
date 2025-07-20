#!/usr/bin/env python3
# Simple Kundali Test Script

import datetime
import ephem
import math

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

def test_kundali():
    print("🕉️ KUNDALI TEST - Using Sample Data")
    print("="*50)
    
    # Sample birth data (you can change these)
    birth_data = {
        'year': 1990,
        'month': 6,
        'day': 15,
        'hour': 14,  # 2 PM
        'minute': 30,
        'latitude': 28.6139,  # Delhi
        'longitude': 77.2090
    }
    
    print(f"📅 Sample Birth: {birth_data['day']}/{birth_data['month']}/{birth_data['year']}")
    print(f"⏰ Time: {birth_data['hour']:02d}:{birth_data['minute']:02d}")
    print(f"📍 Location: Delhi (Lat: {birth_data['latitude']}, Lon: {birth_data['longitude']})")
    print("\n🔮 Calculating Kundali...")
    
    try:
        # Create observer
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
        
        # Display results
        print("\n🌟 KUNDALI RESULTS:")
        print("-" * 50)
        print(f"🌅 Ascendant (Lagna): {ascendant_sign}")
        print("\n🪐 Planetary Positions:")
        print(f"{'Planet':<10} {'Sign':<12} {'House':<6} {'Longitude':<10}")
        print("-" * 50)
        
        for planet_name, data in planets_data.items():
            print(f"{planet_name:<10} {data['sign']:<12} {data['house']:<6} {data['longitude']:.2f}°")
        
        print("\n✅ Kundali calculation successful!")
        
    except Exception as e:
        print(f"❌ Error calculating Kundali: {e}")
        print("This might be due to:")
        print("- Invalid date/time")
        print("- Network issues (ephem needs to download data)")
        print("- Missing ephem library")

if __name__ == "__main__":
    test_kundali() 