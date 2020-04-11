import pymysql

def get_connection():
    return pymysql.connect(
			host = "localhost",
			user="root",
			passwd="admin1234",
			database="latihan"
		)