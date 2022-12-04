import node as nd


class Network:
    def __init__(self):
        self.nodes = []

    def addNode(self, node):
        if isinstance(node, nd.Node):
            self.nodes.append(node)
        else:
            raise Exception("Wrong parameter type!")

    def nodes(self):
        for node in self.nodes:
            print(node.print())
