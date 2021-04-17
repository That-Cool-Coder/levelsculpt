import tkinter as tk
import os

from levelsculpt.config import *
from levelsculpt.ui import EditorViewport, EditorSidebar

class Application:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title(PRODUCTION_NAME)

        self.scriptDir = os.path.dirname(__file__)
        #photo = tk.PhotoImage(file=os.path.join(self.scriptDir, ICON_PATH))
        #self.root.iconphoto(True, photo)

        self.editorViewportHolder = tk.Frame(self.root)
        self.editorViewportHolder.grid(row=0, column=0)
        self.editorViewport = EditorViewport(self.editorViewportHolder)

        self.editorSidebarHolder = tk.Frame(self.root, background='white')
        self.editorSidebarHolder.grid(row=0, column=1)
        self.editorSidebar = EditorSidebar(self.editorSidebarHolder, self.updateEditorSettings)
    
    def mainloop(self):
        self.root.mainloop()
    
    def updateEditorSettings(self, newSettings):
        self.editorViewport.settings = newSettings