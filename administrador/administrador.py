from kivy.app import App
from kivy.uix.boxlayout import BoxLayout

class AdministradorWindow(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
class AdministradorApp(App):
    def build(self):
        return AdministradorWindow()
    
if __name__ == "__main__":
    AdministradorApp().run()