import mysql.connector
import configparser



config = configparser.ConfigParser()
config.read('conf.ini')

def sql(*args):

	conn = mysql.connector.connect(host='{}'.format(config['SERVER']['url']),database='TDC')
	cursor = conn.cursor()

	cursor.execute(*args)


	try: #Fonction SELECT
		
		out = cursor.fetchall()

	except: #Fonction INSERT

		out = None

	conn.commit()
	cursor.close()
	conn.close()

	return out


#data = ['2020-11-21', 'Elie']
#cmd = "SELECT * from HEURES WHERE DATE=%s AND NOM=%s"

#data=['+33667936781','Tom']
#cmd="SELECT * FROM HUMAINS WHERE TEL = %s OR PRENOM = %s"	

#print(sql(cmd, data))