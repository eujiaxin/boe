import pandas as pd
import numpy as np

df = pd.read_csv("C:\\Users\\fabia\\github\\boe\\scripts\\dummy_data.csv")
df.columns = df.columns.str.upper()
df["COMMENCEMENT_DT"] = pd.to_datetime(df["COMMENCEMENT_DT"])
df.columns

def get_unique_student(df):
    student_identifier = [
        'PERSON ID', 'TITLE',
        'SURNAME', 'GIVEN NAMES', 'COMMENCEMENT_DT', "COURSE_CD", "C_VER"
    ]
    df = df[student_identifier].drop_duplicates()
    df['NAME'] = df['SURNAME'] + ' ' + df['GIVEN NAMES']
    return list(map(tuple, df[['PERSON ID', 'NAME', 'COMMENCEMENT_DT', "COURSE_CD", "C_VER"]].values))

important_fields = ['PERSON ID', 'UNIT_CD',
                        'ACAD_YR', 'MARK', 'GRADE', 'CAL_TYPE', 'COURSE_CD', 'C_VER']
df_records = df[important_fields].drop_duplicates().to_dict('records')
df_records
