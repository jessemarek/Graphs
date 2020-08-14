from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

from util import Stack, Queue

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
# map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph = literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

##############################################
#               MAZE TRAVERSAL               #
##############################################

# will store rooms with a dict of the directions of
# exits and what rooms are in that direction
# ex: { 0: {'n': '?', 'e': 5, 's': 2, 'w': None} }
maze_map = {}

# dict with directions(keys) and the opposite direction(values)
opp_dir = {'n': 's', 'e': 'w', 's': 'n', 'w': 'e'}


# get the shortest path from a deadend to a room with an unexplored exit
def get_path(start):
    # list to store the path to backtrack
    route = []
    # create a queue to hold paths for a BFS
    q = Queue()
    q.enqueue([start])
    # set to keep track of rooms we have already visited
    visited = set()

    while q.size() > 0:
        # get path from front of queue
        path = q.dequeue()
        # get the last room in the path to check adjacent rooms
        last = path[-1]
        # if we haven't visited this room yet
        if last in visited:
            continue
        # check to see if its a room with unexplored exits
        if '?' in maze_map[last].values():
            # if it is then we need to convert the rooms in the path
            # to directions to travel in order to get there
            for i in range(len(path)-1):
                for k, v in maze_map[path[i]].items():
                    if v == path[i+1]:
                        route.append(k)
            # return the path
            return route
        # mark room as visited
        visited.add(last)
        # look at the current room and add any explored neighbors to the search
        for k, v in maze_map[last].items():
            # copy the current path up to this point
            new_path = path[:]
            # add the next room to search to the new path
            new_path.append(v)
            # add the new path to our queue
            q.enqueue(new_path)


def traverse_maze():
    # keep track of the number of unexplored exits we encounter
    unexplored = 0
    prev_room = None
    dir_moved = None
    backtracked = False
    # create a stack to keep track of our path
    s = Stack()
    # init stack with the path
    s.push('n')

    while s.size() > 0:
        # get the current room
        room = player.current_room.id
        # get the exits for the current room
        exits = player.current_room.get_exits()

        # if the current room is not in the map record it
        if room not in maze_map:
            # init the current room exits to None
            maze_map[room] = {}

        # update the current rooms exits
        for e in exits:
            # if the exit isn't marked
            if e not in maze_map[room]:
                # set it as '?'
                maze_map[room][e] = '?'
                # increment the unexplored exits
                unexplored += 1
            # if we made a move check if the rooms are marked as connected
        for e in exits:
            if prev_room is not None and prev_room in maze_map:
                # if not already marked as connected record that in maze map
                if maze_map[room][opp_dir[dir_moved]] == '?':
                    maze_map[prev_room][dir_moved] = room
                    maze_map[room][opp_dir[dir_moved]] = prev_room
                    # decrement the unexplored exits
                    unexplored -= 2
            # if we haven't yet explored this way do so
        for e in exits:
            if maze_map[room][e] == '?':
                # add the direction of the exit to the stack
                s.push(e)
        # break out of the loop once every room has been visited
        if unexplored == 0:
            break

        # check to see if this room is a deadend and backtrack
        # to nearest room with an unexplored exit if so
        deadend = [v for k, v in maze_map[room].items() if v == '?']
        if '?' not in deadend:
            backtrack = get_path(room)
            traversal_path.extend(backtrack)
            for direction in backtrack:
                player.travel(direction)

        if backtracked:
            backtracked = False
            room = player.current_room.id

        # grab the path off the top of the stack
        path = s.pop()
        # store current room as the prev room
        # (it will be prev after travel)
        prev_room = player.current_room.id
        # get direction of travel
        dir_moved = direction = path[0]
        # move one room in direction
        player.travel(direction)
        # record movement in traversal path
        traversal_path.append(direction)


traverse_maze()


##############################################

# TRAVERSAL TEST
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(
        f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
