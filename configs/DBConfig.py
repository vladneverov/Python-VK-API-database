import sys
import mysql.connector
from mysql.connector import errorcode

try:
    db = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="root",
      port="3307",
      database="vkdb"
    )
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Что-то не так с вашим именем пользователя или паролем")
    sys.exit()
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("База данных не существует")
    sys.exit()
  else:
    print(err)
    sys.exit()

cursor = db.cursor()