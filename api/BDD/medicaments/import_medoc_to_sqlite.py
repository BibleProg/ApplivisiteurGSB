import csv
import random
from faker import Faker
from pprint import pprint
import pyodbc
import re

def connexion(db_name):
    
    dir_path = '../'
    db_path  = dir_path + db_name
    cnxn = pyodbc.connect("Driver=SQLite3 ODBC Driver;Database=" + db_path)
    return cnxn

def query(sql, arg=False):
    try:
        cnxn   = connexion('api.db')
        cursor = cnxn.cursor()
    except pyodbc.Error as e:
        exit(f"error : {e}")

    try:
        if arg:
            
            if type(arg) == type(list()):
                cursor.executemany(sql,arg)
            else:
                cursor.execute(sql,*arg)    
        else:
            cursor.execute(sql)
    except pyodbc.Error as e:
        print(f'error with query : \n {sql} \n {arg}')
        cursor.rollback()
        print(f"error : {e}")
        pass

    cnxn.commit()

    try:
        res = cursor.fetchall()

        columns = [column[0] for column in cursor.description]
        results = []
        
        if len(res) > 1:
            for row in res:
                results.append(dict(zip(columns, row)))
        else:
            results = dict(zip(columns, res[0]))
    except pyodbc.ProgrammingError as e:
        results = cursor.rowcount 

    cnxn.close()
    
    return results

fake = Faker('it_IT')

bpm = []
with open('CIS_bdpm.txt', newline='') as f:
    spamreader = csv.reader(f, delimiter='\t')
    for row in spamreader:
        bpm.append(row)
bpm.sort()

compo = []
with open('CIS_COMPO_bdpm.txt', newline='') as f:
    spamreader = csv.reader(f, delimiter='\t')
    for row in spamreader:
        compo.append(row)
compo.sort()

cip = []
with open('CIS_CIP_bdpm.txt', newline='') as f:
    spamreader = csv.reader(f, delimiter='\t')
    for row in spamreader:
        cip.append(row)	
cip.sort()

cpd = []
with open('CIS_CPD_bdpm.txt', newline='') as f:
    spamreader = csv.reader(f, delimiter='\t')
    for row in spamreader:
        cpd.append(row)
cpd.sort() 

print(len(bpm))
print(len(compo))
print(len(cip))
print(len(cpd))	

medoc = []
for i in range(len(bpm)):
    stock = random.randint(20,500)
    effet = fake.text()
    medoc.append({'label' : bpm[i][1], 'compo' : compo[i][3], 'prix' : cip[i][10], 'indic' : cpd[i][1], 'date' : cip[i][5], 'effet' : effet, 'stock' : stock})


for med in medoc:
    label = med['label'].replace("'", "\\'")
    date  = med['date'].replace("'", "\\'")
    compo = med['compo'].replace("'", "\\'")
    effet = med['effet'].replace("'", "\\'")
    indic = med['indic'].replace("'", "\\'")
    prix  = med['prix']
    stock = med['stock']

    sql = f"INSERT INTO Medicaments(Label, Date, Composition, Effets, ContreIndic, Prix, Stock) VALUES ('{label}', '{date}', '{compo}', '{effet}', '{indic}', '{prix}', '{stock}')"
    print(sql)
    query(sql)

