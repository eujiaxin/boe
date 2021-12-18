import pandas as pd
import numpy as np

df = pd.read_csv("C:\\Users\\fabia\\github\\boe\\scripts\\dummy_data.csv")
df.columns = df.columns.str.upper()
df["COMMENCEMENT_DT"] = pd.to_datetime(df["COMMENCEMENT_DT"])
df.columns

df.groupby(["COURSE_CD", "C_VER"])["UNIT_CD"].apply(list).reset_index(name='new').to_dict("records")
