import vehicle as vch


class Fleet:
    def __init__(self):
        self.vehicles = []

    def addVehicle(self, vehicle):
        if isinstance(vehicle, vch.Vehicle):
            self.vehicles.append(vehicle)
        else:
            raise Exception("Wrong parameter type!")

    def vehicles(self):
        for vehicle in self.vehicles:
            print(vehicle.print())
