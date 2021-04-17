class KeyTracker:
    def __init__(self, widget):
        self.keysDown = []
        widget.bind_all('<KeyPress>', self.registerKeyDown)
        widget.bind_all('<KeyRelease>', self.registerKeyUp)
    
    def registerKeyDown(self, event):
        self.keysDown.append(event.keysym)
    
    def registerKeyUp(self, event):
        if event.keysym in self.keysDown:
            self.keysDown.remove(event.keysym)
    
    def keyIsDown(self, keysym):
        return keysym in self.keysDown
    
    def controlDown(self):
        return self.keyIsDown('Control_L') or self.keyIsDown('Control_R')