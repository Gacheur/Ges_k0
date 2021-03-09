from kivy.uix.screenmanager import Screen
from kivymd.app import MDApp
from kivymd.uix.picker import MDDatePicker
from kivymd.uix.list import OneLineListItem
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
#from baseclass.sql import sql
from threading import Thread
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDFlatButton, MDFloatingActionButton
from kivymd.uix.label import MDLabel
from kivymd.uix.behaviors import TouchBehavior

from datetime import date


class Item(OneLineListItem, TouchBehavior):

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
				on_pre_open= self.azerty,
				buttons=[
					MDFlatButton(text="Continuer", on_release=self.alert_dialog_continuer_remove_heures),
					],
			)
		self.dialog_remove_heures.open()

	def azerty(self, inst):
		print(self)
		inst.text = 'test'

	def alert_dialog_continuer_remove_heures(self, inst):

		data = tuple(self.text.split("   "))
		print(data)

		cmd="DELETE FROM HEURES WHERE NOM=%s AND CHANTIERS=%s AND NB_HEURES=%s AND DATE=%s AND SEMAINE=%s"
		self.app.sql.select_insert_delete(cmd, data)
		self.parent.remove_widget(self)
		self.app.ls_heures.remove(data)
		self.dialog_remove_heures.dismiss()


'''class MDFloatingActionButton_Mod(MDFloatingActionButton, TouchBehavior):

	def __init__(self, **kw):
		super().__init__(**kw)
		self.app = MDApp.get_running_app()

	def on_long_touch(self, *args):
		label_text = self.parent.parent.ids.data_date.text
		print(label_text[0])

		if 'F' == label_text[0]:
			self.parent.parent.ids.data_date.text = label_text[2:]
		else:
			self.parent.parent.ids.data_date.text = "F {}".format(label_text)'''

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
		
		self.dialog.dismiss()
		self.spin_add_heures()
		


	def sort(self):

		self.on_leave()

		for i in self.app.ls_heures:

			if self.ids.data_pers.text == i[0] and self.week_num == i[4]:

				self.add_item_containt(('   '.join(map(str, i))), 0)


#303, 290, 265