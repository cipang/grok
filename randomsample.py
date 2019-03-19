import os
import random

import psycopg2

host = os.environ["HOST"]
user = os.environ["USER"]
password = os.environ["PASS"]
conn = psycopg2.connect(f"dbname=db user={user} host={host} password={password}")
cur = conn.cursor()

cur.execute("SELECT DISTINCT salesordernumber FROM factinternetsales ORDER BY 1;")
sales_order_numbers = [row[0] for row in cur]

to_delete = random.sample(sales_order_numbers, 4048)
for x in to_delete:
    cur.execute("DELETE FROM factinternetsales WHERE salesordernumber = %s", (x,))

conn.commit()
