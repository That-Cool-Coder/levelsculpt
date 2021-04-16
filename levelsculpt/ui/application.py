import tkinter as tk
import os

from levelsculpt.config import *
from levelsculpt.ui import EditorViewport

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(PRODUCTION_NAME)

        import os
        self.scriptDir = os.path.dirname(__file__)

        photo = tk.PhotoImage(file=os.path.join(self.scriptDir, ICON_PATH))
        self.root.iconphoto(True, photo)

        self.editorViewport = EditorViewport(self.root)
    
    def mainloop(self):
        self.root.mainloop()