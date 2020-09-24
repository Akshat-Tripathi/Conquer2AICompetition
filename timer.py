class turn_timer:
    now = 0
    def __init__(self, interval):
        self.interval = interval
        self.events = []

    def add_event(self, event):
        self.events.append(event)
    
    def reset(self):
        self.now = self.interval - 1
    
    def tick(self):
        now = (self.now - 1) % self.interval
        if now == 0:
            for event in self.events:
                event()
            self.reset()
        self.now = now
