from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.list import TwoLineAvatarIconListItem, IconRightWidget
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import ObjectProperty
from kivymd.uix.snackbar import Snackbar
from kivy.clock import Clock
from baseclass.sql import sql
from threading import Thread

ls_item = []

class Humains(Screen):

	menu_statut = ObjectProperty()

	def __init__(self, **kw):
		super().__init__(**kw)
		self.app = MDApp.get_running_app()


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


	def add_humains(self):
		if self.ids['prénom'].text != '' and self.ids['téléphone'].text != '' and self.ids['statut'].text != '' and self.ids['taux_h'].text != '' and self.ids['taille_pentalon'].text != '' and self.ids['pointure'].text != '':	

			data=(self.ids['téléphone'].text, self.ids['prénom'].text)
			cmd="SELECT * FROM HUMAINS WHERE TEL = %s OR PRENOM = %s"	

			if len(sql(cmd, data)) == 0:
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


				try:
					
					print(sql(cmd, data))
					self.app.build()
					Snackbar(text="Merci !", padding="20dp").open()

				except:
					Snackbar(text="Nop...", padding="20dp").open()

			else:
				Snackbar(text="Ce profil existe déjà", padding="20dp").open()	

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


class HumainsList(Screen):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.app = MDApp.get_running_app()

	def on_enter(self):

		for i in self.app.ls_humains:

			self.ids.container.add_widget(
				TwoLineAvatarIconListItem(text="{}".format(i[0]),secondary_text= "{}".format(i[1]), on_release=self.test)
			)


	def on_leave(self):

		while self.ids.container.children:
			for i in self.ids.container.children:
				self.ids.container.remove_widget(i)


	def test(self, instance):
		print(instance.text)