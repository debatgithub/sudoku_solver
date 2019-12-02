import sys
from utils import *

class Node:
    rChild,lChild,data = None,None,None

    def __init__(self,key):
        self.rChild = None
        self.lChild = None
        self.data = key
class Tree:
    root,size = None,0
    def __init__(self):
        self.root = None
        self.size = 0

    def insert(self,node,someNumber):
        if node is None:
            node = Node(someNumber)
        else:
            if node.data > someNumber:
                self.insert(node.rchild,someNumber)
            else:
                self.insert(node.rchild, someNumber)
        return

def Exerciser():
    t = Tree()
    t.root = Node(4)
    t.root.rchild = Node(5)
    #print t.root.data #this works
    print t.root.rchild.data #this works too
    t = Tree()
    t.insert(t.root,4)
    t.insert(t.root,5)
    print t.root.data #this fails
    print t.root.rchild.data #this fails too

class Sudoku_Solver:
    input_line = ''
    values = []
    solution_status = 0

    def __init__(self, input_line_p):
        self.input_line = input_line_p
        self.values = self.grid_values(self.input_line)
#######
# The Sudoku in the file should be entered in the following format 
#4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......
#4 is the value in top left cell. Then 5 cells are blank. 7th cell has the value 8, 9th cell has the value 5, and the 8th cell is blank
#Then the next line starts
#9x9 or 81 characters in each line of the file, and each line represents an unsolved sudoku game
######
    

    def solve(self, values):
        """
        solves the puzzle
        """

        r_values = self.reduce_sudoku_puzzle(self.values)
        if (r_values == False):
            print "Reached a point of no return"
            return
        self.values = r_values 
        res = self.result(self.values)
        if (res == 1):
            print "The Sudoku puzzle is solved"
            self.print_final(self.values)
            return res
        
        r_values = self.search(self.values)   
        if (r_values):
            self.values = r_values
            res = self.result(r_values)
            self.print_final(r_values)
            if (res == 1):
                 print "The Sudoku puzzle is solved"
                 return res
        print "The Sudoku puzzle is not solved yet"
        self.print_final(self.values)        
        return 0
            

    def search(self, values):
        values = self.reduce_sudoku_puzzle(values)
        if values is False:
            return False ## Failed earlier
        if (self.count_of_multiples(values) == 0): 
            if (self.check_if_solved(values) == True):
                return values ## Solved!
            else:
                return False
    # Choose one of the unfilled squares with the fewest possibilities
        min_len = 20
        min_k = ''
        min_val = ''
        for k in boxes:
            if (len(values[k]) > 1):
                if (min_len > len(values[k])):
                    min_len = len(values[k])
                    min_k = k
                    min_val = values[k]
                    #print "new min_len = %d" %min_len 
    # Now use recurrence to solve each one of the resulting sudokus, and 
        for value in values[min_k]:
            new_sudoku = values.copy()
            new_sudoku[min_k] = value
            attempt = self.search(new_sudoku)
            if attempt:
                return attempt
            
    def reduce_sudoku_puzzle(self, values):

        no_progress = False
        r_values = values
        while not no_progress:
            unsolved_values_after = 0
            unsolved_values_before = self.count_of_multiples(values) 
            if (unsolved_values_before == 0):
                return values
            r_values = self.eliminate(r_values)
            r_values = self.only_choice(r_values)
            unsolved_values_after = self.count_of_multiples(values)
            #print "Before = %d, after = %d" %(unsolved_values_before, unsolved_values_after)
            if self.unsolvable_sudoku(r_values):
                return False
            no_progress = (unsolved_values_after == unsolved_values_before)
        return r_values    


    def unsolvable_sudoku(self, values):
        for box in values.keys():
            val = values[box]
            if (len(val) == 0):
                return True
        return False

    def count_of_multiples(self, values):
        unsolved_boxes = 0
        for box in values.keys():
            val = values[box]
            if (len(val) > 1):
                unsolved_boxes = unsolved_boxes + 1
        return unsolved_boxes

    def result(self, values):
        if (self.solution_status == 1):
            return self.solution_status
        unsolved_boxes = self.count_of_multiples(values)
        if (unsolved_boxes == 0):
            if (self.check_if_solved(values) == True):
                self.solution_status = 1
            else:
                self.solution_status = 0
        else:
            self.solution_status = 0
        return self.solution_status
  
    def check_if_solved(self, values):
        solved = True
        for unit in unitlist:
            if (set(values[s] for s in unit) != set(digits)):
                solved = False;
                return solved
        return solved

          
    def grid_values(self, grid):

        local_values = dict(zip(boxes, grid))
        allowable_digits = '123456789'
        for i in boxes:
            c = local_values[i]
            if (c == '0'):
                local_values[i] = allowable_digits
            elif  (c == '.'):
                local_values[i] = allowable_digits
        return local_values


    def simple_grid_values(self, grid):
        value = dict(zip(boxes, grid))
        return value


    def eliminate(self, values):
        for any_box in values.keys():
            box_digit = values[any_box]
            if (len(box_digit) == 1):
                for any_peer in peers[any_box]:
                    if (len(values[any_peer]) > 1):
                        values[any_peer] = values[any_peer].replace(box_digit,'')
        return values

    def only_choice(self, values):
        for unit in unitlist:
            digits = '123456789'
            for i in digits:
                digit_len = 0
                box_index = ''
                for box in unit:
                    val = values[box]
                    if i in val:
                        digit_len = digit_len + 1
                        box_index = box
                if (digit_len == 1):
                    values[box_index] = i
        return values

    def print_final(self, values):
        display(values)

def main(argv):

    larg = len(sys.argv)
    if (larg > 2):
         print "Invalid number of arguments"
         print "Usage - python function.py name_of_the_sudoku_file"
         sys.exit(-1)
    sudoku_file_name = sys.argv[1]
    try:
        filec = open (sudoku_file_name,'r');
    except IOError:
        print ("Can not open", sudoku_file_name);
        sys.exit (-1)
    try:
        for line in filec:
             
             print "sudoku line = "+line
             sudoku_slvr = Sudoku_Solver(line)
             sudoku_slvr.solve(sudoku_slvr.values)

    
        filec.close();
        return;
    except IOError:
        print ("I/O error");
        sys.exit(-1)



if __name__ == "__main__":
    main(sys.argv[1:])


