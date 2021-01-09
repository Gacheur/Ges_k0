from kivy.lang import Builder

from kivymd.app import MDApp

KV = '''
Screen:

    MDSpinner:
        id: spinner
        size_hint: None, None
        size: dp(46), dp(46)
        pos_hint: {'center_x': .5, 'center_y': .5}
        determinate: True

    MDCheckbox:
        id: check
        size_hint: None, None
        size: dp(48), dp(48)
        pos_hint: {'center_x': .5, 'center_y': .4}
        active: True
        on_active: root.test()

'''


class Test(MDApp):
    def build(self):
        return Builder.load_string(KV)

    def test(self):
        print('test')
        root.ids.spinner.active == True



Test().run()