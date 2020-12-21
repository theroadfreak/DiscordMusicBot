from kivy.app import App
from kivy.uix.button import  Button
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
from kivy.config import Config

import os
import sys
from pynput import keyboard
import pyperclip
from win10toast import ToastNotifier
import subprocess

toaster = ToastNotifier()
Config.set('kivy', 'exit_on_escape', '0')

def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(os.path.dirname(sys.executable))
    else:
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)        

class menuPage(GridLayout,Screen):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.cols = 2
        
        self.box = BoxLayout(orientation='vertical', spacing=20,size_hint=(.5,.1))
        self.buttons = BoxLayout(orientation='vertical', spacing=10,size_hint=(.99,.9))

        self.popup = Popup(title='Test popup',content=Label(text="Will start typing in [color=#33cc33]3[/color] seconds",
                                                            font_size="17sp",markup=True),size_hint=(None, None), size=(400, 400))
        self.label = Label(text="",size_hint=(.5, .99))
        self.typing = TextInput(hint_text='Write here',size_hint=(.99,.1),multiline=False)
        self.typing.bind(on_text_validate=self.addToList)
        self.add = Button(text='Add', size_hint=(.99,.1))
        self.add.bind(on_press=self.addToList)
        self.start = Button(text='Start Typing', size_hint=(.99,.1)) 
        self.start.bind(on_press=self.startTyping)
        self.save = Button(text='Save List', size_hint=(.99,.1))
        self.save.bind(on_press=self.saveList)
        self.load = Button(text='Load Saved List', size_hint=(.99,.1))
        self.load.bind(on_press=self.loadFromSaved)  
        self.startL = Button(text='Start Listening', size_hint=(.99,.1))
        self.startL.bind(on_press=self.listenScreen)
        self.removelast = Button(text='Remove Last item', size_hint=(.99,.1))
        self.removelast.bind(on_press=self.removeLast)



        self.box.add_widget(Label(size_hint=(.5, .001)))
        self.box.add_widget(self.typing)
        
        self.box.add_widget(self.buttons)

        self.buttons.add_widget(self.add)
        self.buttons.add_widget(self.start)
        self.buttons.add_widget(self.save)
        self.buttons.add_widget(self.load)
        self.buttons.add_widget(self.startL)
        self.buttons.add_widget(self.removelast)
        self.buttons.add_widget(BoxLayout(size_hint=(.99,.6)))
        
        self.add_widget(self.label)
        self.add_widget(self.box)   

        
    def addToList(self, instance):
        tempInt=0
        for c in self.typing.text:
            tempInt += ord(c)
        if tempInt % 32 != 0:
            self.label.text += "{}\n".format(self.typing.text)
            self.typing.text = ""
        else:
            pass
    
    def setList(self,saveFile):
        with open(resource_path("{}.txt".format(saveFile)),"r") as f:
            self.label.text += "{}".format(f.read())
            f.close()
        
    def saveList(self, instance):
        n = 0
        while True:
            try:
                with open(resource_path("save{}.txt".format(n)), "r") as f:
                    n += 1
                    f.close()
            except:
                with open(resource_path("save{}.txt".format(n)), "w") as file:
                    file.write(self.label.text)
                    file.close() 
                break
            
    def setListFromListener(self, text):
        self.label.text += "{}\n".format(text)
    
    def loadFromSaved(self, instance):
        subprocess.run(["C:\\Users\\dusha\\miniconda3\\python.exe",resource_path("LoadFromSaved.py")])
        with open(resource_path("Clist.txt"),"r") as file:
            self.label.text += file.read()
            file.close()       
        with open(resource_path("Clist.txt"),"w") as file:
            file.close()
    
    def listenScreen(self,instance):
        DushansMusicBOT.screenmanager.current = "listenPage"
        Listener()
        
    def startTyping(self,instance):
        self.popup.open()
        try:
            with open(resource_path("Clist.txt"),"a") as f:
                f.write(self.label.text)
                f.close()
        except:
            with open(resource_path("Clist.txt"),"w") as f:
                f.write(self.label.text)
                f.close()
        
        os.startfile(resource_path("DiscordMusicBot\\KivyzTyping.exe"))
         
    def removeLast(self, instance):
        listaPesni = self.label.text
        
        listaPesniKakoList = listaPesni.split("\n")
        if listaPesniKakoList[len(listaPesniKakoList)-1] == "":
            listaPesniKakoList.pop()
            listaPesniKakoList.pop()
        else:
            listaPesniKakoList.pop()
            
        listaKakoString = "\n".join(str(e) for e in listaPesniKakoList)
        listaKakoString += "\n"
        
        self.label.text = listaKakoString
        
class Listener():
    def __init__(self):
        self.textToAdd = str()
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
                    
    def restart(self):
        self.listener.stop()
        self.listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        self.listener.start()
        
    def on_press(self,key):
        
        if key == keyboard.Key.home and self.textToAdd != pyperclip.paste():    
            self.textToAdd = pyperclip.paste()
            DushansMusicBOT.menuPageClass.setListFromListener(self.textToAdd)
            toaster.show_toast("Dushan's BOT","'{}' added to list".format(self.textToAdd))
        elif key == keyboard.Key.home: 
            toaster.show_toast("Dushan's BOT","Alraedy listed")            
        
        self.restart()            

    def on_release(self,key):
        if key == keyboard.Key.esc:
            DushansMusicBOT.screenmanager.current = "menuPage"
            return False
        
class ListenPage(GridLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.rows = 1
        self.cols = 1
        self.text = '''
        Copy the text then press the home button to add to list\n\n
                                               [color=#33cc33]Listening...[/color]\n\n
                           Press the escape button to stop'''
        self.add_widget(Label(text=self.text,font_size="17sp",markup=True))
        
            
class DushansMusicBOTApp(App):
    menuPageClass = menuPage()
    def build(self):

        self.screenmanager = ScreenManager()

        menuScreen=Screen(name="menuPage")
        menuScreen.add_widget(DushansMusicBOTApp.menuPageClass)
        self.screenmanager.add_widget(menuScreen)        

        listenScreen=Screen(name="listenPage")
        listenScreen.add_widget(ListenPage())
        self.screenmanager.add_widget(listenScreen)
        
        return self.screenmanager


if __name__ == "__main__":
    with open(resource_path("Clist.txt"),"w") as f:
        f.close()
    DushansMusicBOT = DushansMusicBOTApp()
    DushansMusicBOT.run()

    