# pylint: disable=line-too-long
# pylint: disable=unused-argument
import argparse
import pandas as pd

def clean_data(country="PT"):
    """
    Load, clean, filter and save life expectancy data for Portugal. The cleaning process envolves unpivoting the date to long format,
    ensure 'year' is an int, 'value' is a float and clean the errors. 
    """
    df = pd.read_csv(
        '/Users/bia/Desktop/DareData/daredata_foundations/assignments/life_expectancy/data/eu_life_expectancy_raw.tsv', 
        sep='\t'
    )
    df[['unit', 'sex', 'age', 'geo']] = df.iloc[:, 0].str.split(',', expand=True)
    df = df.drop(df.columns[0], axis=1)
    df = df.melt(id_vars=['unit', 'sex', 'age', 'geo'], var_name='year', value_name='value')
    df['year'] = pd.to_numeric(df['year'], errors='coerce')
    df['value'] = df['value'].str.replace('e', '', regex=False)
    df['value'] = pd.to_numeric(df['value'], errors='coerce')
    df.dropna(subset=['value'], inplace=True)
    df = df[df['geo'] == 'PT']
    df.rename(columns={'geo': 'region'}, inplace=True)
    df.to_csv('/Users/bia/Desktop/DareData/daredata_foundations/assignments/life_expectancy/data/pt_life_expectancy.csv', index=False)

if __name__ == "__main__":  # pragma: no cover
    parser = argparse.ArgumentParser()
    parser.add_argument("--country", default="PT", help="Country code to filter the data")
    args = parser.parse_args()
    clean_data(args.country)
    