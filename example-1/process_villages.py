import pandas as pd
from mm_geo_coder import MMGeoCoder
import time

def process_villages():
    """
    Read the CSV file, process each village name through MMGeoCoder,
    and save results with latitude and longitude to a new CSV file.
    """
    
    # Read the original CSV file
    df = pd.read_csv('data_to_check.csv')
    
    # Initialize lists to store results
    latitudes = []
    longitudes = []
    
    # Process each village name
    total_villages = len(df)
    
    for index, row in df.iterrows():
        village_name = row['ကျေးရွာအုပ်စု']
        print(f"Processing {index + 1}/{total_villages}: {village_name}")
        
        try:
            # Create MMGeoCoder instance and get location
            geo_coder = MMGeoCoder(village_name)
            location = geo_coder.get_geolocation()
            
            # Extract latitude and longitude
            if location and isinstance(location, dict):
                latitude = location.get('latitude', '')
                longitude = location.get('longitude', '')
            else:
                latitude = ''
                longitude = ''
                
        except Exception as e:
            print(f"Error processing {village_name}: {e}")
            latitude = ''
            longitude = ''
        
        latitudes.append(latitude)
        longitudes.append(longitude)
        
        # Add a small delay to avoid overwhelming the geocoding service
        time.sleep(0.5)
    
    # Add latitude and longitude columns to the dataframe
    df['latitude'] = latitudes
    df['longitude'] = longitudes
    
    # Save the results to a new CSV file
    output_filename = 'villages_with_coordinates.csv'
    df.to_csv(output_filename, index=False, encoding='utf-8')
    
    print(f"\nProcessing complete! Results saved to {output_filename}")
    print(f"Total villages processed: {total_villages}")
    
    # Print summary
    successful_geocoding = sum(1 for lat, lon in zip(latitudes, longitudes) if lat and lon)
    print(f"Successfully geocoded: {successful_geocoding}/{total_villages}")

if __name__ == "__main__":
    process_villages() 