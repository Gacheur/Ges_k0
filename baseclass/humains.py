from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.list import TwoLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton
from kivy.clock import Clock
#from baseclass.sql import sql
from threading import Thread
from kivymd.uix.behaviors import TouchBehavior
from kivymd.uix.textfield import MDTextField



class Item(TwoLineListItem, TouchBehavior):

	dialog_remove_heures= None
	def __init__(self, **kw):

		super().__init__(**kw)
		self.app = MDApp.get_running_app()

	def on_long_touch(self, *args):

		print(self.text)

		data = (self.text,)
		cmd="SELECT * FROM HUMAINS WHERE PRENOM =%s"

		global profil
		profil = self.app.sql.select_insert_delete(cmd, data)

		print("<on_long_touch> event")
		print(self.text)
		print(self.parent)
		print(self.parent.parent.parent.parent.manager.current)
		self.parent.parent.parent.parent.manager.current = 'humains' #Attention emboitement de merde...


		self.app.root.ids.humains.ids['prénom'].text = profil[0][0]
		self.app.root.ids.humains.ids['téléphone'].text = profil[0][1]
		self.app.root.ids.humains.ids['statut'].text = profil[0][2]
		self.app.root.ids.humains.ids['taux_h'].text = profil[0][3]
		self.app.root.ids.humains.ids['taille_pentalon'].text = profil[0][4]
		self.app.root.ids.humains.ids['pointure'].text = profil[0][5]


		# A revoir ! 


class Humains(Screen):

	dialog_confirm_modify_profil = None

	def __init__(self, **kw):
		super().__init__(**kw)
		self.app = MDApp.get_running_app()


	def on_pre_enter(self):
		self.ids.progress.active= False

	def on_enter(self):

		menu_items = [{"text": "Associer"},{"text": "Apprenti"},{"text": "Renégat"},{"text": "Stagiaire"}]

		self.menu_statut = MDDropdownMenu(
			caller=self.ids.statut,
			items=menu_items,
			position="center",
			width_mult=3,
		)
		self.menu_statut.bind(on_release=self.get_statut)

		



	def get_statut(self, instance_menu, instance_menu_item):

		def get_statut(interval):
			self.ids['statut'].text = instance_menu_item.text

		Clock.schedule_once(get_statut, 0.3)
		
		self.menu_statut.dismiss()


	def spin_add_humains(self):


		self.ids.progress.active= True

		p = Thread(target=self.add_humains)
		p.start()
		


	def sql_add_humaine(self):

		if self.ids['statut'].text == 'Stagiaire':
			data=(
				self.ids['prénom'].text,
				self.ids['téléphone'].text,
				self.ids['statut'].text,
				0.0,
				'0',
				'0'
			)

		else:
			data=(
				self.ids['prénom'].text,
				self.ids['téléphone'].text,
				self.ids['statut'].text,
				self.ids['taux_h'].text,
				self.ids['taille_pentalon'].text,
				self.ids['pointure'].text
			)

		cmd="INSERT INTO HUMAINS(PRENOM, TEL, STATUT, TAUX_H, TAILLE_PENTALON, POINTURE) VALUES (%s,%s,%s,%s,%s,%s)"

			
		self.app.sql.select_insert_delete(cmd, data)
		self.app.ls_humains.insert(0, data)



		self.app.config['USER'] = {
			"principal" : "{}".format(self.ids['prénom'].text)
			}

		with open('conf.ini', 'w') as configfile:
			self.app.config.write(configfile)

			
		Snackbar(text="Merci !", padding="20dp").open()


	def add_humains(self):
		if self.ids['prénom'].text != '' and self.ids['téléphone'].text != '' and self.ids['statut'].text != '' and self.ids['taux_h'].text != '' and self.ids['taille_pentalon'].text != '' and self.ids['pointure'].text != '':	

			data=(self.ids['téléphone'].text, self.ids['prénom'].text)
			cmd="SELECT * FROM HUMAINS WHERE TEL = %s OR PRENOM = %s"	

			if len(self.app.sql.select_insert_delete(cmd, data)) == 0:
				try:
					self.sql_add_humaine()
				except:
					Snackbar(text="Nop...", padding="20dp").open()

			else:
				self.alert_dialog()

		else:

			Snackbar(text="Les champs doivent etre completés", padding="20dp").open()

			for i in self.ids:
				try:
					if self.ids[i].text == '':
						self.ids[i].icon_right = 'alert'
				except:
					None

			

		self.ids.progress.active= False
		return


	def alert_dialog(self):
		if not self.dialog_confirm_modify_profil:
			self.dialog_confirm_modify_profil = MDDialog(
			title="Attention",
			text="Voulez vous vraiment modifier ce profil ?",
			buttons=[
				MDFlatButton(text="Continuer", on_release=self.alert_dialog_continuer),
				],
			)
		self.dialog_confirm_modify_profil.open()


	def alert_dialog_continuer(self, inst):

		data = profil[0]
		print(data)

		cmd="DELETE FROM HUMAINS WHERE PRENOM=%s AND TEL=%s AND STATUT=%s AND TAUX_H=%s AND TAILLE_PENTALON=%s AND POINTURE=%s"
		self.app.sql.select_insert_delete(cmd, data)
		self.app.ls_humains.remove(data)

		self.sql_add_humaine()
		print(profil)

		self.dialog_confirm_modify_profil.dismiss()



class HumainsList(Screen):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.app = MDApp.get_running_app()

	def on_enter(self):

		for i in self.app.ls_humains:

			self.ids.container.add_widget(
				Item(text="{}".format(i[0]),secondary_text= "{}".format(i[1]), on_release=self.test)
			)


	def on_leave(self):

		while self.ids.container.children:
			for i in self.ids.container.children:
				self.ids.container.remove_widget(i)


	def test(self, instance):
		print(instance.text)