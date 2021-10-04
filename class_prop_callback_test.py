import time

class C(object):
    def __init__(self):
        self.on_event = None
        self._event_changed = False
    
    @property 
    def event_changed(self): 
        return self._event_changed
        

    @event_changed.setter
    def event_changed(self, value): 
        self._event_changed = value
        if(value == True): 
            self.on_event()






    def on_event(self): 
        print("on_event called original function")


c = C()
def on_event_callback(): 
    print("on_event callback passed")

c.on_event = on_event_callback 


c.event_changed = True 