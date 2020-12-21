from pynput import keyboard
from time import sleep
import sys,os


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = os.path.dirname(os.path.dirname(sys.executable))
    else:
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        
    return os.path.join(base_path, relative_path)        


sleep(3)

keyboardControl = keyboard.Controller()
listToType = str()   


with open(resource_path("Clist.txt"),"r") as f:
    listToType = f.read()
    f.close()
    
listToTypeAsList = listToType.split("\n")

for x in listToTypeAsList:
    if x != "" and x != " ":
        keyboardControl.type("!play ")
        keyboardControl.type(x)
        keyboardControl.press(keyboard.Key.enter)
        sleep(2)
