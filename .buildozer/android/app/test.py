import asyncio
import random
import time
from kivy.app import App
from kivy.lang import Builder

ui = Builder.load_string('''
BoxLayout:
    orientation: 'vertical'
    GridLayout:
        rows: 2
        cols: 2
        Label:
            text: 'Status:'
            size_hint: 0.3, 1
        Label:
            id: status
            text: ''
        Label:
            text: 'Data:'
            size_hint: 0.7, 1
        Label:
            id: data
            text: ''
    BoxLayout:
        direction: 'horizontal'
        Button:
            text: 'Get Data'
            on_press: app.connect()
        Button:
            text: 'Stop Data'
            on_press: pass
''')

class MyAsyncApp(App):

    def __init__(self):
        super(self.__class__, self).__init__()

        self.x_connected = None
        self.x_widget_data = None
        self.x_widget_status = None
        self.x_loop = asyncio.get_event_loop()

    def build(self):
        return ui

    def connect(self):
        # Get widget
        self.x_widget_status = self.root.ids.status

        # Update status
        self.x_widget_status.text = 'Preparing to connect...'

        # Connect using asyncio
        # --> But the loop must be already running <---
        self.x_loop.call_soon(self.do_connect)

    async def do_connect(self):
        # Connect asynchronously

        # Get widget
        self.x_widget_data = self.root.ids.data

        # Update status
        self.x_connected = False
        self.x_widget_status.text = 'Connecting...'

        # Perform actual actions
        try:
            result = await self.feed_kivy()
            if result:
                self.x_widget_status.text = 'Service not available: ' + result
                return
        except Exception as e:
            self.x_widget_status.text = 'Error while connecting'
            return

        # Update status
        self.x_connected = True
        self.x_widget_status.text = 'Connected'

    async def feed_kivy(self):
        # Deliver fresh data at random interval

        # Some slow process to get data
        result = await asyncio.sleep(random.randint(1, 5), time.time())
        self.x_widget_data.text = result

        # Reschedule ourselves
        await self.x_loop.call_soon(self.feed_kivy())


def main():
    # If loop started here, app is never started
    loop = asyncio.get_event_loop()
    loop.call_soon(MyAsyncApp().run())
    loop.run_forever()
    loop.close()


if __name__ == '__main__':
    main()