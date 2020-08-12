import random
from util import Queue


class User:
    def __init__(self, name):
        self.name = name


class SocialGraph:
    def __init__(self):
        self.last_id = 0
        self.users = {}
        self.friendships = {}

    def add_friendship(self, user_id, friend_id):
        """
        Creates a bi-directional friendship
        """
        if user_id == friend_id:
            print("WARNING: You cannot be friends with yourself")
        elif friend_id in self.friendships[user_id] or user_id in self.friendships[friend_id]:
            print("WARNING: Friendship already exists")
        else:
            self.friendships[user_id].add(friend_id)
            self.friendships[friend_id].add(user_id)

    def add_user(self, name):
        """
        Create a new user with a sequential integer ID
        """
        self.last_id += 1  # automatically increment the ID to assign the new user
        self.users[self.last_id] = User(name)
        self.friendships[self.last_id] = set()

    def populate_graph(self, num_users, avg_friendships):
        """
        Takes a number of users and an average number of friendships
        as arguments

        Creates that number of users and a randomly distributed friendships
        between those users.

        The number of users must be greater than the average number of friendships.
        """
        # Reset graph
        self.last_id = 0
        self.users = {}
        self.friendships = {}
        # !!!! IMPLEMENT ME

        # Add users
        for i in range(num_users):
            self.add_user(f"User {i}")

        # Create friendships
        possible = []

        for user_id in self.users:
            for friend_id in range(user_id + 1, self.last_id + 1):
                possible.append((user_id, friend_id))

        random.shuffle(possible)

        for i in range(num_users * avg_friendships // 2):
            friendships = possible[i]
            self.add_friendship(friendships[0], friendships[1])

    def get_all_social_paths(self, user_id):
        """
        Takes a user's user_id as an argument

        Returns a dictionary containing every user in that user's
        extended network with the shortest friendship path between them.

        The key is the friend's ID and the value is the path.
        """
        visited = {}  # Note that this is a dictionary, not a set
        # !!!! IMPLEMENT ME

        # create a queue to store the path we have traversed
        q = Queue()
        # init the queue with user id
        q.enqueue([user_id])

        # create the path through each users friend network
        while q.size() > 0:
            # path from starting point to cur user
            path = q.dequeue()
            # current user is at end of path
            user = path[-1]

            # if we haven't already visited this friend
            if user not in visited:
                # mark as visited with the path to get here
                visited[user] = path

                # look at this users friends to find friends of friends
                for friend in self.friendships[user]:
                    # create a new path to the firends of friends
                    new_path = path[:]
                    new_path.append(friend)
                    # add the new path to the queue to track the next degree of separation
                    q.enqueue(new_path)

        return visited


if __name__ == '__main__':
    sg = SocialGraph()
    sg.populate_graph(10, 2)
    print(sg.friendships)
    connections = sg.get_all_social_paths(1)
    print(connections)
