import tkinter as tk
import os

from levelsculpt.config import *
from levelsculpt.ui import WorldViewport

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(PRODUCTION_NAME)

        self.scriptDir = os.path.dirname(__file__)
        #photo = tk.PhotoImage(file=os.path.join(self.scriptDir, ICON_PATH))
        #self.root.iconphoto(True, photo)

        self.worldViewport = WorldViewport(self.root)
    
    def mainloop(self):
        self.root.mainloop()