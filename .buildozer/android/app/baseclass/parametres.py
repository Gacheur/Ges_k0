from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.picker import MDThemePicker
from kivymd.uix.list import TwoLineAvatarIconListItem, IconRightWidget
from kivymd.uix.menu import MDDropdownMenu
from kivy.properties import ObjectProperty
from kivymd.uix.snackbar import Snackbar
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.button import MDFlatButton
from kivymd.uix.dialog import MDDialog

#from baseclass.sql import sql
from threading import Thread

import configparser

class Parametres(Screen):

	dialog = None

	def __init__(self, **kw):
		super().__init__(**kw)
		self.app = MDApp.get_running_app()


	def on_enter(self):

		ls_i_personne = [{"text": "{}".format(i[0])} for i in self.app.ls_humains]
		print(ls_i_personne)

		self.main_user_dd_menu = MDDropdownMenu(
			caller=self.ids.container,
			items=ls_i_personne,
			width_mult=3,
		)
		self.main_user_dd_menu.bind(on_release=self.set_item)

		try:
			self.app.config.read('conf.ini')
			self.ids.main_user.secondary_text = self.app.config['USER']['principal']
		except:
			None

		try:
			self.app.config.read('conf.ini')
			self.ids.adress_server.secondary_text = self.app.config['SERVER']['url']
		except:
			None



	def cancel(self, inst):

		self.app.config['THEME'] = {
			"primary" : "{}".format(self.app.theme_cls.primary_palette),
			"accent" : "{}".format(self.app.theme_cls.accent_palette),
			"theme" : "{}".format(self.app.theme_cls.theme_style),
			}

		with open('conf.ini', 'w') as configfile:
			self.app.config.write(configfile)


	def show_theme_picker(self):

		theme_dialog = MDThemePicker(on_dismiss=self.cancel)
		theme_dialog.open()



	def set_item(self, instance_menu, instance_menu_item):


		self.ids.main_user.secondary_text = instance_menu_item.text

		self.app.config['USER'] = {
			"principal" : "{}".format(instance_menu_item.text)
			}

		with open('conf.ini', 'w') as configfile:
			self.app.config.write(configfile)

		self.main_user_dd_menu.dismiss()



	def set_adresse_serveur(self):
		if not self.dialog:
			self.dialog = MDDialog(
				title="Address:",
				type="custom",
				content_cls=Content(),
				buttons=[
					MDFlatButton(
						text="CANCEL", text_color=self.app.theme_cls.primary_color
					),
					MDFlatButton(
						text="OK", on_release= self.grabText
					),
				],
			)
		self.dialog.open()


	def grabText(self, inst):
		for obj in self.dialog.content_cls.children:
			try:
				self.ids.adress_server.secondary_text = obj.text

				self.app.config['SERVER'] = {
					"url" : "{}".format(obj.text)
					}

				with open('conf.ini', 'w') as configfile:
					self.app.config.write(configfile)

			except:
				None
		self.dialog.dismiss()
		Snackbar(text="Merci, Veuillez redemarrer Ges_k0", padding="20dp").open()
		

class Content(BoxLayout):
	pass