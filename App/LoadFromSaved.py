from kivy.app import App
from kivy.uix.button import  Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout

import sys
import os

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(os.path.dirname(sys.executable))
    else:
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)        

class SavedPage(GridLayout):
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 4
        self.rows = 4
        self.numberOfButtons = 0
        
        for _ in range(14):
            try:
                open(resource_path("save{}.txt".format(self.numberOfButtons)), "r")
                self.numberOfButtons += 1      
            except:
                break
        
        for x in range(self.numberOfButtons):
            button = Button(text="Save {}".format(x),color=(1, 1, 0 , 1))
            button.bind(on_press=self.PassTextToList)
            self.add_widget(button)
        for x in range(15 - self.numberOfButtons):
            button = Button(text="Empty Save")
            self.add_widget(button)

        self.CancelButton = Button(text="Cancel",background_color=(1, 1, 1, 0))
        self.CancelButton.bind(on_press=lambda instance: quit())
        self.add_widget(self.CancelButton)

    def PassTextToList(self,instance):
        formatedString = instance.text
        formatedString = formatedString.replace(' ', '')
        formatedString = formatedString.casefold()

        self.stringFromFile = str()
        
        with open(resource_path("{}.txt".format(formatedString)),"r") as file:
            self.stringFromFile = file.read()
        
        with open(resource_path("Clist.txt"),"a") as file:
            file.write(self.stringFromFile)
        quit()

class EpicApp(App):
    def build(self):
        return SavedPage()
  
EpicApp().run()
