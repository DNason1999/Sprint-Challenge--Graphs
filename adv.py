from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

from collections import deque

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
#map_file = "maps/test_line.txt"
#map_file = "maps/test_cross.txt"
#map_file = "maps/test_loop.txt"
#map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

#opposite_dir = {'n':'s','e':'w','s':'n','w':'e'}

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
traversal_path = []

next_rooms = []
# Create a double ended queue
unvisited = list(range(0,len(world.rooms)))
# Append the starting room to the deque
next_room = world.rooms[unvisited[0]]
unvisited.remove(player.current_room.id)
# While the deque is not empty, loop
while len(unvisited) > 0:
    next_rooms.append(next_room)
    s_d = deque()

    s_visited = set()

    s_d.append([next_room])

    while len(s_d) > 0:
        s_path = s_d.popleft()

        s_last = s_path[-1]
        if s_last.id in unvisited:
            c_room = s_path[0]
            for room in s_path[1:]:
                dic = {}
                for x in world.rooms[c_room.id].get_exits():
                    dic[x] = world.rooms[c_room.id].get_room_in_direction(x).id
                inverted_dict = {v:k for k,v in dic.items()}
                traversal_path.append(inverted_dict[room.id])
                c_room = room
            unvisited.remove(s_last.id)
            next_room = s_last
            break

        else:
            s_visited.add(s_last.id)
            if s_last not in unvisited:
                for direction in world.rooms[s_last.id].get_exits():
                    s_room_in_dir = s_last.get_room_in_direction(direction)
                    if s_room_in_dir.id not in s_visited:
                        s_d.append(s_path+[s_room_in_dir])


# print(len(traversal_path))

# next_rooms = [x.id for x in next_rooms]
# print(next_rooms)

# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")
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
