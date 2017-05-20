# python3
from collections import deque

class Request:
    def __init__(self, arrival_time, process_time):
        self.arrival_time = arrival_time
        self.process_time = process_time


class Response:
    def __init__(self, dropped, start_time):
        self.dropped = True if dropped > 0 else False
        self.start_time = start_time


class Buffer:
    def __init__(self, size):
        self.size = size
        # finish_time for each packet placed in this buffer
        # should implement deque to be able to call last element in queue and to know its finish time
        self.finish_time_ = deque([])

    @property
    def is_full(self):
        if len(self.finish_time_) >= self.size:
            return True
        else:
            return False

    def remove_old(self, request):
        '''
            removes all old packets that their finish time is <= current incoming packet.
        '''
        while self.finish_time_:
            #if first element isn't <= incoming time then no other element will be.
            if self.finish_time_[0] <= request.arrival_time:
                self.finish_time_.pop(0)
            else:
                break

    @property
    def last_element(self):
        return self.finish_time_[-1]

    @property
    def is_empty(self):
        return True if len(self.finish_time_) == 0 else False


    def Process(self, request):
        """will recieve a request with given arrival time and processing time, you should check
            1- buffer availabilty: that buffer has free space len(buffer.finish_time_) < buffer.size
            2- buffer deallocation: for requests with buffer.finish_time.pop() <= request.arrival_time
            3- request dropping if no availble space or time at request.arrival_time
        """
        # refresh buffer
        self.remove_old(request)

        # check buffer availabilty
        if self.is_full:
            return Response(True, -1)

        # check if empty buffer
        if self.is_empty:
            # if only one packet to be inserted, finish_time list will start and finish within only those times.
            # if request.arrival_time == 2 & process_time == 2 then packet is to be processed on 2 and finish time is 4
            self.finish_time_ = [request.arrival_time + request.process_time]
            return Response(False, request.arrival_time)

        respon = Response(False, self.last_element)
        self.finish_time_.append(self.last_element + request.process_time)
        return respon


def ReadRequests(count):
    requests = []
    for i in range(count):
        arrival_time, process_time = map(int, input().strip().split())
        # list of pending requests
        requests.append(Request(arrival_time, process_time))
    return requests


def ProcessRequests(requests, buffer):
    responses = []
    for request in requests:
        responses.append(buffer.Process(request))
    return responses


def PrintResponses(responses):
    for response in responses:
        print(response.start_time if not response.dropped else -1)



if __name__ == "__main__":
    size, count = map(int, input().strip().split())

    # returns a list of pending requests each instance has two properties: .arrival_time & .process_time
    requests = ReadRequests(count)

    # intializes a buffer of given size that will hold to-be-processed packets. this instance has no .finish_time_ yet
    buffer = Buffer(size)

    # send pending requests with their corresponding buffer.
    responses = ProcessRequests(requests, buffer)

    PrintResponses(responses)

