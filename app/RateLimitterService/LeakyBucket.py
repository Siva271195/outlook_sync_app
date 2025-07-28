import time

# This is actually TokenBucket Implementation, i was a bit confused as was reading both together.
class LeakyBucket:
    def __init__(self, capacity, refresh_rate):
        self.capacity = capacity
        self.current_capacity = 0
        self.refresh_rate = refresh_rate
        self.last_refresh_time = time.time()

    def add(self, items):
        self.refresh()

        if self.current_capacity >= self.capacity:
            return 0,False
        if self.current_capacity < self.capacity and len(items) + self.current_capacity <= self.capacity:
            self.current_capacity += len(items)
            return len(items),True
        else:
            item_to_add = self.capacity - self.current_capacity
            self.current_capacity = self.capacity
            return item_to_add,True

    def refresh(self):
        current_time = time.time()
        if current_time - self.last_refresh_time >= self.refresh_rate:
            self.current_capacity = 0
            self.last_refresh_time = current_time
    
    def get_current_capacity(self):
        self.refresh()
        return self.current_capacity
    
    def get_available_capacity(self):
        self.refresh()
        return self.capacity - self.current_capacity
    
    def release(self, item_count):
        self.current_capacity = self.current_capacity - item_count
        if(self.current_capacity < 0):
            self.current_capacity = 0