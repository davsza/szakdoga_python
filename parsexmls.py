import glob
import os
import random
import xml.etree.ElementTree as et
import time

import info as inf
import node as nd
import vehicle as vhc
import request as req
import dataset as data
import network as nw
import fleet as flt

now = time.localtime()
current_time = time.strftime("%H:%M:%S", now)
print(f"Start: {current_time}")

path = "C:\\Users\\david\\Documents\\Szakdoga\\datasets"
path2 = "C:\\Users\\david\\Documents\\Szakdoga\\datasets\\benchmark"
path_results = "C:\\Users\\david\\Documents\\Szakdoga\\results\\final"
path_test = "C:\\Users\\david\\Documents\\Szakdoga\\datasets\\test"
path_test_result = "C:\\Users\\david\\Documents\\Szakdoga\\datasets\\test\\result"
idx = 0
dateSets = []
info = None
network = nw.Network()
fleet = flt.Fleet()
requests = []


def stringToSec(param):
    hour = 0
    minute = 0
    if len(param) == 4:
        if param[0] == 0:
            hour += int(param[1])
        else:
            str0 = param[0]
            str1 = param[1]
            str_ = str0 + str1
            hour += int(str_)
        str2 = param[2]
        str3 = param[3]
        str__ = str2 + str3
        minute += int(str__)
        return hour * 3600 + minute * 60
    elif len(param) == 3:
        hour += int(param[0])
        str2 = param[1]
        str3 = param[2]
        str__ = str2 + str3
        minute += int(str__)
        return hour * 3600 + minute * 60
    elif len(param) == 1:
        return 0


def gather_data():
    final = dict()
    for filename in glob.glob(os.path.join(path_results, '*.txt')):
        print(filename)
        with open(os.path.join(os.getcwd(), filename), 'r') as file:
            lines = file.readlines()
            alns_distance = -1
            vehicle_count_a = -1
            iterations = -1
            values = []
            for line in lines:
                if "_data:" in line:
                    line = line.split(" ")
                    data_info = line[1][:len(line[1])-1]
                if "_greedyDistance:" in line:
                    line = line.split(" ")
                    greedy_distance = float(line[1][:len(line[1])-1])
                if "_vehicleCountG:" in line:
                    line = line.split(" ")
                    vehicle_count_g = int(line[1][:len(line[1])-1])
                if "_ALNSDistance:" in line:
                    line = line.split(" ")
                    alns_distance = float(line[1][:len(line[1])-1])
                if "_vehicleCountA:" in line:
                    line = line.split(" ")
                    vehicle_count_a = int(line[1][:len(line[1])-1])
                if "_iterations:" in line:
                    line = line.split(" ")
                    iterations = int(line[1][:len(line[1])-1])
                if "_values:" in line:
                    line = line.split(" ")
                    values = line[1]
            if data_info not in final:
                data_dict = dict()
                data_dict["gDst"] = greedy_distance
                data_dict["gVC"] = vehicle_count_g
                aDst = [alns_distance] if alns_distance != -1 else []
                aVC = [vehicle_count_a] if alns_distance != -1 else []
                it = [iterations] if alns_distance != -1 else []
                val = [values]
                data_dict["aDst"] = aDst
                data_dict["aVC"] = aVC
                data_dict["it"] = it
                data_dict["val"] = val
                final[data_info] = data_dict
            else:
                final[data_info]["aDst"].append(alns_distance) if alns_distance != -1 else None
                final[data_info]["aVC"].append(vehicle_count_a) if alns_distance != -1 else None
                final[data_info]["it"].append(iterations) if alns_distance != -1 else None
                final[data_info]["val"].append(values)
    print(final)
    with open("final_results.csv", 'w') as file:
        for k, v in final.items():
            name = k
            col = ";"
            vGC = v["gVC"]
            gDst = v["gDst"]
            aVCmin = min(v["aVC"])
            aVCmax = max(v["aVC"])
            aVCavg = sum(v["aVC"]) / len(v["aVC"])
            aDstmin = min(v["aDst"])
            aDstmax = max(v["aDst"])
            aDstavg = sum(v["aDst"]) / len(v["aDst"])
            str_ = str(name) + col + str(vGC) + col + str(gDst) + col + str(aVCmin) + col + str(aVCmax) + col + str(aVCavg) + col + str(aDstmin) + col + str(aDstmax) + col + str(aDstavg) + "\n"
            print(str_)
            file.write(str_)


