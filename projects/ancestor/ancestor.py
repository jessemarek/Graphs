from util import Queue


def earliest_ancestor(ancestors, starting_node):
    # init a lookup table to find a child's(keys) parents(values)
    relatives = {}
    # loop through ancestors list and build lookup table of child/parents
    for pair in ancestors:
        parent = pair[0]
        child = pair[1]
        # if child not already in relatives table
        if child not in relatives:
            # init the child to an empty list
            relatives[child] = []
        # add the parent to the list of relatives
        relatives[child].append(parent)

    # check if node is in lookup table
    if starting_node not in relatives:
        # if it isn't in table we don't have an ancestor for this child
        return -1

    # create a list to store all the possible paths
    paths = []

    # create a queue of paths to track the ancestory
    q = Queue()
    q.enqueue([starting_node])

    # while the queue is not empty
    while q.size() > 0:
        # look at first node in queue
        cur = q.dequeue()

        # if this node is in the lookup table it has ancestors
        if cur[-1] in relatives:
            # add the ancestors for this node to the queue
            for p in relatives[cur[-1]]:
                new_path = cur + [p]
                q.enqueue(new_path)
        # we have reached the end of a path
        else:
            new_path = cur[:]
            # store that path in our list
            paths.append(new_path)

    # determine the max len of every possible path in the paths
    max_len = max([len(path) for path in paths])

    # return the smallest number from list of paths matching the max length
    return min([path[-1] for path in paths if len(path) == max_len])


ancestors = [(1, 3), (2, 3), (3, 6), (5, 6), (5, 7),
             (4, 5), (4, 8), (8, 9), (11, 8), (10, 1)]
print(earliest_ancestor(ancestors, 6))
