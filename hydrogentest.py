import pandas as pd
import numpy as np

df = pd.read_csv("C:\\Users\\fabia\\github\\boe\\scripts\\dummy_data.csv")
df.columns = df.columns.str.upper()
df["COMMENCEMENT_DT"] = pd.to_datetime(df["COMMENCEMENT_DT"])
df.columns

def get_unique_course(df):
    course_identifier = ['COURSE_CD', 'C_VER', 'CRS_TITLE']
    aux = df[course_identifier].drop_duplicates()
    return list(map(tuple, aux.values))
course_identifier = ['COURSE_CD', 'C_VER']
df["new"] = df["COURSE_CD"] + df["C_VER"].astype(str)
df["new"].unique()
# df.groupby(["COURSE_CD", "C_VER"])["UNIT_CD"].apply(list).reset_index(name='new').to_dict("records")
get_unique_course(df)