def kim():
    for filename in glob.glob(os.path.join(path2, '*.txt')):
        with open(os.path.join(os.getcwd(), filename), 'r') as file:
            name = filename.split("\\")[-1].split(".")[0]
            size = name.split("_")[0]
            name = "stop_" + str(size)
            lines = file.readlines()
            capacity = float(lines[0].split("\t")[0].strip())
            total_yardage = float(lines[1].split("\t")[0].strip())
            total_number_of_stops = float(lines[2].split("\t")[0].strip())
            speed = float(lines[4].split("\t")[0].strip())

            info = None
            network = nw.Network()
            fleet = flt.Fleet()
            requests = []

            info = inf.Info("benchmark", name)
            print(f"Processing {info.name}")

            idx = 0
            for i in range(6, len(lines)):
                line = lines[i].split(" ")
                newList = []

                if "\t" in line[0]:
                    newList = line[0].split("\t")
                else:
                    for elem in line:
                        if len(elem) > 0:
                            newList.append(elem)

                for elem in newList:
                    if len(elem) < 1:
                        newList.remove(elem)

                node = nd.Node(idx, int(newList[7].split("\\")[0]), float(newList[1]), float(newList[2]))
                network.addNode(node)

                timeStart = stringToSec(newList[3])
                timeEnd = stringToSec(newList[4])

                if timeStart is None or timeEnd is None:
                    print(newList[3], newList[4], stringToSec(newList[3]), stringToSec(newList[4]))
                    print(newList)

                service_time = int(newList[5])
                quantity = float(newList[6])

                request = req.Request(idx, idx, timeStart, timeEnd, quantity, service_time)
                requests.append(request)

                idx += 1

            for i in range(len(requests) - 1):
                vehicle = vhc.Vehicle(0, 0, 0,
                                      capacity, total_number_of_stops)
                fleet.addVehicle(vehicle)

            dataset = data.Dataset(info, network, fleet, requests)
            matrix = dataset.generateMatrix(False)
            newFile = "benchmark/" + dataset.info.name + ".txt"
            dataset.writeFile(newFile, False)


def solomon():
    for filename in glob.glob(os.path.join(path, '*.xml')):
        with open(os.path.join(os.getcwd(), filename), 'r') as file:
            tree = et.parse(file)
            root = tree.getroot()

            info = None
            network = nw.Network()
            fleet = flt.Fleet()
            requests = []

            for child in root:
                if child.tag == "info":
                    info = inf.Info(child[0].text, child[1].text)
                    #print(f"Processing {info.name}")
                if child.tag == "network":
                    for i, treeNode in enumerate(child[0]):
                        node = nd.Node(treeNode.attrib["id"], treeNode.attrib["type"],
                                       treeNode[0].text, treeNode[1].text)
                        network.addNode(node)
                        if i == 0:
                            network.addNode(node)
                if child.tag == "fleet":
                    qty = int(child[0].attrib["number"])
                    depot_end = child[0][3].text
                    for _ in range(len(network.nodes) - 1):
                        vehicle = vhc.Vehicle(child[0].attrib["type"], child[0][0].text, child[0][1].text,
                                              child[0][2].text, child[0][3].text)
                        fleet.addVehicle(vehicle)
                if child.tag == "requests":
                    # depot
                    request = req.Request(0, 0, 0, depot_end, 9999.9, 0)
                    requests.append(request)
                    requests.append(request)
                    for i, basic_request in enumerate(child):
                        request = req.Request(basic_request.attrib["id"], basic_request.attrib["node"],
                                              basic_request[0][0].text, basic_request[0][1].text,
                                              basic_request[1].text, basic_request[2].text)
                        requests.append(request)
        dataset = data.Dataset(info, network, fleet, requests)
        matrix = dataset.generateMatrix(True)
        newFile = "converted/" + dataset.info.name + ".txt"
        dataset.writeFile(newFile, solomon)


