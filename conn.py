import mysql.connector

mysql_config={
    'host': 'localhost',
    'user': 'root',
    'password': 'test',
    'database' : 'mydb'
}

conn = mysql.connector.connect(**mysql_config)
cursor = conn.cursor()

create_table = '''
    CREATE TABLE IF NOT EXISTS mytb (
        id INT AUTO_INCREMENT PRIMARY KEY,
        task_name VARCHAR(70) NOT NULL,
        exec_at TIMESTAMP 
    )
'''

cursor.execute(create_table)

task_name = 'Task Name'
execution_timestamp = '2024-03-08 12:00:00' 

insert_query='INSERT INTO mytb (task_name, exec_at) VALUES (%s, %s)'
data = (task_name, execution_timestamp)

cursor.execute(insert_query,data)

# Retreive Records
select_query= 'SELECT * FROM mytb'
cursor.execute(select_query)
records = cursor.fetchall()

print("Records:")
for record in records:
    rid,rtask, rts = record
    format_timestamp = rts.strftime('%Y-%m-%d %H:%M:%S')
    print(f"ID: {rid}, Task: {rtask}, Execution Time: {format_timestamp}")

cursor.close()    
conn.close()