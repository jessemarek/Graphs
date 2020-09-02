"""
Simple graph implementation
"""
from util import Stack, Queue  # These may come in handy


class Graph:

    """Represent a graph as a dictionary of vertices mapping labels to
    edges."""

    def __init__(self):
        self.vertices = {}

    def add_vertex(self, vertex_id):
        """
        Add a vertex to the graph.
        """
        self.vertices[vertex_id] = set()

    def add_edge(self, v1, v2):
        """
        Add a directed edge to the graph.
        """
        if v1 in self.vertices and v2 in self.vertices:
            self.vertices[v1].add(v2)
        else:
            raise IndexError("nonexistant vertex")

    def get_neighbors(self, vertex_id):
        """
        Get all neighbors (edges) of a vertex.
        """
        return self.vertices[vertex_id]

    def bft(self, starting_vertex):
        """
        Print each vertex in breadth-first order
        beginning from starting_vertex.
        """
        # Create an empty queue
        q = Queue()
        # Add starting vertex ID
        q.enqueue(starting_vertex)
        # Create set for visited verts
        visited = set()
        # While queue is not empty
        while q.size() > 0:
            # Dequeue a vert
            v = q.dequeue()
            # If not visited
            if v not in visited:
                # Visit it!
                print(v)
                # Mark as visited
                visited.add(v)
                # Add all neighbors to the queue
                for neighbor in self.get_neighbors(v):
                    q.enqueue(neighbor)

    def dft(self, starting_vertex):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.
        """
        # Create an empty stack
        s = Stack()
        # Add starting vertex ID
        s.push(starting_vertex)
        # Create set for visited verts
        visited = set()
        # While stack is not empty
        while s.size() > 0:
            # pop a vert
            v = s.pop()
            # If not visited
            if v not in visited:
                # Visit it!
                print(v)
                # Mark as visited
                visited.add(v)
                # Add all neighbors to the stack
                for neighbor in self.get_neighbors(v):
                    s.push(neighbor)

    def dft_recursive(self, starting_vertex, visited=None):
        """
        Print each vertex in depth-first order
        beginning from starting_vertex.

        This should be done using recursion.
        """
        if visited is None:
            visited = set()
        # print the vert when we visit
        print(starting_vertex)
        # add the vert to the visited set
        visited.add(starting_vertex)
        # continue traversing the verts in our graph
        for v in self.vertices[starting_vertex]:
            # if we haven't visited it yet
            if v not in visited:
                # recurse and visit
                self.dft_recursive(v, visited)

    def bfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing the shortest path from
        starting_vertex to destination_vertex in
        breath-first order.
        """
        # Create an empty queue and enqueue A PATH TO the starting vertex ID
        q = Queue()

        q.enqueue([starting_vertex])
        # Create a Set to store visited vertices
        visited = set()
        # While the queue is not empty...
        while q.size() > 0:
            # Dequeue the first PATH
            v = q.dequeue()
            # Grab the last vertex from the PATH
            last = v[-1]
            # If that vertex has not been visited...
            if last not in visited:
                # CHECK IF IT'S THE TARGET
                if last == destination_vertex:
                    # IF SO, RETURN PATH
                    return v
            # Mark it as visited...
            visited.add(last)
            # Then add A PATH TO its neighbors to the back of the queue
            for neighbor in self.get_neighbors(last):
                # COPY THE PATH
                path = v.copy()
                # APPEND THE NEIGHOR TO THE BACK
                path.append(neighbor)
                # ADD the new path to the queue
                q.enqueue(path)

        return None

    def dfs(self, starting_vertex, destination_vertex):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.
        """
        # Create an empty stack and push A PATH TO the starting vertex ID
        s = Stack()

        s.push([starting_vertex])
        # Create a Set to store visited vertices
        visited = set()
        # While the stack is not empty...
        while s.size() > 0:
            # pop the top PATH
            v = s.pop()
            # Grab the last vertex from the PATH
            last = v[-1]
            # If that vertex has not been visited...
            if last not in visited:
                # CHECK IF IT'S THE TARGET
                if last == destination_vertex:
                    # IF SO, RETURN PATH
                    return v
            # Mark it as visited...
            visited.add(last)
            # Then add A PATH TO its neighbors to the top of the stack
            for neighbor in self.get_neighbors(last):
                # COPY THE PATH
                path = v.copy()
                # APPEND THE NEIGHOR TO THE BACK
                path.append(neighbor)
                # ADD the new path to the stack
                s.push(path)

    def dfs_recursive(self, starting_vertex, destination_vertex, visited=None, path=None):
        """
        Return a list containing a path from
        starting_vertex to destination_vertex in
        depth-first order.

        This should be done using recursion.
        """
        # keep track of visited verts
        if visited is None:
            visited = set()
        # store the target path
        if path is None:
            path = []
        # mark the current vert as visited
        visited.add(starting_vertex)
        # copy the path and add the current vert to the end
        path = path[:]
        path.append(starting_vertex)
        # check if we are at the destination vert
        if starting_vertex == destination_vertex:
            return path
        # we need to keep searching, visit the neighbors of the vert
        for n in self.get_neighbors(starting_vertex):
            if n not in visited:
                # store the next recursive call as a new path
                new_path = self.dfs_recursive(
                    n, destination_vertex, visited, path)
                # if we don't find a deadend return the path to the prev call
                if new_path is not None:
                    return new_path
        # deadend and no target found, return None
        return None

        """
        # keep track of visited verts
        visited = set()
        # store the target path
        target_path = None

        def find_path(path):
            # cur vert at end of path
            vertex = path[-1]
            nonlocal target_path
            nonlocal visited
            # if vert is not yet visited
            if vertex not in visited:
                # mark vert as visited
                visited.add(vertex)
                # check to see if vert is our destination
                if vertex == destination_vertex:
                    # if it is set the target path to the path
                    target_path = path
                else:
                    # otherwise keep searching other verts
                    for v in self.vertices[vertex]:
                        new_path = path.copy()
                        new_path.append(v)
                        find_path(new_path)
        # recursively search for target path
        find_path([starting_vertex])

        return target_path
        """


if __name__ == '__main__':
    graph = Graph()  # Instantiate your graph
    # https://github.com/LambdaSchool/Graphs/blob/master/objectives/breadth-first-search/img/bfs-visit-order.png
    graph.add_vertex(1)
    graph.add_vertex(2)
    graph.add_vertex(3)
    graph.add_vertex(4)
    graph.add_vertex(5)
    graph.add_vertex(6)
    graph.add_vertex(7)
    graph.add_edge(5, 3)
    graph.add_edge(6, 3)
    graph.add_edge(7, 1)
    graph.add_edge(4, 7)
    graph.add_edge(1, 2)
    graph.add_edge(7, 6)
    graph.add_edge(2, 4)
    graph.add_edge(3, 5)
    graph.add_edge(2, 3)
    graph.add_edge(4, 6)

    '''
    Should print:
        {1: {2}, 2: {3, 4}, 3: {5}, 4: {6, 7}, 5: {3}, 6: {3}, 7: {1, 6}}
    '''
    print(graph.vertices)

    '''
    Valid BFT paths:
        1, 2, 3, 4, 5, 6, 7
        1, 2, 3, 4, 5, 7, 6
        1, 2, 3, 4, 6, 7, 5
        1, 2, 3, 4, 6, 5, 7
        1, 2, 3, 4, 7, 6, 5
        1, 2, 3, 4, 7, 5, 6
        1, 2, 4, 3, 5, 6, 7
        1, 2, 4, 3, 5, 7, 6
        1, 2, 4, 3, 6, 7, 5
        1, 2, 4, 3, 6, 5, 7
        1, 2, 4, 3, 7, 6, 5
        1, 2, 4, 3, 7, 5, 6
    '''
    graph.bft(1)

    '''
    Valid DFT paths:
        1, 2, 3, 5, 4, 6, 7
        1, 2, 3, 5, 4, 7, 6
        1, 2, 4, 7, 6, 3, 5
        1, 2, 4, 6, 3, 5, 7
    '''
    graph.dft(1)
    graph.dft_recursive(1)

    '''
    Valid BFS path:
        [1, 2, 4, 6]
    '''
    print(graph.bfs(1, 6))

    '''
    Valid DFS paths:
        [1, 2, 4, 6]
        [1, 2, 4, 7, 6]
    '''
    print(graph.dfs(1, 6))
    print(graph.dfs_recursive(1, 6))
