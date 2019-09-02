from fordfulkerson import *
from reader import *
from train import *
import sys
import copy
import json

class NodeCounter(object):

    def __init__(self):
        self.number = -1

    def next_number(self):
        self.number += 1
        return self.number
    
    def number_of_nodes(self):
        return self.number + 1

class TrainGraph(Graph):
    
    def __init__(self, matrix, s, t):
        super().__init__(matrix, s, t)
        # maintains a mapping of node number to train
        self.node_to_train = [None for _ in range(self.size)]

    def map_train(self, node_number, train):
        # Binds train to corresponding node numbers.
        self.node_to_train[node_number] = train

class Roster(object):

    def __init__(self):
        # list of train services included in this roster, ordered.
        self.duty_list = []

    def add_duty(self, train):
        # Add train to roster.
        self.duty_list.append(train)

    def pretty_print(self):
        pass

    def json(self):
        def readable_time(minute):
            return str(minute//60) + ":" + str(minute%60)

        roster_json = []
        for train in self.duty_list:
            duty = {
                "originTime" : readable_time(train.origin_time),
                "destTime" : readable_time(train.dest_time),
                "originStation" : train.origin,
                "destStation": train.dest,
                "trainNo": train.train_no,
                "direction": int(train.train_no) % 2,
                "revenueService": train.in_service,
            }
            roster_json.append(duty)

        return roster_json

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

    source = node_counter.next_number()
    sink = node_counter.next_number()

    service_trains = read_service_trains('data/' + sys.argv[1])
    positioning_trains = read_positioning_trains('data/' + sys.argv[2])

    positioning_trains = remove_conflict_positioning_trains(service_trains, positioning_trains)

    # number of nodes =  (source + sink) + 2*number_of_trains
    number_of_nodes = 2 + 2*(len(service_trains) + len(positioning_trains))
   
    graph = TrainGraph([[0 for _ in range(number_of_nodes)] for _ in range(number_of_nodes)], 0, 1)

    # assign node numbers
    for train in service_trains + positioning_trains:
        train.top_node = node_counter.next_number()
        train.bottom_node = node_counter.next_number()
        graph.map_train(train.top_node, train)
        graph.map_train(train.bottom_node, train)

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

    original_graph = copy.deepcopy(graph)
    flow = ford_fulkerson(graph)
    required_trainsets = len(service_trains) - flow
    print("Required trainsets:", required_trainsets)

    rosters = create_roster(service_trains, original_graph, graph)

    print('roster = ' + json.dumps(rosters))

def create_roster(service_trains, original_graph, residual_graph):
    
    ## First, chain trains together according to original graph and residual graph.
    for u in range(2, original_graph.size):
        for v in range(2, original_graph.size):
            if original_graph.matrix[u][v] == 1 and residual_graph.matrix[u][v] == 0:
                first_train = residual_graph.node_to_train[u]
                second_train = residual_graph.node_to_train[v]

                # chain trains together
                first_train.next_train = second_train
                second_train.prev_train = first_train
    

    ## Second, collect the "chain-of-trains"
    rosters = []

    for train in service_trains:  # TODO: add positioning trains
        if train.prev_train == None:
            # this is the first train, trace all following trains
            
            roster = Roster()
            roster.add_duty(train)
            
            next_train = train.next_train
            while next_train:
                roster.add_duty(next_train)
                next_train = next_train.next_train


            rosters.append(roster.json())

    return rosters


# def enforce_fifo(train_list):
#     for train in 

if __name__ == '__main__':
    if (len(sys.argv) < 3):
        print("please specify timetable & positioning_trains as arguments")
    else:
        main()