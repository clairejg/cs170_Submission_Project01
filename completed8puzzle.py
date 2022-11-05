import copy
import sys
from sys import maxsize # to trace cheapest node
import time

class State:
    goal_state = [[1, 2, 3], [4, 5, 6], [7, 8, 0]] 
#
    def __init__(self, puzzle, sz):
        self.puzzle = puzzle
        self.sz = sz
        self.row, self.col = self.search_zero() 
        print("*Printing the user input puzzle by Accessing 'puzzle' from State class...\n")
        print_puzzle(puzzle)
    def search_zero(self):
        for row in range(len(self.puzzle)): 
            for col in range(len(self.puzzle)): 
                if self.puzzle[row][col] == 0: 
                  return row, col 
  
    def get_newBoard(self, i, j):
        updated_board = self.puzzle[self.row][self.col] #save current puzzle into the pzzle
        self.puzzle[self.row][self.col] = self.puzzle[i][j] #swap '0' and 'whatever number'
        self.puzzle[i][j] = updated_board 
        #board is now updated after swap

    #1 row == row[0], 2 row == row[1]...
    def go_up(self):
        if 0 not in self.puzzle[0]: #when '0' is not in row[0]
            self.get_newBoard(self.row - 1, self.col) #//swap '0' to upper tile
            self.row = self.row - 1  #decrement row index.== moved down
            return True

    def go_down(self): 
        if 0 not in self.puzzle[2]: 
            self.get_newBoard(self.row + 1, self.col) 
            self.row= self.row + 1  
            return True
           
    def go_left(self): 
        curr_Left = False 
        for row in range(self.sz):
            if self.puzzle[row][0] == 0:
                curr_Left = True
                break

        if curr_Left == False:
            self.get_newBoard(self.row, self.col - 1) 
            self.col = self.col - 1
            return True

    def go_right(self): 
        curr_Right = False 
        for row in range(self.sz):
            if self.puzzle[row][2] == 0: 
                curr_Right = True
                break

        if curr_Right== False:
            self.get_newBoard(self.row, self.col+ 1) 
            self.col = self.col + 1    
            return True

    def display_puzzle(self):
        board = []
        for i in range(0, 3):
            print(self.puzzle[i])
        print("\n")
        board = [] #reset, otherwise it occurs error

class History:
     def __init__ (self):
        self.open_node = []
        self.total_node_expanded=0
history=History() #create instance of History class to trace them.

class Node:
    def __init__(self, state, path_cost, heuristic): 
        self.state = state #puzzle.
        self.path_cost = path_cost # ==depth_values.
        self.heuristic = heuristic # heuristic cost == heauristic Value
        #print("Printing State from Node class...")
        #print(state)

#Functions Delcaration::
def print_puzzle(puzzle):
    print("#This is the user's puzzle:")
    for i in range(0, 3):
        print(puzzle[i])
    print("\n")

def save_child(node, child_list):
    #deep copy the parent node == it creates child node.
  child = copy.deepcopy(node) 
  child.path_cost = child.path_cost + 1  #cost incrementations
 
  child_list.append(child)

def traverse_node(node):
  history.total_node_expanded
  child_list = []

  if node.state.go_up(): # if the tile is able to go_up
    history.open_node.append(node.state.puzzle) 
    save_child(node, child_list) #copy child node to child_list
    node.state.go_down() 
    #node_expanded_total+=node_expanded_total

  if node.state.go_down(): 
    history.open_node.append(node.state.puzzle)
    save_child(node, child_list) 
    node.state.go_up() 

  if node.state.go_left(): 
    history.open_node.append(node.state.puzzle) 
    save_child(node, child_list)
    node.state.go_right()

  if node.state.go_right(): 
    history.open_node.append(node.state.puzzle) 
    save_child(node, child_list) 
    node.state.go_left()

  history.total_node_expanded += len(child_list)
  return child_list

def remove_node(node_paths_sets): #removes cheapest node
  cheapest = maxsize
  removable_node = maxsize 
 
  for n in range(len(node_paths_sets)):
    g_of_n=node_paths_sets[n].path_cost + node_paths_sets[n].heuristic
    if (g_of_n) < cheapest:
        #when g(n)< cheapest Node, We update the new cheapest node to g(n) value
      cheapest = (g_of_n)
      removable_node = n

  node = node_paths_sets.pop(removable_node)
  return node

def count_misplaced_tiles(node):
  total_misplaced_tiles = 0 

  for row in range(len(node.state.puzzle)):
    for col in range(len(node.state.puzzle)):
      if node.state.puzzle[row][col] != node.state.goal_state[row][col]: 
        if node.state.puzzle[row][col] != 0: #we must not count '0' tile for the 'total_misplcaed_tile'
          total_misplaced_tiles += 1

  return total_misplaced_tiles

def manhattan_distance(node):
    goal_puzzle = [[1, 2, 3], [4, 5, 6], [7, 8, 0]] #2-d array
    manhattan_distance = 0
    #Manhattan_distance== total horizontal+ Vertical distance of each tile of user' puzzle(==node.state.puzzle)
    #away from Goal_state_Puzzle board.
    prev_row=0 
    prev_col=0
    goal_col=0 
    goal_row=0

    for element in range(1, 9):
        for row in range(len(node.state.puzzle)):
            for col in range(len(node.state.puzzle)):
                #if node.state.puzzle[row][col] != 0:
                    if int(node.state.puzzle[row][col]) == element:
                        prev_row=row
                        prev_col=col
                    if goal_puzzle[row][col] == element:
                        goal_row=row
                        goal_col=col
                    
        manhattan_distance += abs(goal_row-prev_row)+abs(goal_col-prev_col)
                        #keep adding at the inside of loops. 
    #abs == absolute val
    
    return manhattan_distance

