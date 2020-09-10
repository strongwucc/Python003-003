import pandas as pd
import pymysql

mysql_conn = pymysql.connect(
    host='localhost',
    port=3306,
    user='root',
    password='123456',
    db='pandas',
    charset='utf8mb4'
)

# 1. SELECT * FROM data;
sql = 'SELECT * FROM data'
df = pd.read_sql(sql, mysql_conn)
# print(df)

# 2. SELECT * FROM data LIMIT 10;
df2 = df.loc[0: 9]
# print(df2)


# 3. SELECT id FROM data;  //id 是 data 表的特定一列
df3 = df['id']
# print(df3)

# 4. SELECT COUNT(id) FROM data;
df4 = df['id'].count()
# print(df4)

# 5. SELECT * FROM data WHERE id<1000 AND age>30;
df5 = df[(df['id'] < 1000) & (df['age'] > 30)]
# print(df5)


sql = 'SELECT * FROM table1'
df = pd.read_sql(sql, mysql_conn)

# 6. SELECT id,COUNT(DISTINCT order_id) FROM table1 GROUP BY id;
df6 = df.groupby(['id']).agg({'order_id': 'nunique'})
# print(df6)

# 7. SELECT * FROM table1 t1 INNER JOIN table2 t2 ON t1.id = t2.id;
sql1 = 'SELECT * FROM table1'
sql2 = 'SELECT * FROM table2'

t1 = pd.read_sql(sql1, mysql_conn)
t2 = pd.read_sql(sql2, mysql_conn)

df7 = pd.merge(t1, t2, on='id')
# print(df7)

# 8. SELECT * FROM table1 UNION SELECT * FROM table2;
df8 = pd.concat([t1, t2])
# print(df8)

# 9. DELETE FROM table1 WHERE id=10;
t9 = t1[ t1['id'] != 10 ]
# print(t9)

# 10. ALTER TABLE table1 DROP COLUMN column_name;
t10 = t1.drop('order_time', axis=1)
# print(t10)

mysql_conn.close()