import pandas as pd

def rat_sightings():
    df = pd.read_csv(
        './data/Rat_Sightings_20231112.csv', dtype={20: str}
    )
    df.dropna(subset=['Created Date', 'Longitude', 'Latitude'], inplace=True)
    return df

if __name__ == '__main__':
    print(rat_sightings())