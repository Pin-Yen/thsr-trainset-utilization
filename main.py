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

    # number of nodes =  (source + sink) + 2*(number_of_service_train + number_of_positioning_train)
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

        
        next_positioning_trains = list(filter(lambda t: train.can_be_next(t), positioning_trains))

        if next_positioning_trains:
            next_positioning_train = min(next_positioning_trains, key=lambda t: t.origin_time)
            graph.link(train.bottom_node, next_positioning_train.top_node)


    original_graph = copy.deepcopy(graph)
    flow = ford_fulkerson(graph)
    required_trainsets = len(service_trains) - flow
    print("Required trainsets:", required_trainsets)

    rosters = create_roster(service_trains, positioning_trains, original_graph, graph)

    print('roster = ' + json.dumps(rosters))

def create_roster(service_trains, positioning_trains, original_graph, residual_graph):
    
    ## First, chain trains together according to original graph and residual graph.
    for u in range(2, original_graph.size):
        for v in range(2, original_graph.size):
            if original_graph.matrix[u][v] == 1 and residual_graph.matrix[u][v] == 0:
                first_train = residual_graph.node_to_train[u]
                second_train = residual_graph.node_to_train[v]

                # chain trains together
                if not first_train == second_train:
                    first_train.next_train = second_train
                    second_train.prev_train = first_train
    modified = True
    while modified:
        modified = False
        enforce_fifo(service_trains, positioning_trains)
        modified = enforce_no_idle(positioning_trains)


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


def enforce_fifo(service_trains, positioning_trains):
    modified = False

    all_trains = service_trains + positioning_trains
    trains_by_origin = sorted(all_trains, key=lambda t: t.origin_time)
    trains_by_dest = sorted(all_trains, key=lambda t: t.dest_time)

    for train in trains_by_dest:
        # TODO: use only service trains and selected non-revenue trains instead of all trains
        if train.next_train == None:
            continue

        next_candidates = list(filter(lambda t: train.can_be_next(t), trains_by_origin))

        if not next_candidates:
            continue

        for next_candidate in next_candidates:
            if not next_candidate.prev_train:
                continue
            if next_candidate.origin_time >= train.next_train.origin_time:
                break
            else:
                if next_candidate.prev_train.dest_time > train.dest_time:
                    # train & next_candidate.prev_train violates FIFO principle
                    # swap
                    modified = True
                    parent1, parent2 = train, next_candidate.prev_train
                    child1 ,child2 = train.next_train, next_candidate
                    print('swap !!!')
                    print(parent1.train_no, parent1.dest_time, '-> (new)', child2.train_no, child2.origin_time)
                    print(parent2.train_no, parent2.dest_time, '-> (new)', child1.train_no, child1.origin_time)
                    # i = input('.')
                    # parent1.swap = True
                    # parent2.swap = True

                    parent1.next_train = child2
                    child2.prev_train = parent1
                    parent2.next_train = child1
                    child1.prev_train = parent2
                    break
    return modified


def enforce_no_idle(positioning_trains):
    modified = False

    positioning_trains = sorted(positioning_trains, key=lambda t: t.origin_time)
    
    for train in positioning_trains:
        # If next train is also a positioning train, make sure it is the earilst one
        if not train.next_train:
            continue
        if not train.next_train.in_service:
            can_be_next_positioning = list(filter(lambda t: train.can_be_next(t), positioning_trains))
            if train.next_train != can_be_next_positioning[0]:
                for next_train_candidate in can_be_next_positioning:
                    if next_train_candidate == train.next_train:
                        break
                    if not next_train_candidate.prev_train:
                        # swap
                        modified = True
                        old_next_train = train.next_train
                        train.next_train = next_train_candidate
                        next_train_candidate.prev_train = train
                        next_train_candidate.next_train = old_next_train.next_train
                        old_next_train.next_train = None
                        old_next_train.prev_train = None
                        break

    return modified


if __name__ == '__main__':
    if (len(sys.argv) < 3):
        print("please specify timetable & positioning_trains as arguments")
    else:
        main()