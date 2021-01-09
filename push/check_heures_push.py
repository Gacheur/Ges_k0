import datetime
import mysql.connector

import androidhelper

def sql(*args):

	conn = mysql.connector.connect(host='tdcndd.site',database='TDC')
	cursor = conn.cursor()

	cursor.execute(*args)


	out = cursor.fetchall()


	return out

year = 2020
week = 50
rtt = True


first_day = datetime.datetime.strptime('{} {} 1'.format(year, week), '%G %V %u').date()
print(first_day)

if rtt == True:
	dates = [first_day + datetime.timedelta(days=d) for d in range(4)]
	print('Vendredi RTT')
	print(dates)
else:
	dates = [first_day + datetime.timedelta(days=d) for d in range(5)]
	print('Vendredi Travaillé')
	print(dates)


ls_humains = sql("SELECT PRENOM, TEL FROM HUMAINS")
print(ls_humains)

ls_heures = sql("SELECT NOM, DATE FROM HEURES WHERE SEMAINE ={}".format(week))
print(ls_heures)

ls_compare= []

for i in ls_humains:
	for j in dates:
		ls_compare.append((i[0],str(j)))

print(ls_compare)



non_match = list(set(ls_compare)-set(ls_heures))
non_match = [x[0] for x in non_match]
non_match = list(set(non_match))

print("Non-match elements: ", non_match)


for i in ls_humains:

	if i[0] in non_match:
		num = i[1]
		text = "Message Automatique: {}, des heures son manquantes en S{}".format(i[0],week)
		print(num, text)
		androidhelper.Android().smsSend(num, text)
