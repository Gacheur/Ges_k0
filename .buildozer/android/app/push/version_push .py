import datetime
import mysql.connector

import androidhelper

def sql(*args):

	conn = mysql.connector.connect(host='tdcndd.site',database='TDC')
	cursor = conn.cursor()

	cursor.execute(*args)


	out = cursor.fetchall()


	return out


ls_humains = sql("SELECT PRENOM, TEL FROM HUMAINS")
print(ls_humains)

for i in ls_humains:

	text = "Message Automatique: Une nouvelle version de Ges_k0 est disponible.\n Merci de télécharger et installer la nouvelle image sur le site: http://tdcndd.site"
	print(i[1], text)
	androidhelper.Android().smsSend(num, text)
