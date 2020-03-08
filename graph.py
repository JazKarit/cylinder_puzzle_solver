import pygame.font, pygame.draw
import random, time
from anytree import Node, RenderTree


class Graph():
    
    def __init__(self, settings, screen):
        """Initialize graph attributes and data."""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        
        self.node_radius = 30
        #....................empty.......blue........green..........yellow.........red        
        self.node_colors = [(0,0,0),(0, 164, 239),(7, 173, 70), (241, 193, 0), (193, 37, 7)]
        self.edge_color = (0,0,0)
        
        #from center
        self.nodes = []       #form [(x,y),color]
        self.build_nodes()    
        self.edge_coords = [] #form ((x,y),(x,y))
        self.edges = []       #form (n1,n2)
        self.adjacency_list = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
        self.build_edges()
        self.build_adjacency_list()
        self.ball_list = [0,1,1,1,1,1,2,2,2,2,2,3,3,3,3,3,4,4,4,4,4]
        self.randomize()
        self.solved_nodes = []
        self.wait_time = 0.15
        
    def build_nodes(self):
        """Build frame of where nodes of graph go"""
        center_x = self.screen_rect.center[0] 
        center_y = self.screen_rect.center[1] - 50
        x_spacing = 200
        y_spacing = 160
        left_x = center_x - int(1.5 * x_spacing)
        up_y = center_y - int(1.5 * y_spacing)
        self.nodes.append([ (int(center_x-2.5*x_spacing),center_y),self.node_colors[0] ])
        
        for j in range(0,4):
            for i in range(0,5):
                self.nodes.append([ (left_x + i*x_spacing,up_y + j*y_spacing),self.node_colors[0] ])
        
    def build_edges(self):
        """Build frame of where edges of graph go"""
        for i in range(0,4):
            self.add_edge(0,5*i+1)
            self.add_edge(5*i+1,5*i+2)
            self.add_edge(5*i+3,5*i+4)
        for i in range(0,4):
            for j in range(0,4):
                self.add_edge(5*i+2,5*j+3)
                self.add_edge(5*i+4,5*j+5)
    
    def build_adjacency_list(self):
        for i in range(0,21):
            for edge in self.edges:
                if edge[0] == i:
                    self.adjacency_list[i].append(edge[1])
                elif edge[1] == i:
                    self.adjacency_list[i].append(edge[0])
                    

            
    
    def add_edge(self,n1,n2):
        self.edges.append((n1,n2))
        self.edge_coords.append(( self.nodes[n1][0],self.nodes[n2][0] ))
        
    def draw_graph(self):
        """Draw all nodes and edges in graph"""
        for edge in self.edge_coords:
            pygame.draw.line(self.screen,self.edge_color,edge[0],edge[1],4)
        for node in self.nodes:
            pygame.draw.circle(self.screen,node[1],node[0],self.node_radius)
                   
    def randomize(self):
        #4 kinds of balls labeled 1-4 and 5 of each ball
        #0 is the empty slot
        random.shuffle(self.ball_list)
        self.solved_nodes = []
        self.update_graph()
        
    def update_graph(self):
        for i in range(len(self.nodes)):
            self.nodes[i][1] = self.node_colors[self.ball_list[i]]
    
    def solve_puzzle(self):
        self.solve_row(1,5,1)
        self.solve_row(6,10,2)
        time.sleep(60)
        self.solve_last_two_rows()
        time.sleep(10)
        self.clean_up_last_two_rows()
        #self.random_mix()
        #self.solve_row(11,15,3)
        #self.solve_row(16,20,4)
        
    def clean_up_last_two_rows(self):
        unsolved_nodes = [15,14,13,12,11,0,16,17,18,19,20]
        
        #get empty slot index
        empty_slot = 0
        for node in unsolved_nodes:
            if self.ball_list[node] == 0:
                empty_slot = node
                break
                
        path = [15,14,13,12,11,0,16,17,18,19]
        if empty_slot not in path:
            path = [14,13,12,11,0,16,17,18,19,20]
        while empty_slot != path[0]:
            path = path[1:] + path[:1]
        while True:
            for node in path:
                self.ball_list[empty_slot] = self.ball_list[node] 
                self.ball_list[node] = 0
                empty_slot = node
                self.update_graph()
                self.draw_graph()
                pygame.display.flip()
                if empty_slot == 0:
                    if 3 not in self.ball_list[11:16] or 3 not in self.ball_list[16:21]:
                        print("solved")
                        return
                time.sleep(0.5)
                
        
    def solve_last_two_rows(self):
        unsolved_nodes = [15,14,13,12,11,0,16,17,18,19,20]
        
        
        #get empty slot index
        empty_slot = 0
        for node in unsolved_nodes:
            if self.ball_list[node] == 0:
                empty_slot = node
                break
        
        prev_node = -1
        while True:
            #Pick out the switch that maximizes adj_nodes of same color
            #Expected error getting stuck going back an forth between two
            #equally good states
            best_switch_node = 0
            best_adj_nodes = 0
            for node in self.adjacency_list[empty_slot]:
                if node != prev_node and node in unsolved_nodes:
                    self.ball_list[empty_slot] = self.ball_list[node] 
                    self.ball_list[node] = 0
                    future_adj_nodes = self.count_largest_adj(unsolved_nodes)
                    if future_adj_nodes > best_adj_nodes:
                        best_adj_nodes = future_adj_nodes
                        best_switch_node = node
                    
                    self.ball_list[node] = self.ball_list[empty_slot]
                    self.ball_list[empty_slot] = 0 
            
            self.ball_list[empty_slot] = self.ball_list[best_switch_node] 
            self.ball_list[best_switch_node] = 0
            prev_node = empty_slot
            empty_slot = best_switch_node
            self.update_graph()
            self.draw_graph()
            pygame.display.flip()
            print(best_adj_nodes)
            if best_adj_nodes == 10:
                #time.sleep(3)
                return
            time.sleep(1)
        
        
                
        
        
        
    def count_largest_adj(self,unsolved_nodes):
        adj_yellow_nodes = 0
        adj_red_nodes = 0
        prev_node = 0
        yellow_run = 0
        red_run = 0
        for node in unsolved_nodes:
            if self.ball_list[node] == 3:
                if red_run > adj_red_nodes:
                    adj_red_nodes = red_run
                red_run = 0
            elif self.ball_list[node] == 4:
                if yellow_run > adj_yellow_nodes:
                    adj_yellow_nodes = yellow_run
                yellow_run = 0
            if self.ball_list[node] == 3 and self.ball_list[prev_node] == 3:
                yellow_run += 1
            if self.ball_list[node] == 4 and self.ball_list[prev_node] == 4:
                red_run += 1
                
            if self.ball_list[node] != 0: #ignore empty slot
                prev_node = node
        adj_yellow_nodes += 1
        adj_red_nodes += 1
        
        if adj_yellow_nodes == 5 or adj_red_nodes == 5:
            return 10
        return adj_yellow_nodes + adj_red_nodes
        
    def random_mix(self):
        unsolved_nodes = [0,11,12,13,14,15,20,19,18,17,16]
        empty_slot_index = 0
        for node in unsolved_nodes:
            if self.ball_list[node] == 0:
                empty_slot_index = node
                break
        prev_node = 25
        while True:
            rand = random.randint(0,len(self.adjacency_list[empty_slot_index])-1)
            switch_node = self.adjacency_list[empty_slot_index][rand]#node to switch with empty slot
            if switch_node in unsolved_nodes and switch_node != prev_node:
                
                #print("switch " + str(empty_slot_index) + " with " + str(switch_node))
                self.ball_list[empty_slot_index] = self.ball_list[switch_node] 
                self.ball_list[switch_node] = 0
                prev_node = empty_slot_index
                empty_slot_index = switch_node
                self.update_graph()
                self.draw_graph()
                pygame.display.flip()
                if self.check_solved(unsolved_nodes):
                    return
                time.sleep(self.wait_time)
            
        
        
    def check_solved(self,unsolved_nodes):
        adj_color_3 = 0
        adj_color_4 = 0
        prev_node = 0
        for node in unsolved_nodes:
            if self.ball_list[node] == 3 and self.ball_list[prev_node] == 3:
                adj_color_3 += 1
            elif self.ball_list[node] == 2 and self.ball_list[prev_node] == 2:
                adj_color_2 += 1
            if self.ball_list[node] != 0: #ignore empty slot
                prev_node = node
        if adj_color_3 == 5 or adj_color_4 == 5:
            #print("solved")
            #print(adj_color_3)
            #print(adj_color_4)
            return True
        else:
            return False
                
            
        
        
    def solve_row(self,begin_index,end_index,color_num):
        for node in range(begin_index,end_index+1):
            self.solve_node(node,color_num)
    
    def solve_node(self,node,color):
        path = self.search_ball(node,color)
        for n in range(1,len(path)):
            #print("Move " + str(path[n-1]) + " to " + str(path[n]))
            self.move_ball_node(path[n-1],path[n])#empty next node and move ball there
        self.solved_nodes.append(node)
            
    def move_ball_node(self,start_node,end_node):
        """
        Empty end node and move ball in start node there
        Not to be used to move the empty slot
        """
        if self.ball_list[start_node] == 0:
            print("Attempting to move empty slot like a ball")
        if start_node == end_node:
            return
        self.move_empty_slot(end_node,[start_node])
        self.ball_list[end_node] = self.ball_list[start_node] 
        self.ball_list[start_node] = 0
        self.update_graph()
        self.draw_graph()
        pygame.display.flip()
        time.sleep(self.wait_time)
        
    def move_empty_slot(self,node,untouchable_nodes):
        """Move empty slot to the given node"""
        path = self.search_ball(node,0,untouchable_nodes) #empty slot is a ball with number 0
        #print(path)
        for n in range(1,len(path)):
            self.ball_list[path[n-1]] = self.ball_list[path[n]] 
            self.ball_list[path[n]]   = 0
            self.update_graph()
            self.draw_graph()
            pygame.display.flip()
            time.sleep(self.wait_time)
            
            
    def search_ball(self,node,color,untouchable_nodes = []):
        """
        Return a path to nearest ball to node <node> of color <color> 
        May not pass through solved nodes or any untouchable nodes 
        passed in
        """
        if self.ball_list[node] == color:
            return []
        else:
            root = Node(node,num=node)
            new_leaves = [root] #node list
            visited_nodes = [node] #int list
            i = 0
            while i < 20:
                i += 1
                leaves = new_leaves #node list
                new_leaves = []
                for leaf in leaves:
                    for n in self.adjacency_list[leaf.num]: 
                        if self.ball_list[n] == color and n not in self.solved_nodes and n not in untouchable_nodes:
                            node_n = Node(n,parent=leaf,num=n)
                            ancestors = node_n.ancestors
                            path = []
                            for ancestor in ancestors:
                                path.append(ancestor.name)
                            path.append(node_n.name)
                            path.reverse()
                            return path
                        elif n not in visited_nodes and n not in self.solved_nodes and n not in untouchable_nodes:
                            visited_nodes.append(n)
                            node_n = Node(n,parent=leaf,num=n)
                            new_leaves.append(node_n)
            print("No allowed moves")
            time.sleep(5.0)
                
                 
                
            
        
        

