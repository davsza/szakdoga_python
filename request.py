class Request:
    def __init__(self, id, node, time_start, time_end, quantity, service_time):
        self.id = id
        self.node = node
        self.time_start = time_start
        self.time_end = time_end
        self.quantity = quantity
        self.service_time = service_time

    def print(self):
        print(f"Request id: {self.id}, node: {self.node}, time_start: {self.time_start}, time_end: {self.time_end}, "
              f"quantity: {self.quantity}, service_time: {self.service_time}")
