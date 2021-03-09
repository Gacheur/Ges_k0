import mysql.connector
import configparser



config = configparser.ConfigParser()
config.read('conf.ini')


class DatabaseCom():

	def __init__(self, *args):
		#conn = mysql.connector.connect(host='{}'.format(config['SERVER']['url']),database='TDC')
		self.conn = mysql.connector.connect(host='tdc.ovh',database='TDC')
		self.cursor = self.conn.cursor()


	def select_insert_delete(self, *args):
		
		self.cursor.execute(*args)

		try: #Fonction SELECT
			
			out = self.cursor.fetchall()

		except: #Fonction INSERT DELETE

			out = '+ - OK'

		self.conn.commit()
		#cursor.close()
		#conn.close()

		return out