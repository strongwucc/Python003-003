# import datetime

# str1 = '11分钟前'
# print(str1[:str1.find('分钟前')])
# now = datetime.datetime.now()
# print(now.strftime("%Y-"))

# six_mini = (now + datetime.timedelta(minutes=-6)).strftime("%Y-%m-%d %H:%M:%S")

# print(now, six_mini)
# in_date = '11-13 20:29'
# dt = datetime.datetime.strptime(in_date, "2020-%m-%d %H:%M")
# print(dt)
import pandas as pd
from sqlalchemy import create_engine
from snownlp import SnowNLP

engine = create_engine(
    f'mysql+pymysql://root:lucienwu0101@localhost:3306/graduation')
sql = 'select * from backend_comment;'
df = pd.read_sql_query(sql, engine)
df_copy = df.copy()

df_copy = df_copy.dropna()
df_copy = df_copy.drop(df_copy[df_copy.content == ''].index)
df_copy = df_copy.drop_duplicates('content')

df_copy['sentiment'] = df_copy['content'].map(lambda x: SnowNLP(x).sentiments)

df_copy.to_sql('backend_comment', engine, if_exists='replace', index=False)
with engine.connect() as con:
    con.execute(
        'ALTER TABLE backend_comment ADD PRIMARY KEY (`id`);')
    con.execute(
        'ALTER TABLE backend_comment CHANGE id id BIGINT NOT NULL AUTO_INCREMENT;')

# print(df_copy)
