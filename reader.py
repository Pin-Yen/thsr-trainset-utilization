from train import *

class PrepareTime(object):
    PRE_TIME = {'NAG' : 0, 'TPE' : 0, 'TAC' : 15, 'ZUY' : 0}
    POST_TIME = {'NAG' : 15, 'TPE' : 15, 'TAC' : 15, 'ZUY' : 15}

    def pre_time(station):
        return PrepareTime.PRE_TIME[station]

    def post_time(station):
        return PrepareTime.POST_TIME[station]
        
def to_minutes(hh_mm):
    return 60*int(hh_mm[:2]) + int(hh_mm[3:5])

def read_service_trains(file_name):
    train_list = []

    with open(file_name) as f:
        for line in f:
            train_no, origin, origin_time, dest, dest_time\
             = line.split(' ')

            origin_time = to_minutes(origin_time)
            dest_time = to_minutes(dest_time)

            train = Train()
            train.train_no = train_no
            train.origin = origin
            train.origin_time = origin_time
            train.dest = dest
            train.dest_time = dest_time
            train.start_time = origin_time - PrepareTime.pre_time(origin)
            train.end_time = dest_time + PrepareTime.post_time(dest)
            train.in_service = True

            train_list.append(train)

    return train_list

def read_positioning_trains(file_name):
    train_list = []

    with open(file_name) as f:
        for line in f:
            train_no, origin, origin_time, dest, dest_time\
             = line.split(' ')[0:5]

            origin_time = to_minutes(origin_time)
            dest_time = to_minutes(dest_time)

            train = Train()
            train.train_no = train_no
            train.origin = origin
            train.origin_time = origin_time
            train.start_time = origin_time
            train.dest = dest
            train.dest_time = dest_time
            train.end_time = dest_time
            train.in_service = False
            train.conflict_trains = line.split(' ')[5:]
            train_list.append(train)

    return train_list
