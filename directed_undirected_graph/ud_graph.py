# Course: CS261
# Author: Ru Yang
# Assignment: 6
# Description: The program includes a UndirectedGraphclass. It designed to support
#              the following type of graph: undirected, unweighted, no duplicate edges, 
#              no loops and cycles are allowed. The implementation includes add_vertex(), 
#              add_edge(), remove_edge(), remove_vertex(),  get_vertices(), get_edges(),
#              is_valid_path(), dfs(), ​bfs(), count_connected_components(), and has_cycle().

import heapq
from collections import deque

class UndirectedGraph:
    """
    Class to implement undirected graph
    - duplicate edges not allowed
    - loops not allowed
    - no edge weights
    - vertex names are strings
    """

    def __init__(self, start_edges=None):
        """
        Store graph info as adjacency list
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self.adj_list = dict()

        # populate graph with initial vertices and edges (if provided)
        # before using, implement add_vertex() and add_edge() methods
        if start_edges is not None:
            for u, v in start_edges:
                self.add_edge(u, v)

    def __str__(self):
        """
        Return content of the graph in human-readable form
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = [f'{v}: {self.adj_list[v]}' for v in self.adj_list]
        out = '\n  '.join(out)
        if len(out) < 70:
            out = out.replace('\n  ', ', ')
            return f'GRAPH: {{{out}}}'
        return f'GRAPH: {{\n  {out}}}'

    # ------------------------------------------------------------------ #

    def add_vertex(self, v: str) -> None:
        """
        Add new vertex to the graph
        """
        if v not in self.adj_list:
            self.adj_list[v] = []

        
    def add_edge(self, u: str, v: str) -> None:
        """
        Add edge to the graph
        """
        # If u & v refer to the same vertex.
        if u == v:
            return 
        
        if u not in self.adj_list:            # If u not in the graph.
            self.adj_list[u] = [v]
        else:                                 # If u in the graph.
            if v not in self.adj_list[u]:
                self.adj_list[u].append(v)
        
        if v not in self.adj_list:            # If v not in the graph.
            self.adj_list[v] = [u]
        else:
            if u not in self.adj_list[v]:
                self.adj_list[v].append(u)        # If v in the graph.


    def remove_edge(self, v: str, u: str) -> None:
        """
        Remove edge from the graph
        """
        if v in self.adj_list and u in self.adj_list:
            if u in self.adj_list[v]:
                self.adj_list[u].remove(v)
                self.adj_list[v].remove(u)
        

    def remove_vertex(self, v: str) -> None:
        """
        Remove vertex and all connected edges
        """
        if v in self.adj_list:
            for adj_value in self.adj_list[v]:
                self.adj_list[adj_value].remove(v)
            self.adj_list.pop(v)


    def get_vertices(self) -> []:
        """
        Return list of vertices in the graph (any order)
        """
        result = []
        for vertex in self.adj_list:
            result.append(vertex)
        return result


    def get_edges(self) -> []:
        """
        Return list of edges in the graph (any order)
        """
        result = []
        viewed = []
        for key in self.adj_list:
            for value in self.adj_list[key]:
                if value not in viewed:
                    result.append((key, value))
                    viewed.append(key)
        return result


    def is_valid_path(self, path: []) -> bool:
        """
        Return true if provided path is valid, False otherwise
        """
        path_length = len(path)
        if path_length != 0:
            if path[0] not in self.adj_list:
                return False 
            for index in range(1, path_length):
                if path[index] not in self.adj_list:
                    return False
                else:
                    if path[index] not in self.adj_list[path[index - 1]]:
                        return False
        return True
  

    def dfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during DFS search
        Vertices are picked in alphabetical order
        """
        visited = []
        if v_start in self.adj_list:
            wait = [v_start]
            while len(wait) != 0:
                temp = wait.pop(0)
                if temp not in visited:
                    visited.append(temp)
                    if temp == v_end:
                        return visited
                    temp_list = []
                    for value in self.adj_list[temp]:
                        temp_list.append(value)
                    temp_list.sort()
                    wait = temp_list + wait   
        return visited


    def bfs(self, v_start, v_end=None) -> []:
        """
        Return list of vertices visited during BFS search
        Vertices are picked in alphabetical order
        """
        visited = []
        if v_start in self.adj_list:
            wait = [v_start]
            while len(wait) != 0:
                temp = wait.pop(0)
                if temp not in visited:
                    visited.append(temp)
                    if temp == v_end:
                        return visited
                    temp_list = []
                    for value in self.adj_list[temp]:
                        temp_list.append(value)
                    temp_list.sort()
                    wait = wait + temp_list
        return visited 
        

    def count_connected_components(self):
        """
        Return number of connected componets in the graph
        """
        visited = []
        count = 0
        for vertex in self.adj_list:
            if vertex not in visited:
                self.count_connected_components_helper(vertex, visited)
                count += 1
        return count
    
    def count_connected_components_helper(self, vertex, visited):
        """The helper function for count_connected_componments()."""
        visited.append(vertex)
        for value in self.adj_list[vertex]:
            if value not in visited:
                self.count_connected_components_helper(value, visited)
 

    def has_cycle(self):
        """
        Return True if graph contains a cycle, False otherwise
        """
        visited = []
        for vertex in self.adj_list:
            if vertex not in visited:
                if self.has_cycle_helper(vertex, visited):
                    return True
        return False
    
    def has_cycle_helper(self, vertex, visited, parent = None):
        """The helper function for has_cycle_helper()."""
        visited.append(vertex)
        for value in self.adj_list[vertex]:
            if value not in visited:
                if self.has_cycle_helper(value, visited, vertex):
                    return True
            elif value != parent:
                return True
        return False
   


if __name__ == '__main__':

    print("\nPDF - method add_vertex() / add_edge example 1")
    print("----------------------------------------------")
    g = UndirectedGraph()
    print(g)

    for v in 'ABCDE':
        g.add_vertex(v)
    print(g)

    g.add_vertex('A')
    print(g)

    for u, v in ['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE', ('B', 'C')]:
        g.add_edge(u, v)
    print(g)


    print("\nPDF - method remove_edge() / remove_vertex example 1")
    print("----------------------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    g.remove_vertex('DOES NOT EXIST')
    g.remove_edge('A', 'B')
    g.remove_edge('X', 'B')
    print(g)
    g.remove_vertex('D')
    print(g)


    print("\nPDF - method get_vertices() / get_edges() example 1")
    print("---------------------------------------------------")
    g = UndirectedGraph()
    print(g.get_edges(), g.get_vertices(), sep='\n')
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE'])
    print(g.get_edges(), g.get_vertices(), sep='\n')


    print("\nPDF - method is_valid_path() example 1")
    print("--------------------------------------")
    g = UndirectedGraph(['AB', 'AC', 'BC', 'BD', 'CD', 'CE', 'DE'])
    test_cases = ['ABC', 'ADE', 'ECABDCBE', 'ACDECB', '', 'D', 'Z']
    for path in test_cases:
        print(list(path), g.is_valid_path(list(path)))


    print("\nPDF - method dfs() and bfs() example 1")
    print("--------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = 'ABCDEGH'
    for case in test_cases:
        print(f'{case} DFS:{g.dfs(case)} BFS:{g.bfs(case)}')
    print('-----')
    for i in range(1, len(test_cases)):
        v1, v2 = test_cases[i], test_cases[-1 - i]
        print(f'{v1}-{v2} DFS:{g.dfs(v1, v2)} BFS:{g.bfs(v1, v2)}')


    print("\nPDF - method count_connected_components() example 1")
    print("---------------------------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print(g.count_connected_components(), end=' ')
    print()


    print("\nPDF - method has_cycle() example 1")
    print("----------------------------------")
    edges = ['AE', 'AC', 'BE', 'CE', 'CD', 'CB', 'BD', 'ED', 'BH', 'QG', 'FG']
    g = UndirectedGraph(edges)
    test_cases = (
        'add QH', 'remove FG', 'remove GQ', 'remove HQ',
        'remove AE', 'remove CA', 'remove EB', 'remove CE', 'remove DE',
        'remove BC', 'add EA', 'add EF', 'add GQ', 'add AC', 'add DQ',
        'add EG', 'add QH', 'remove CD', 'remove BD', 'remove QG',
        'add FG', 'remove GE')
    for case in test_cases:
        command, edge = case.split()
        u, v = edge
        g.add_edge(u, v) if command == 'add' else g.remove_edge(u, v)
        print('{:<10}'.format(case), g.has_cycle())
