from mm_geo_coder import MMGeoCoder
import pandas as pd

def test_geocoding():
    """
    Test the geocoding functionality with a few sample village names
    """
    
    # Read the CSV file to get sample village names
    df = pd.read_csv('data_to_check.csv')
    
    # Test with first 3 village names
    test_villages = df['ကျေးရွာအုပ်စု'].head(3).tolist()
    
    print("Testing geocoding with sample villages:")
    print("-" * 50)
    
    for village in test_villages:
        print(f"\nTesting: {village}")
        try:
            geo_coder = MMGeoCoder(village)
            location = geo_coder.get_geolocation()
            
            if location and isinstance(location, dict):
                latitude = location.get('latitude', '')
                longitude = location.get('longitude', '')
                print(f"  Latitude: {latitude}")
                print(f"  Longitude: {longitude}")
            else:
                print("  No location data found")
                
        except Exception as e:
            print(f"  Error: {e}")

if __name__ == "__main__":
    test_geocoding() 