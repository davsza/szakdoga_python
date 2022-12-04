import math


class Dataset:
    def __init__(self, info, network, fleet, requests):
        self.info = info
        self.network = network
        self.fleet = fleet
        self.requests = requests

    def getinfo(self):
        self.info.print()

    def print(self):
        print(f"Dataset info: {self.info.dataset}, {self.info.name}")
        print("Network: ")
        for node in self.network.nodes:
            node.print()
        for vehicle in self.fleet.vehicles:
            vehicle.print()
        for request in self.requests:
            request.print()

    def generateMatrix(self, solomon):
        matrix = []
        for idx1, node1 in enumerate(self.network.nodes):
            row = []
            for idx2, node2 in enumerate(self.network.nodes):
                if idx1 == idx2:
                    row.append(0)
                else:
                    cx1, cy1 = node1.cx, node1.cy
                    cx2, cy2 = node2.cx, node2.cy
                    if solomon:
                        distance = math.sqrt((float(cx1) - float(cx2)) ** 2 + (float(cy1) - float(cy2)) ** 2)
                    else:
                        distance = abs(float(cx1) - float(cx2)) + abs(float(cy1) - float(cy2))
                        distance = distance * 0.000189394 * 3600 / 40
                    # distance = distance * 0.000189394 * (distance * 0.9144) / 17.88161
                    row.append(distance)
            matrix.append(row)
        return matrix

    def printMatrix(self):
        matrix = self.generateMatrix()
        for row in matrix:
            for column in row:
                print(f"{column} ", end="")
            print()

    def writeFile(self, fileName, solomon):
        matrix = self.generateMatrix(solomon)
        with open(fileName, 'w') as file:
            file.write(f"{self.info.dataset} : {self.info.name}")
            file.write("\nNodes (cx, cy, quantity, beginDt, endDt, serviceTime)")
            for node, request in zip(self.network.nodes, self.requests):
                file.write(f"\n{node.cx} {node.cy} {request.quantity} {request.time_start} {request.time_end} "
                           f"{request.service_time}")
            file.write("\nVehicles (type, departureNode, arrivalNode, capacity, maximumTravelTime)")
            for vehicle in self.fleet.vehicles:
                file.write(f"\n{vehicle.type} {vehicle.departure_node} {vehicle.arrival_node} {vehicle.capacity} "
                           f"{vehicle.max_travel_time}")
            file.write("\nDistance matrix")
            file.write("\n")
            for row in matrix:
                for value in row:
                    file.write(f"{value} ")
                file.write("\n")







