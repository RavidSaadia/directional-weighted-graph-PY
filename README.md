# directional-weighted-graph-PY

Ex3 Readme. Introduction @auther Ravid Saadia & Achiya Zigler

In this project we will implement the interfaces. There are tow classes which we will use in order to implement the interfaces and another graphics class. (We will elaborate each class by it's section)

an example image represented here: 

![alt text](https://github.com/RavidSaadia/directional-weighted-graph-PY/blob/master/Figure_1.png)
![alt text](https://github.com/RavidSaadia/directional-weighted-graph-PY/blob/master/Figure_2.png)

functions implementations

Node class function:

The first class is an inner class that called _**"Node Class"**_. This class represents the individual Vertex in a (directional) weighted graph.

In this class we will perform the following steps:

        -def get_inside(self) -> dict:
            """
            return dict with keys of node u
            such that (u,self) edge exists,
            with value of the edge's weight
            :return: dict
            """

        -def get_outside(self) -> dict:
            """
            return dict with keys of node u
            such that (self,u) edge exists,
            with value of the edge's weight
            :return: dict
            """

        -def id(self) -> int:
            """
            :return: the node's id
            """

        -def set_in(self, key, w):
            """
            add in edge with key = key and weight = w
            :param key:
            :param w:
            """

        -def set_out(self, key, w):
            """
            add out edge with key = key and weight = w
            :param key:
            :param w:
            """

        -def del_in(self, key):
            """
            remove in edge
            :param key:
            :return:
            """

        -def del_out(self, key):
            """
            remove out edge
            :param key:
            :return:
            """
            **_DWGraph_DS classs function:_**


The second class is called _**"DiGraph Class"**_.
This class represents all Vertexes which are what make our graph.
This graph is called "directed weighted Graph".
This class creates a graph from each individual vertex (node) by implement the interface **"GraphInterface"**
in the code "DiGraph" to create the graph itself.
The Data Structures which we used are "dict" since it is very effective.
In this class we will perform the following steps:



    -def remove_node(self, node_id: int) -> bool:
        """
        remove node with key = node_id from the graph
        :param node_id:
        :return: True if node_id has been removed, False else
        """
        

    -def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """
        remove the edge (node_id1,node_id2) from the graph.
        :param node_id1:
        :param node_id2:
        :return: True if the edge removed,
        False if nothing has been changed
        (for example if one of the keys doesn't exists
        or the edge itself doesn't exists.
        """
      

    -def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """
        add node with key = node_id.
        optional: set position with 2-tuple(x,y) coordinates.
        :param node_id:
        :param pos:
        :return: True if the node has been removed, False if nothing has changes.
        (for example if the node doesn't exists in the graph.
        """
       

    -def v_size(self) -> int:
        """
        :return: number of nodes in the graph.
        """

    -def e_size(self) -> int:
        """
        :return: number of edges in the graph.
        """

    -def get_all_v(self) -> dict:
        """
        :return: dictionary with keys represents all the nodes keys, the values are the nodes.
        """

    -def all_in_edges_of_node(self, id1: int) -> dict:
        """
        :param id1:
        :return: dictionary of the ingoing edges from key=id1
        """

    -def all_out_edges_of_node(self, id1: int) -> dict:
        """
        :param id1:
        :return: dictionary of the outgoing edges from key=id1
        """

    -def get_mc(self) -> int:
        """
        :return: number of changes made in the graph
        """

    -def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        add edge (id1,id2) with weight = weight to the graph.
        :param id1:
        :param id2:
        :param weight:
        :return: True iff the edge (id1,id2) wasn't existed before
        """
        

    -def get_edge(self, id1, id2) -> (float,bool):
        """
        :param id1:
        :param id2:
        :return: 2-tuple. 1st is the weight of edge (id1,id2) (-1 if not existed), 2nd is wether the edge was existed
        """
        
        **_DWGraph_Algo class function:_**

The third class is called _**"GraphAlgo Class"**_ .
This class executes algorithmic operations on graphs which were created by "DiGraph".
We implement the interface "GraphAlgoInterface" in the code "GraphAlgo" to perform algorithmic operations on different graphs.
In this class we will use the parameters "Tag and Info" which we have in the class "Node".
In this class we will perform the following steps:
            
            
            
        -def get_graph(self) -> GraphInterface:
        """
        :return: the initialized graph
        """

    -def _DFS_visit(self, root, finishing, t):
        """
        private method in use by dfs().
        the pseudo code for recursive function is:
        1. color[u] ← GRAY
        2. time ← time + 1
        3. d[u] ← time
        4. for each v ∈ Adj[u]
        5.  do if color[v] = WHITE
        6.      then π[v] ← u
        7.      DFS-Visit(v)
        8. color[u] ← BLACK
        9. f[u] ← time ← time + 1
        the code below is the 'while-version' of the pseudo code above.
        """
        

    -def dfs(self, nodes, t=False):
        """
        simple dfs concept, with a touch of calculating the scc's inside the algorithm to save runtime.
        the pseudo code taken from algo1 lecture.
        1. for each vertex u ∈ V[G]
        2.  do color[u] ← white (0)
        3.  π[u] ← NULL (-1)
        4. time ← 0
        5. for each vertex u ∈ V[G]
        6.  do if color[u] = white
        7.      then DFS-Visit(u)
        """
        

    -def transpose(self):
        """
        this method was written originally for SCC's,
        but a shortcut made by swapping all_out_edges_of_node with all_in_edges_of_node when needed.
        so the function remained for general purposes.
        """
        

    -def load_from_json(self, file_name: str) -> dict:
        """
        load  a graph from a json file.
        the graph loaded will replace the initialized graph.
        """
       
    -def save_to_json(self, file_name: str) -> bool:
        """
        save the initialized graph to a file.
        """
        

    -def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        calculate the shortest path from id1 to id2 using dijaxtra algorithm.
        :return: the weight of the path and a list with the path keys.
        if the path doesn't exist, return 'inf',[].
        """
        

    -def connected_component(self, id1: int) -> list:
        """
        return the component that contains id1
        represented by list of the component's keys.
        if the key isn't in the initialized graph, return [].
        """
        

    -def connected_components(self) -> List[list]:
        """
        1. call DFS(G) to compute finishing times f [u] for all u
        2. compute G transpose (actually just swapping all_in_edges_of_node with all_out_edges_of_node)
        3. call DFS(G transpose), but in the main loop, consider vertices in
           order of decreasing f [u] (as computed in first DFS)
        4. output the vertices in each tree of the depth-first forest
           formed in second DFS as a separate SCC
        """

        

    -def plot_graph(self) -> None:
        """
        painting the graph using matplotlib (in 'Graphics.py')
        """
        
        
The forth class is called _**"Graphics Class"**_ .
This class drawing graphs which were created by "DiGraph".
In this class we will perform the following steps:
        
     -def set_radius(g):
          """
          computing radius size with the proportions of the graph's 'spread'
          """
   


     -def dist(pos1, pos2):
         """
         a simple method to compute distance in 2 dimensioned real space.
         """
         return np.sqrt(np.power(pos1[0] - pos2[0], 2) + np.power(pos1[1] - pos2[1], 2))
     
     
     -def get_point(s, e, r):
         """
         given circle s centered in (x1,y1) with radius r
         and circle e centered in (x2,y2) with radius r,
         compute the intersection between the line (x1,y1)->(x2,y2) and the closer side of the edge of e to s.
         purpose: to draw the arrows correctly
         """
                 
   
     -def paint(g, title="", show_w=False, t=False):
         """
         plot g.
         ===flags===
             title: choose the title to show on the top. default is an empty string.
             show_w: to print the edges weights. not recommended in graphs containing both uv and vu edges.
             t: plot the transposed version of the graph
         """
        
        
        
        
        
        
        