def solomonValidator():
    jodah = []
    for j, filename in enumerate(glob.glob(os.path.join(path_test, '*.xml'))):
        for _ in range(1):
            with open(os.path.join(os.getcwd(), filename), 'r') as file:
                tree = et.parse(file)
                root = tree.getroot()

                x = []
                y = []
                tws = []
                twe = []
                q = []
                st = []

                info = None
                network = nw.Network()
                fleet = flt.Fleet()
                requests = []

                for child in root:
                    if child.tag == "info":
                        info = inf.Info(child[0].text, child[1].text)
                        # print(f"Processing {info.name}")
                    if child.tag == "network":
                        for i, treeNode in enumerate(child[0]):
                            x.append(treeNode[0].text)
                            y.append(treeNode[1].text)

                            node = nd.Node(treeNode.attrib["id"], treeNode.attrib["type"],
                                           treeNode[0].text, treeNode[1].text)
                            network.addNode(node)

                            if i == 0:
                                x.append(treeNode[0].text)
                                y.append(treeNode[1].text)

                                network.addNode(node)

                    if child.tag == "fleet":
                        capacity = child[0][2].text

                        for _ in range(len(network.nodes) - 1):
                            vehicle = vhc.Vehicle(child[0].attrib["type"], child[0][0].text, child[0][1].text,
                                                  child[0][2].text, child[0][3].text)
                            fleet.addVehicle(vehicle)

                    if child.tag == "requests":
                        # depot
                        tws.append(0)
                        tws.append(0)
                        twe.append(10000)
                        twe.append(10000)
                        q.append(0)
                        q.append(0)
                        # TODO: service time
                        st.append(0)
                        st.append(0)

                        request = req.Request(0, 0, 0, 10000, 9999.9, 0)
                        requests.append(request)
                        requests.append(request)

                        for i, basic_request in enumerate(child):
                            tws.append(basic_request[0][0].text)
                            twe.append(basic_request[0][1].text)
                            q.append(basic_request[1].text)
                            st.append(basic_request[2].text)

                            request = req.Request(basic_request.attrib["id"], basic_request.attrib["node"],
                                                  basic_request[0][0].text, basic_request[0][1].text,
                                                  basic_request[1].text, basic_request[2].text)
                            requests.append(request)

            dataset = data.Dataset(info, network, fleet, requests)
            matrix = dataset.generateMatrix(True)
            tmp = [matrix, x, y, tws, twe, q, st, capacity, info]
            jodah.append(tmp)
            print(len(x), len(y), len(tws), len(twe), len(q), len(st), len(matrix))

    for j, filename in enumerate(glob.glob(os.path.join(path_test_result, '*.txt'))):
        print(filename)
        with open(os.path.join(os.getcwd(), filename), 'r') as file:
            lines = file.readlines()
            vehicles = []
            for line in lines:
                if "$" in line:
                    vehicles.append(line.split(": ")[1].split(" "))
            for vehicle in vehicles:
                for i, node in enumerate(vehicle):
                    if "D" in node:
                        vehicle[i] = node[2:]
                    if "\n" in node:
                        vehicle.remove(node)
            jodah[j].append(vehicles)

    # TODO: jodah felépítése: [matrix, coord_x, coord_y, start, end, quantity, service time, capacity, info, vehicles]
    for grenzo in jodah:
        totaldistance = 0
        matrix = grenzo[0]
        x = grenzo[1]
        y = grenzo[2]
        start = grenzo[3]
        end = grenzo[4]
        quantity = grenzo[5]
        servicetime = grenzo[6]
        capacity = grenzo[7]
        info = grenzo[8]
        routes = grenzo[9]
        print(info.name)
        for route in routes:
            currtime = start[0]
            currcapacity = 0
            sumdistance = 0

            servicetime_ = float(servicetime[0])
            currtime = currtime + servicetime_

            for i in range(1, len(route)):
                travel = distance(matrix, route[i - 1], route[i])
                sumdistance += travel

                currtime += travel
                currtime = max(currtime, float(start[i]))

                if currtime > float(end[i]):
                    print(f"tw hiba {i} es {i-1} kozott")

                if int(route[i]) == 1:
                    currcapacity = 0
                else:
                    currcapacity += float(quantity[int(route[i])])
                    if currcapacity > float(capacity):
                        print(f"capacity {i} es {i - 1} kozott")

                servicetime_ = float(servicetime[int(route[i])])
                currtime += servicetime_

            totaldistance += sumdistance
        print(totaldistance)


def distance(matrix, i, j):
    return matrix[int(i)][int(j)]


now = time.localtime()
current_time = time.strftime("%H:%M:%S", now)
print(f"End: {current_time}")
