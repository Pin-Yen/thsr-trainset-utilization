class Train(object):
    """docstring for Train"""
    def __init__(self):
        self.train_no = None
        self.origin = None
        self.origin_time = None
        self.start_time = None
        self.dest = None
        self.dest_time = None
        self.end_time = None
        self.in_service = None
        self.top_node = None
        self.bottom_node = None
        self.conflict_trains = []

        ## assigned by rostering algorithm
        self.prev_train = None
        self.next_train = None

    def can_be_next(self, next_train):
        return (self.dest == next_train.origin)\
         and (self.end_time <= next_train.start_time)\
         and (self.in_service or (self.origin != next_train.dest))

    def approx_can_be_next(self, next_train):
        position_time_matrix = {'NAG' : {'TAC' : 60, 'ZUY' : 110}\
        , 'TAC' : {'NAG' : 60, 'ZUY' : 50}, 'ZUY' : {'NAG':110, 'TAC' : 50}}
        if (self.dest == next_train.origin) and (self.end_time <= next_train.start_time):
            return True
        if (self.dest not in position_time_matrix\
         or next_train.origin not in position_time_matrix[self.dest]):
            return False

        return self.end_time + position_time_matrix[self.dest][next_train.origin] <= next_train.start_time