def expand(node_sets, node, algo):
  
  print("The best state to expand with g(n) = " , str(node.path_cost) + " and h(n) = " , str(node.heuristic) + " is...")
  #must covert to string type
  node.state.display_puzzle()
  child_list = traverse_node(node) #save expanded node into child_list queue.

  if algo==1:
        for child in child_list: 
            if child.state.puzzle not in history.open_node: #if==true, the append child.state.puzzle 
                node_sets.append(child) 
                history.open_node.append(child.state.puzzle) #append the child to the queue.
  elif algo==2:
        for child in child_list: 
                child.heuristic = count_misplaced_tiles(child)
                if child.state.puzzle not in history.open_node: 
                    node_sets.append(child) 
                    history.open_node.append(child.state.puzzle) 
  elif algo==3:
        for child in child_list:
                child.heuristic = manhattan_distance(child)
                if child.state.puzzle not in history.open_node: 
                    node_sets.append(child) 
                    history.open_node.append(child.state.puzzle) 
  return node_sets
   

def general_search(state, algo):
  path = 0
  heuristic = 0
  
  node = Node(state, path, heuristic)  #create instance
  if algo == 1: 
    heuristic = 0
  elif algo == 2: 
    node.heuristic = count_misplaced_tiles(node)
  elif algo == 3: 
    node.heuristic = manhattan_distance(node)
  node_paths_sets = [node] 
  #node_paths_sets: is a set of paths from a start node
    #to goal node.
  max_queue_size = 0
  

  while True:
    max_queue_size = max(len(node_paths_sets), max_queue_size)

    print("#current seen puzzle before 'remove_node'function:")
    print(node.state.puzzle)
    print("#")
    (node) = remove_node(node_paths_sets)
    

    if node.state.puzzle == state.goal_state: 
      depth_cost=node.path_cost
     
      print("The user puzzle found the Goal Puzzle! ")
      print("#which applies: node.state.puzzle == state.goal_state") 
      print("#FROM this puzzle:")
    
      print_puzzle(node.state.puzzle) #This is the user puzzle that has been moved all the way to goal puzzle board.
      print("Solution Depth was: " , str(depth_cost))
      print("Number of nodes expanded: " , str(history.total_node_expanded))
      print("Max queue size: " , str(max_queue_size))
      return
      #must do return to avoid looping

    node_paths_sets = expand(node_paths_sets,node,algo)
    

#driver main function
def main():
  print("Welcome to Claire 8-puzzle Solver. \nType '1' to use a default puzzle, or '2' to create your own." )
  userInput_1 = int(input()) 
  print("userInput_1 :", userInput_1 ) 
  puzzle = []

  if userInput_1 == 1:
    print("Choose from 1)trivial, 2)veryEasy 3)easy 4)doable 5)oh_boy. \n")
    total_puzzle_row =3

    userInput_2 = int(input())
    print("userInput_2 :", userInput_2 ) 
    if userInput_2 == 1:
      puzzle = [[1, 2, 3], [4, 5, 6], [7, 8, 0]]
    elif userInput_2 == 2:
      puzzle = [[1, 2, 3], [4, 5, 6], [7, 0, 8]]
    elif userInput_2 == 3:
      puzzle = [[1, 2, 0], [4, 5, 3], [7, 8, 6]]
    elif userInput_2 == 4:
      puzzle = [[0, 1, 2], [4, 5, 3], [7, 8, 6]]
    elif userInput_2 == 5:
      puzzle = [[8, 7, 1], [6, 0, 2], [5, 4, 3]]
    #total_puzzle_row =3.. illegal here 
        
  elif userInput_1 == 2:
    print("\nEnter your puzzle, using a zero to represent the blank space in the puzzle board. ")
    print("Hit space after typing each number. Hit Enter to go to the next row. \n")
    r1= input("Enter the first row, hit space after typing each number: ")
    r1 = [int(n) for n in r1.split(' ')]
    r2 = input("Enter the second row, hit space after typing each number: ")
    r2 = [int(n) for n in r2.split(' ')]
    r3= input("Enter the third row, hit space after typing each number: ")
    r3= [int(n) for n in r3.split(' ')]
    #[int(n) for n in third_row] == make firstrow: (123) into [1,2,3]
    puzzle = [r1,r2,r3]
    total_puzzle_row =3

  state = State(puzzle,total_puzzle_row)

  alogoritm_type=int(input("Select Algorithm to use:\n"+ "1. Uniform Cost Search\n"+
  "2. A* with Misplaced Tile Heuristic\n"+"3: A* with manhattan_distance Heuristic\n"))
  
  if alogoritm_type == 1:
    start_time = time.time()
    print(" Alogorithm selected: Uniform Cost Search")
    state.display_puzzle()
    general_search(state, alogoritm_type)
    end_time = time.time()
    print("Execution Time : %s seconds ---" %(end_time-start_time))
    #passing State class instance: 'state'

  elif alogoritm_type == 2:
    start_time = time.time()
    print("Alogorithm selected: A*  Misplaced Tile Heuristic")
    state.display_puzzle()
    general_search(state, alogoritm_type)
    end_time = time.time()
    print("Execution Time : %s seconds ---" %(end_time-start_time))

  elif alogoritm_type == 3:
    start_time = time.time()
    print("Alogorithm selected: A* Manhattan Distance Heuristic")
    state.display_puzzle()
    general_search(state, alogoritm_type)
    end_time = time.time()
    print("Execution Time : %s seconds ---" %(end_time-start_time))


   
main()
