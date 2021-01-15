from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.utils import platform

Window.softinput_mode = 'below_target'

if platform == 'linux':
	Window.size = (425,700)

from kivymd.uix.snackbar import Snackbar


from baseclass.heures import Heures
from baseclass.humains import Humains
from baseclass.chantiers import Chantiers
from baseclass.parametres import Parametres
from baseclass.sql import sql

import version
import configparser
import mysql.connector


class Accueil(Screen):
	pass


class MainApp(MDApp):

	def build(self):

	
		self.config = configparser.ConfigParser()
		
		try:
			
			self.config.read('conf.ini')

			self.theme_cls.primary_palette = self.config['THEME']['primary']
			self.theme_cls.accent_color = self.config['THEME']['accent']
			self.theme_cls.theme_style = self.config['THEME']['theme']
		except:
			None


		try:

			self.title = version.__version__
			irl_version = sql("SELECT VERSION FROM LOG")[0][0]

			print(self.title, irl_version)

			if self.title == irl_version:

				self.ls_humains = sql("SELECT * from HUMAINS")
				print(self.ls_humains)

				self.ls_chantiers = sql("SELECT * from CHANTIERS")
				print(self.ls_chantiers)

				self.ls_heures = sql("SELECT * from HEURES")
				self.ls_heures.reverse()
				print(self.ls_heures)

				return Builder.load_file("main.kv")


			else:
				return Builder.load_file("kv/error_version.kv")

		except:
			return Builder.load_file("kv/error_url.kv")



	def set_serveur_adress(self):

		try:
			mysql.connector.connect(host='{}'.format(self.root.ids.server_adress.text),database='TDC')

			self.config['SERVER'] = {
				"url" : "{}".format(self.root.ids.server_adress.text)
				}

			with open('conf.ini', 'w') as configfile:
				self.config.write(configfile)

			Snackbar(text="Merci, Veuillez redemarrer Ges_k0", padding="20dp").open()

		except:

			Snackbar(text="Adresse invalide", padding="20dp").open()

MainApp().run()