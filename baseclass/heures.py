from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.list import OneLineListItem, OneLineAvatarIconListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
#from baseclass.sql import sql
from threading import Thread
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivymd.uix.behaviors import TouchBehavior

from datetime import date

import time
from kivy.clock import Clock
Clock.max_iteration = 100

'''class Item(OneLineListItem, TouchBehavior):

	dialog_remove_heures= None

	def __init__(self, **kw):
		super().__init__(**kw)
		self.app = MDApp.get_running_app()
		self.week_num = ()

	def on_long_touch(self, *args):

		if not self.dialog_remove_heures:
			self.dialog_remove_heures = MDDialog(
				title="Supprimer",
				text="Etes vous sur de vouloir supprimer {} ?".format(self.text),
				buttons=[
					MDFlatButton(text="Continuer", on_release=self.alert_dialog_continuer_remove_heures),
					],
			)
		self.dialog_remove_heures.open()

	def alert_dialog_continuer_remove_heures(self, inst):

		data = tuple(self.text.split("   "))
		print(data)

		cmd="DELETE FROM HEURES WHERE NOM=%s AND CHANTIERS=%s AND NB_HEURES=%s AND DATE=%s AND SEMAINE=%s"
		self.app.sql.select_insert_delete(cmd, data)
		self.parent.remove_widget(self)
		self.app.ls_heures.remove(data)
		self.dialog_remove_heures.dismiss()


value = None

class ItemConfirm(OneLineAvatarIconListItem): #Pour la boite de dialogue
	divider = None

	def set_icon(self, instance_check):

		global value
		value = self.text

		instance_check.active = True
		check_list = instance_check.get_widgets(instance_check.group)
		for check in check_list:
			if check != instance_check:
				check.active = False

class Heures(Screen):


	dialog = None
	dialog_remove_heures= None
	target_rm = None


	def __init__(self, **kw):
		super().__init__(**kw)
		self.app = MDApp.get_running_app()
		self.week_num = ()



	def sql_add_heures(self):

		cmd="INSERT INTO HEURES(NOM, CHANTIERS, NB_HEURES, DATE, SEMAINE) VALUES (%s,%s,%s,%s,%s)"

		data = (
			self.ids['data_pers'].text,
			self.ids['data_chantier'].text,
			self.ids['data_time'].text, 
			self.ids['data_date'].text,
			self.week_num
		)

		self.app.sql.select_insert_delete(cmd, data)
		self.add_item_containt('   '.join(data), index= len(self.ids.container.children))

		self.app.ls_heures.insert(0, data)

		Snackbar(text="Merci !", padding="20dp").open()


	def add_item_containt(self, text, index):

		new_line = Item(text=text)
		self.ids.container.add_widget(new_line, index=index)

	def remove_label(self):

		self.ids.data_time.text =''
		self.ids.data_date.text =''
		self.ids.data_pers.text =''
		self.ids.data_chantier.text =''

	def on_leave(self):

		while self.ids.container.children:
			for i in self.ids.container.children:
				self.ids.container.remove_widget(i)


	def on_pre_enter(self):
		self.ids.progress.active= False

	def on_enter(self):


		try:
			self.app.config.read('conf.ini')
			self.ids['data_pers'].text = self.app.config['USER']['principal']
		except:
			None


		self.ids['data_date'].text = str(date.today().strftime('%d-%m'))
		self.week_num = str('S{}'.format(date.today().isocalendar()[1]))
		self.ids['data_time'].text = '8h'

	
		for i in self.app.ls_heures:

			self.add_item_containt('   '.join(i), 0)
			
		#ls personnes
		ls_i_personne = [{"text": "{}".format(i[0])} for i in self.app.ls_humains]
		self.menu = MDDropdownMenu(caller=self.ids.pick_pers, items=ls_i_personne, position="bottom", width_mult=3)
		self.menu.bind(on_release=self.get_humains)


		#ls chantier
		ls_i_chantier = [{"text": "{}".format(i[0])} for i in self.app.ls_chantiers]
		self.menu_chantier = MDDropdownMenu(caller=self.ids.pick_chantier, items=ls_i_chantier, position="bottom", width_mult=3)
		self.menu_chantier.bind(on_release=self.get_chantier)

		#ls nb_heures
		ls_i_nb_heures = [{"text":"{}h".format(i+1)} for i in range(9)]
		ls_i_nb_heures.append({'text':'Mal'})
		ls_i_nb_heures.append({'text':'Abs'})
		ls_i_nb_heures.append({'text':'Form'})
		ls_i_nb_heures.append({'text':'CP'})
		ls_i_nb_heures.append({'text':'AT'})
		self.menu_time = MDDropdownMenu(caller=self.ids.pick_time,items=ls_i_nb_heures,position="bottom",width_mult=2)
		self.menu_time.bind(on_release=self.get_time)



	def show_date_picker(self):
		date_dialog = MDDatePicker()
		date_dialog.bind(on_save=self.get_date)
		date_dialog.open()

	def get_time(self, instance_menu, instance_menu_item):
		self.ids['data_time'].text = instance_menu_item.text
		self.menu_time.dismiss()
	
	def get_humains(self, instance_menu, instance_menu_item):
		self.ids['data_pers'].text = instance_menu_item.text
		self.menu.dismiss()

	def get_chantier(self, instance_menu, instance_menu_item):
		self.ids['data_chantier'].text = instance_menu_item.text
		self.menu_chantier.dismiss()

	def get_date(self, instance, date, date_range):
		self.ids['data_date'].text = str(date.strftime('%d-%m'))
		self.week_num = str('S{}'.format(date.isocalendar()[1]))


	def spin_add_heures(self):


		self.ids.progress.active= True

		p = Thread(target=self.add_heures)
		p.start()
		

	def add_heures(self):


		if self.ids['data_time'].text!='' and self.ids['data_chantier'].text!='' and self.ids['data_pers'].text!='' and self.ids['data_date'].text!='' :#Les champs sont pas vides A REVOIR !

			data = (self.ids['data_date'].text, self.ids['data_pers'].text)
			cmd="SELECT * FROM HEURES WHERE DATE =%s AND NOM =%s"

			if len(self.app.sql.select_insert_delete(cmd, data)) == 0:

				try:
					self.sql_add_heures()

				except:
					Snackbar(text="Nop...", padding="20dp").open()

			else:
				self.alert_dialog()

		else:
			Snackbar(text="Les champs doivent etre completés", padding="20dp").open()


		self.ids.progress.active= False

		return


	def alert_dialog(self):
		if not self.dialog:
			self.dialog = MDDialog(
			title="Attention",
			text="Tu as déjà des heures sur cette date. Merci de verifier les informations",
			buttons=[
				MDFlatButton(text="Continuer", on_release=self.alert_dialog_continuer),
				],
			)
		self.dialog.open()


	def alert_dialog_continuer(self, inst):

		self.sql_add_heures()
		self.dialog.dismiss()


	def sort(self):

		self.on_leave()

		for i in self.app.ls_heures:

			if self.ids.data_pers.text == i[0] and self.week_num == i[4]:

				self.add_item_containt(('   '.join(map(str, i))), 0)


#303, 290, 265'''




