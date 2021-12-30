import pandas as pd


def run():
    with open('scripts\dummy_data.csv', 'r') as file:
        df = pd.read_csv(file)
        df = df[df['COURSE_CD'] == 'C2001']
        print(df.to_markdown())
        df.to_csv('only_c2001_dummy.csv', index=False)
