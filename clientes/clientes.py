from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class ClientesWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(*kwargs)
        
class ClientesApp(App):
    def build(self):
        return ClientesWindow()
    
if __name__ == "__main__":
    ClientesApp().run()