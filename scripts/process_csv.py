import csv
import pandas as pd
import numpy as np

# def read_csv():
#     rows = []
#     with open("scripts/dummy_data.csv", 'r') as file:
#         csvreader = csv.reader(file)
#         header = next(csvreader)
#         for row in csvreader:
#             rows.append(row)
#     print(header)
#     print(rows[-1])

"""
TODO:
get unique student
find intake year + sem for commencement date (?) general studies and CS course are DIFFERENT. 
has graduated default false? <- this is where process course credit points?
populate with above data

populate course (need faculty?)

populate unit (default name and code just put same or sth)

populate enrolment
NOTE:
general studies commencement date might be different! (Look at Dan Peake)
"""


def get_unique_student(df):
    df = df[['Person ID', 'TITLE', 'Surname',
             'Given names', 'COMMENCEMENT_DT']].drop_duplicates()
    df['name'] = df.Surname + ' ' + df['Given names']
    return df[['Person ID', 'name', 'COMMENCEMENT_DT']].values.tolist()


def run():
    df = pd.read_csv('scripts/dummy_data.csv')
    x = get_unique_student(df)
    print(x)

    a = [[38866542, 'Michael Watson'], [41877053, 'Alison Ogden'], [41905875, 'Alan Hemmings'], [43199398, 'Owen Quinn'], [44678853, 'Jan Greene'], [44716329, 'Hannah Gibson'], [44883104, 'Blake Ferguson'], [45416518, 'Michael Miller'], [45416860, 'Cameron Berry'], [45629317, 'Alexander Morgan'], [45723445, 'Harry Ball'], [45789683, 'Richard Payne'], [45888033, 'Brandon Poole'], [46174698, 'Anna Bond'], [46224614, 'Charles Poole'], [46335201, 'Michael Stewart'], [46349895, 'Neil Arnold'], [46352732, 'Sam Kerr'], [46360595, 'Carl Rees'], [46360789, 'Natalie Walsh'], [46381783, 'Audrey Lee'], [46426312, 'Stewart Ferguson'], [46438074, 'Joseph Slater'], [46504890, 'Jacob Black'], [46547640, 'Joe Walker'], [46599109,
                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                         'Pippa Smith'], [46657527, 'Madeleine McGrath'], [46673603, 'Blake Cameron'], [46697634, 'Adam Mathis'], [46722904, 'Carolyn Langdon'], [46809483, 'Stewart MacLeod'], [47087904, 'Joan Mackenzie'], [47098345, 'Jason Welch'], [47178093, 'James Lawrence'], [47226912, 'Adrian Mathis'], [47278386, 'Simon Buckland'], [47364600, 'Wanda Peters'], [47391017, 'Eric Buckland'], [47409007, 'Anthony Hart'], [47413407, 'Heather Mackenzie'], [47421072, 'Sebastian Taylor'], [47430156, 'Jennifer Graham'], [47437093, 'Frank Davies'], [47443705, 'Kevin Marshall'], [47480036, 'Ava Berry'], [47500235, 'Dan Peake'], [47560556, 'Angela Brown'], [48260620, 'Brandon Turner'], [48279625, 'Michael MacLeod'], [48656966, 'Lillian Davies']]
    print(len(a))
    print(len(x))
