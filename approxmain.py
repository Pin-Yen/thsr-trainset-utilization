from fordfulkerson import *
from reader import *
from train import *
import sys
class NodeCounter(object):
    """docstring for NodeCounter"""
    def __init__(self):
        self.number = -1

    def next_number(self):
        self.number += 1
        return self.number
    
    def number_of_nodes(self):
        return self.number + 1


def main():
    node_counter = NodeCounter()
    source, sink = node_counter.next_number(), node_counter.next_number()

    service_trains = read_service_trains('data/' + sys.argv[1])


    # assign node numbers
    for train in service_trains:
        train.top_node = node_counter.next_number()
        train.bottom_node = node_counter. next_number()

    number_of_nodes = node_counter.number_of_nodes()
    graph = Graph([[0 for _ in range(number_of_nodes)] for _ in range(number_of_nodes)], 0, 1)

    for train in service_trains:
        graph.link(source, train.top_node)
        graph.link(train.bottom_node, sink)

        for next_train in filter(lambda t: train.approx_can_be_next(t), service_trains):
            graph.link(train.top_node, next_train.bottom_node)

    flow = ford_fulkerson(graph)
    required_trainsets = len(service_trains) - flow
    print("Required trainsets:", required_trainsets)


if __name__ == '__main__':
    if (len(sys.argv) < 2):
        print("please specify timetable as argument")
    else:
        main()