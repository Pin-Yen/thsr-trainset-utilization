from fordfulkerson import *
from reader import *
from train import *
import sys

class NodeCounter(object):

    def __init__(self):
        self.number = -1

    def next_number(self):
        self.number += 1
        return self.number
    
    def number_of_nodes(self):
        return self.number + 1

def remove_conflict_positioning_trains(service_trains, positioning_trains):
    def has_conflict(positioning_train, service_train_set):
        for conflict_train in positioning_train.conflict_trains:
            if conflict_train in service_train_set:
                return True
        return False

    service_train_set = set([t.train_no for t in service_trains])
    return list(filter(lambda t: not has_conflict(t, service_train_set), positioning_trains))

def main():
    node_counter = NodeCounter()
    source, sink = node_counter.next_number(), node_counter.next_number()

    service_trains = read_service_trains('data/' + sys.argv[1])
    positioning_trains = read_positioning_trains('data/' + sys.argv[2])

    positioning_trains = remove_conflict_positioning_trains(service_trains, positioning_trains)

    # assign node numbers
    for train in service_trains + positioning_trains:
        train.top_node = node_counter.next_number()
        train.bottom_node = node_counter. next_number()

    number_of_nodes = node_counter.number_of_nodes()
    graph = Graph([[0 for _ in range(number_of_nodes)] for _ in range(number_of_nodes)], 0, 1)

    for train in service_trains:
        graph.link(source, train.top_node)
        graph.link(train.bottom_node, sink)

        for next_train in filter(lambda t: train.can_be_next(t), service_trains):
            graph.link(train.top_node, next_train.bottom_node)

        for next_train in filter(lambda t: train.can_be_next(t), positioning_trains):
            graph.link(train.top_node, next_train.top_node)

    for train in positioning_trains:
        graph.link(train.top_node, train.bottom_node)

        for next_train in filter(lambda t: train.can_be_next(t), service_trains):
            graph.link(train.bottom_node, next_train.bottom_node)

        for next_train in filter(lambda t: train.can_be_next(t), positioning_trains):
            graph.link(train.bottom_node, next_train.top_node)

    flow = ford_fulkerson(graph)
    required_trainsets = len(service_trains) - flow
    print("Required trainsets:", required_trainsets)


if __name__ == '__main__':
    if (len(sys.argv) < 3):
        print("please specify timetable & positioning_trains as arguments")
    else:
        main()