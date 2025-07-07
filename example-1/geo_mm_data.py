from mm_geo_coder import MMGeoCoder

# Test with a place name from the CSV file
geo_coder = MMGeoCoder("ပါလှဲ့ (အထက်)")   
location = geo_coder.get_geolocation()
print(f"Geocoding result for 'ပါလှဲ့ (အထက်)': {location}")
