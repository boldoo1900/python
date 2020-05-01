import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np 
from fabric import Connection

mydb = mysql.connector.connect(
  host="localhost",
  user="testuser",
  passwd="123",
  database="testdb"
)

mycursor = mydb.cursor()
mycursor.execute("select count(distinct user_id) as user_id_count, web_id, DATE_FORMAT(timestamp, '%Y-%m-%d') as date\n\
	                from visit_history\n\
                  group by web_id, DATE_FORMAT(timestamp, '%Y-%m-%d');")
myresult = mycursor.fetchall()

mycursor.close();
mydb.close();

df = pd.DataFrame(myresult, columns=['user_id_count', 'web_id', 'date'])

dfPivot = df.pivot_table(index="web_id", columns="date", values="user_id_count", aggfunc=np.sum, fill_value=0)
dfPivot = dfPivot.rename_axis(None, axis=1)
print(dfPivot)

dfPivot.to_csv (r'testPivot.csv', index = True, header=True)
    
conn = Connection("fenrir", user='munkhbold-bayasgalan', connect_kwargs={'password': "Password phrase !!!"})
conn.put('testPivot.csv', remote='/home/local/GENIEE/munkhbold-bayasgalan/')