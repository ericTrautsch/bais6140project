import pandas as pd

def rat_sightings():
    df = pd.read_csv(
        './data/Rat_Sightings_20231112.csv', dtype={20: str}
    )
    df = df[df['Borough'] != 'Unspecified']
    df.dropna(subset=['Created Date', 'Longitude', 'Latitude', 'Complaint Type', 'Borough', 'Community Board'], inplace=True)
    return df

def resurant_inspections():
    df = pd.read_csv('./data/DOHMH_New_York_City_Restaurant_Inspection_Results_20231112.csv')
    # Convert 'Community Board' from float to string
    df['Community Board'] = df['Community Board'].astype(str)

    df['Community Board'] = df['Community Board'].str.replace('.0', '')
    df['Community Board'] = df['Community Board'].str[1:]
    df['BORO'] = df['BORO'].str.upper()

    # Concatenate 'BORO' and 'Community Board' into a new column 'CommunityBoardRevised'
    df['Community Board'] = df['Community Board'] + ' ' + df['BORO']
    # Prepare your data - ensure latitude and longitude are numerical
    df['Latitude'] = pd.to_numeric(df['Latitude'], errors='coerce')
    df['Longitude'] = pd.to_numeric(df['Longitude'], errors='coerce')
    df = df[df['CRITICAL FLAG'] == 'Critical']

    
    df.dropna(subset=['Latitude', 'Longitude'], inplace=True)

    return df

if __name__ == '__main__':
    print((resurant_inspections()))