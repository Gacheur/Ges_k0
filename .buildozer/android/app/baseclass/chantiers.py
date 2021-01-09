from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.list import TwoLineAvatarIconListItem, IconRightWidget
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import ObjectProperty
from kivymd.uix.snackbar import Snackbar
from baseclass.sql import sql
from threading import Thread

class Chantiers(Screen):

	def __init__(self, **kw):
		super().__init__(**kw)
		self.app = MDApp.get_running_app()


	def spin_add_chantier(self):

		self.ids.progress.active= True

		p = Thread(target=self.add_chantier)
		p.start()

	def add_chantier(self):

		if self.ids['nom'].text != '' and self.ids['localisation'].text != '': #Si les champs ne sont pas vide

			data=(self.ids['nom'].text,self.ids['localisation'].text)
			cmd="SELECT * FROM CHANTIERS WHERE NOM =%s OR LOCALISATION =%s"			

			if len(sql(cmd, data)) == 0:
				try:
					cmd="INSERT INTO CHANTIERS(NOM, LOCALISATION) VALUES (%s,%s)"
			
					sql(cmd, data)
					self.app.build()
					Snackbar(text="Merci !", padding="20dp").open()


				except:
					Snackbar(text="Nop...", padding="20dp").open()

			else:
				Snackbar(text="Ce chantier existe déjà", padding="20dp").open()			


		else:
			Snackbar(text="Les champs doivent etre completés", padding="20dp").open()
			for i in self.ids:
				try:
					if self.ids[i].text == "":
						self.ids[i].icon_right = 'alert'
				except:
					None

		self.ids.progress.active= False
		return



class ChantiersList(Screen):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		self.app = MDApp.get_running_app()


	def on_enter(self):

		for i in self.app.ls_chantiers:

			self.ids.container.add_widget(
				TwoLineAvatarIconListItem(text="{}".format(i[0]),secondary_text= "{}".format(i[1]), on_release=self.test)
			)

	def on_leave(self):

		while self.ids.container.children:
			for i in self.ids.container.children:
				self.ids.container.remove_widget(i)

	def test(self, instance):
		print(instance.text)