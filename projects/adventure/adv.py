from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
# map_file = "maps/main_maze.txt"

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


def traverse_maze(prev_room=None, dir_moved=None):
    # get current room number
    room = player.current_room.id
    # check map to see if we've been in this room before
    if room not in maze_map:
        # add room to map and init the exits for this room as none
        maze_map[room] = {'n': None, 'e': None, 's': None, 'w': None}
    # get the exits to this room
    exits = player.current_room.get_exits()
    # update the exits for the current room in the map
    for e in exits:
        if maze_map[room][e] is None:
            maze_map[room][e] = '?'
    # pick a direction to travel
    print(f"Map Rooms: {maze_map}")
    # travel that way.
    # update map with previous room and direction travelled


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