from kivymd.uix.list import OneLineAvatarIconListItem, OneLineListItem
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDFloatingActionButton
from kivymd.uix.picker import MDDatePicker
from kivy.uix.boxlayout import BoxLayout
from kivymd.uix.behaviors import TouchBehavior

from kivymd.uix.snackbar import Snackbar

from datetime import date

import version


value = None


class ItemConfirm(OneLineAvatarIconListItem): #Pour la boite de dialogue
	divider = None

	def set_icon(self, instance_check):

		global value
		value = self.text

		instance_check.active = True
		check_list = instance_check.get_widgets(instance_check.group)
		for check in check_list:
			if check != instance_check:
				check.active = False

class Content_dialog_picker(BoxLayout):
	pass


class Item(OneLineListItem, TouchBehavior): #Pour la liste d'afichage


	def __init__(self, **kw):
		super().__init__(**kw)
		self.app = MDApp.get_running_app()

	def on_long_touch(self, *args):

		screen = self.app.root.ids.screen_manager.get_screen("heures")

		screen.dialog_remove_heures.title = 'Voulez vous supprimer ?'
		screen.dialog_remove_heures.text = self.text
		screen.dialog_remove_heures.open()



class Heures(Screen):

	dialog_picker = None
	dialog_remove_heures= None
	dialog_date = None
	init_list = None

	def __init__(self, **kw):
		super().__init__(**kw)
		self.app = MDApp.get_running_app()

	def grabText(self, inst):

		dialog_selected = inst.parent.parent.parent.parent.title

		if dialog_selected == 'Chantier':
			self.ids.data_chantier.text = value

		elif dialog_selected == 'Personne':
			self.ids.data_pers.text = value

		elif dialog_selected == "Nombre d'heures":		
			self.ids.data_time.text = value

		self.dialog_picker.dismiss()

	def get_date(self, instance, date, date_range):
		self.ids['data_date'].text = str(date.strftime('%d-%m'))
		self.week_num = str('S{}'.format(date.isocalendar()[1]))


	def alert_dialog_continuer_remove_heures(self, inst):

		dialog_selected = inst.parent.parent.parent.parent.text
		data = tuple(dialog_selected.split("   "))
		print(data)

		cmd="DELETE FROM HEURES WHERE NOM=%s AND CHANTIERS=%s AND NB_HEURES=%s AND DATE=%s AND SEMAINE=%s"
		self.app.sql.select_insert_delete(cmd, data)

		ls = [i for i in self.ids.maincontainer.children if i.text == dialog_selected]
		self.ids.maincontainer.remove_widget(ls[0])	
		self.dialog_remove_heures.dismiss()

	def caller(self, spec):
		print(self.dialog_picker)
		print(self.dialog_picker.content_cls.children)
		print(self.dialog_picker.content_cls.children[0].children)

		self.dialog_picker.title = spec

		if spec == "Nombre d'heures":
			ls = self.ls_heures 

		elif spec == 'Personne' :
			ls = self.ls_humains

		else:
			ls = self.ls_chantiers

		for j in ls:

			self.dialog_picker.content_cls.children[0].children[0].add_widget(j)

		self.dialog_picker.open()


	def clear_bialog_box(self, inst):
		while self.dialog_picker.content_cls.children[0].children[0].children:
			for i in self.dialog_picker.content_cls.children[0].children[0].children:
				self.dialog_picker.content_cls.children[0].children[0].remove_widget(i)


	def sort(self):

		# Suppression des items de la scroll_view
		while self.ids.maincontainer.children:
			for i in self.ids.maincontainer.children:
				self.ids.maincontainer.remove_widget(i)


		# Ajouts des items dans la scroll_view
		for i in self.ls_data:
			if self.ids.data_pers.text == i[0] and self.week_num == i[4]: # Par personne et par semaine 
				new_line = Item(text='   '.join(i))
				self.ids.maincontainer.add_widget(new_line)	


	def spin_add_heures(self):
		self.ids.progress.active= True

		def add_heures():

			if self.ids['data_time'].text!='' and self.ids['data_chantier'].text!='' and self.ids['data_pers'].text!='' and self.ids['data_date'].text!='' :#Les champs sont pas vides A REVOIR !

				data = (self.ids['data_date'].text, self.ids['data_pers'].text)
				cmd="SELECT * FROM HEURES WHERE DATE =%s AND NOM =%s"

				if len(self.app.sql.select_insert_delete(cmd, data)) == 0:

					try:

						cmd="INSERT INTO HEURES(NOM, CHANTIERS, NB_HEURES, DATE, SEMAINE) VALUES (%s,%s,%s,%s,%s)"

						data = (
							self.ids['data_pers'].text,
							self.ids['data_chantier'].text,
							self.ids['data_time'].text, 
							self.ids['data_date'].text,
							self.week_num
						)

						self.app.sql.select_insert_delete(cmd, data)

						new_line = Item(text='   '.join(data))
						self.ids.maincontainer.add_widget(new_line, index= len(self.ids.maincontainer.children))	

						#self.ls_data.insert(0, data)

						Snackbar(text="Merci !", padding="20dp").open()

					except:
						Snackbar(text="Nop...", padding="20dp").open()

				else:
					self.dialog_remove_heures.title = 'Attention'
					self.dialog_remove_heures.text = 'Vous avez déjà des heures saisies sur cette date, voulez vous continuer ?'
					self.dialog_remove_heures.open()

			else:
				Snackbar(text="Les champs doivent etre completés", padding="20dp").open()

			self.ids.progress.active= False
			


		Thread(target=add_heures).start()
		


	def remove_label(self):

		self.ids.data_time.text =''
		self.ids.data_date.text =''
		self.ids.data_pers.text =''
		self.ids.data_chantier.text =''

	def on_leave(self):

		while self.ids.maincontainer.children:
			for i in self.ids.maincontainer.children:
				self.ids.maincontainer.remove_widget(i)

	def on_enter(self):
		self.ids.progress.active= True

		def init():
			if not self.init_list:
				print('Init init_list')
				self.ls_humains = [ItemConfirm(text=i[0]) for i in self.app.ls_humains]
				self.ls_chantiers = [ItemConfirm(text=i[0]) for i in self.app.ls_chantiers]
				self.ls_heures = [ItemConfirm(text=i) for i in ['1','2','3','4','5','6','7','8','9','Mal','Abs','Form','CP','AT']]
				self.ls_data = self.app.ls_data
				self.week_num = str('S{}'.format(date.today().isocalendar()[1]))
				self.init_list=1

			if not self.dialog_picker:
				print('Init dialog_picker')
				self.dialog_picker = MDDialog(
					type="custom",
					content_cls=Content_dialog_picker(),
					on_dismiss= self.clear_bialog_box,
					buttons=[
						MDFlatButton(
							text="Confirmer", on_release=self.grabText
						),
					]
				)


			if not self.dialog_remove_heures:
				print('Init dialog_remove_heures')
				self.dialog_remove_heures = MDDialog(
					title="Dialog_remove",
					text="text",
					buttons=[
						MDFlatButton(text="Continuer", on_release=self.alert_dialog_continuer_remove_heures),
						],
				)

			if not self.dialog_date:
				self.dialog_date = MDDatePicker()
				self.dialog_date.bind(on_save=self.get_date)

			
			for i in self.ls_data:
				new_line = Item(text='   '.join(i))
				self.ids.maincontainer.add_widget(new_line)	#2sec


			try:
				self.app.config.read('conf.ini')
				self.ids.data_pers.text = self.app.config['USER']['principal']
			except:
				None

			self.ids.data_date.text = str(date.today().strftime('%d-%m'))
			self.ids.data_time.text = '8h'

			self.ids.progress.active= False


		Thread(target=init).start()

if __name__ == "__main__":
	MainApp().run()