# Course: CS261 - Data Structures
# Author: Ru Yang
# Assignment: 6
# Description: This program contains a DirectedGraph class. It designed to support the following type of graph:
#              directed, weighted (positive edge weights only), no duplicate edges, no loops. Cycles are allowed.
#              The implementation will include the following methods: add_vertex(), add_edge(), remove_edge(), 
#              get_vertices(), get_edges(), is_valid_path(), dfs(), ​bfs(), has_cycle(), and dijkstra().


import heapq
from collections import deque

class DirectedGraph:
    """
    Class to implement directed weighted graph
    - duplicate edges not allowed
    - loops not allowed
    - only positive edge weights
    - vertex names are integers
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency matrix
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.v_count = 0
        self.adj_matrix = []

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            v_count = 0
            for u, v, _ in start_edges:
                v_count = max(v_count, u, v)
            for _ in range(v_count + 1):
                self.add_vertex()
            for u, v, weight in start_edges:
                self.add_edge(u, v, weight)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if self.v_count == 0:
            return 'EMPTY GRAPH\n'
        out = '   |'
        out += ' '.join(['{:2}'.format(i) for i in range(self.v_count)]) + '\n'
        out += '-' * (self.v_count * 3 + 3) + '\n'
        for i in range(self.v_count):
            row = self.adj_matrix[i]
            out += '{:2} |'.format(i)
            out += ' '.join(['{:2}'.format(w) for w in row]) + '\n'
        out = f"GRAPH ({self.v_count} vertices):\n{out}"
        return out

    # ------------------------------------------------------------------ #

    def add_vertex(self) -> int:
        """
        Adds a new vertex to the graph. The vetex will be assigned a reference index.
        Then the method returns this index number.
        """
        new_vertex = []
        for _ in range(self.v_count):
            new_vertex.append(0)
            
        self.adj_matrix.append(new_vertex)
        self.v_count += 1
        
        for vertex in self.adj_matrix:
            vertex.append(0)
        return self.v_count
        

    def add_edge(self, src: int, dst: int, weight=1) -> None:
        """
        Adds a new edge to the graph. If either or both vertex indices do not exist 
        in the graph, or if the weight is not a positive integer, or if src and dst 
        refer to the same vertex, do nothing. If an edge already exists, update its weight.
        """
        if weight < 0:            # Input weight is not a positive integer.
            return 
        if src == dst:            # src and dst refer to the same vertex.
            return
        if src not in range(self.v_count) or dst not in range(self.v_count):        # src and dst is invalid.
            return 
        self.adj_matrix[src][dst] = weight         # Connecting two vertices.
        

    def remove_edge(self, src: int, dst: int) -> None:
        """
        Removes an edge between two vertices. If either or both vertex indices do not exist 
        or if there is no edge between them, do nothing.
        """
        if src not in range(self.v_count) or dst not in range(self.v_count):        # src and dst is invalid.
            return 
        self.adj_matrix[src][dst] = 0
    

    def get_vertices(self) -> []:
        """
        Returns a list of vertices of the graph.
        """
        result = []
        for index in range(self.v_count):
            result.append(index)
        return result
    

    def get_edges(self) -> []:
        """
        Returns a list of edges in the graph by the form tuple(src, dst, weight).
        """
        result = []
        for src in range(self.v_count):
            for dst in range(self.v_count):
                if self.adj_matrix[src][dst] != 0:
                    result.append((src, dst, self.adj_matrix[src][dst]))
        return result   
      

    def is_valid_path(self, path: []) -> bool:
        """
        Takes a list of vertex indices and returns True if the sequence is vertices 
        represents a valid path in the graph. Empty path is considered valid.
        """
        # Empty path.
        if len(path) == 0:            
            return True
        
        # One vertex in path.
        if len(path) == 1:               
           if 0 <= path[0] < self.v_count:
               return True
           return False

        # More than one vertex.
        for index in range(len(path) - 1):
            src, dst = path[index], path[index + 1]
            if src in range(self.v_count) and dst in range(self.v_count):
                if self.adj_matrix[src][dst] == 0:
                    return False
            else:
                return False
        return True
    

    def dfs(self, v_start, v_end=None) -> []:
        """
        Performs a DFS in the graph and returns a list of vertices visited during the search.
        If starting vertex in invalid, returns an empty list. If end vertex is invalid, the 
        search should be done as no end vertex.
        """
        visited = []
        if v_start in range(self.v_count):
            wait = [v_start]
            while len(wait) != 0:
                temp = wait.pop(0)
                if temp not in visited:
                    visited.append(temp)
                    if temp == v_end:
                        return visited
                    temp_list = []
                    for next_vertex in range(self.v_count):
                        if self.adj_matrix[temp][next_vertex] != 0:
                            temp_list.append(next_vertex)
                        temp_list.sort()
                        wait = temp_list + wait
        return visited
    

    def bfs(self, v_start, v_end=None) -> []:
        """
        Performs a BFS in the graph and returns a list 
        of vertices visited during the search.
        """
        visited = []
        if v_start in range(self.v_count):
            wait = [v_start]
            while len(wait) != 0:
                temp = wait.pop(0)
                if temp not in visited:
                    visited.append(temp)
                    if temp == v_end:
                        return visited
                    temp_list = []
                    for next_vertex in range(self.v_count):
                        if self.adj_matrix[temp][next_vertex] != 0:
                            temp_list.append(next_vertex)
                        temp_list.sort()
                        wait = wait + temp_list
        return visited                
    

    def has_cycle(self):
        """
        Return True if there is at least one 
        cycle in the graph, else return False.
        """
        visited = []
        rec_stack = []
        for vertex in range(self.v_count):
            if vertex not in visited:
                if self.has_cycle_helper(vertex, visited, rec_stack):
                    return True
        return False
    
    def has_cycle_helper(self, vertex, visited, rec_stack):
        """The helper function for has_cycle()."""
        visited.append(vertex)
        rec_stack.append(vertex)
        for next_vertex in range(self.v_count):
            if next_vertex not in visited and self.adj_matrix[vertex][next_vertex] != 0:
                if self.has_cycle_helper(next_vertex, visited, rec_stack):
                    return True
            elif next_vertex in rec_stack and self.adj_matrix[vertex][next_vertex] != 0:
                return True
        rec_stack.pop()
        return False
    

    def dijkstra(self, src: int) -> []:
        """
        This method implements the Dijkstra algorithm to compute the length of 
        the shortest path from a given vertex to all other vertices in the graph.
        """
        visited = {}
        heap_queue = [[0, src]]
        while heap_queue:
            vertex = heapq.heappop(heap_queue)
            if vertex[1] not in visited:
                visited[vertex[1]] = vertex[0]
                for next_vertex in range(self.v_count):
                    distance = self.adj_matrix[vertex[1]][next_vertex]
                    if distance != 0:
                        heapq.heappush(heap_queue, [distance + vertex[0], next_vertex])
        result = []
        for vertex in range(self.v_count):
            if vertex in visited:
                result.append(visited[vertex])
            else:
                result.append(float('inf'))
        return result


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = DirectedGraph()
    print(g)
    for _ in range(5):
        g.add_vertex()
    print(g)

    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    for src, dst, weight in edges:
        g.add_edge(src, dst, weight)
    print(g)


    print("\nPDF - method get_edges() example 1")
    print("----------------------------------")
    g = DirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    test_cases = [[0, 1, 4, 3], [1, 3, 2, 1], [0, 4], [4, 0], [], [2]]
    for path in test_cases:
        print(path, g.is_valid_path(path))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for start in range(5):
        print(f'{start} DFS:{g.dfs(start)} BFS:{g.bfs(start)}')


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)

    edges_to_remove = [(3, 1), (4, 0), (3, 2)]
    for src, dst in edges_to_remove:
        g.remove_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')

    edges_to_add = [(4, 3), (2, 3), (1, 3), (4, 0)]
    for src, dst in edges_to_add:
        g.add_edge(src, dst)
        print(g.get_edges(), g.has_cycle(), sep='\n')
    print('\n', g)


    print("\nPDF - dijkstra() example 1")
    print("--------------------------")
    edges = [(0, 1, 10), (4, 0, 12), (1, 4, 15), (4, 3, 3),
             (3, 1, 5), (2, 1, 23), (3, 2, 7)]
    g = DirectedGraph(edges)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
    g.remove_edge(4, 3)
    print('\n', g)
    for i in range(5):
        print(f'DIJKSTRA {i} {g.dijkstra(i)}')
