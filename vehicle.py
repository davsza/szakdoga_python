class Vehicle:
    def __init__(self, type, departure_node, arrival_node, capacity, max_travel_time):
        self.type = type
        self.departure_node = departure_node
        self.arrival_node = arrival_node
        self.capacity = capacity
        self.max_travel_time = max_travel_time

    def print(self):
        print(f"Vehicle type: {self.type}, departue_node: {self.departure_node}, arrival_node: {self.arrival_node}, "
              f"capacity: {self.capacity}, max_travel_time: {self.max_travel_time}")
