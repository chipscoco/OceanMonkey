from oceanmonkey.core.queue import QueueType


def next_queue(queues):
    """
    :param queues: the first element of queues indicates the queue object's index in queues
    [1, queue, queue, queue]
    :return: a queue from queues with round robin
    """
    queues_length = len(queues)
    if queues[0] <= 0 or queues[0] >= queues_length:
        queues[0] = 1
    index = queues[0]
    queues[0] = queues[0] + 1 if queues[0] < queues_length else 1
    return queues[index] if queues_length > 1 else None

def all_queues(queues):
    for queue in queues[1:]:
        yield queue

