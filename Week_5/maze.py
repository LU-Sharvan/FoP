"""
File: maze.py
Author: Sharvan Gangadin
Description: Code that returns the route through a maze from start to end, contains both recursive and iterative way
License: LU License
"""

class Maze():
    # visualization characters
    block = "\uFF03"
    empty = "\u3000"
    path = "\uFF0A"

    def __init__(self, start, transitions):
        """ A maze has two objects that you need to use to solve the assignment"""
        self.start = start  # Starting position in maze
        self.transitions = transitions  # List of neighbours

        # This is for visualization purposes and you do not need for the assignment
        width = max(self.transitions, key=lambda x: x[0])[0]  # function lambda returns x[0] (x) to determine width
        height = max(self.transitions, key=lambda x: x[1])[1]  # function lambda return x[1] (y) to determine heigth
        self.maze = [[Maze.block] * (width + 3), [Maze.block] * (width + 3)]
        for j in range(height + 1):  # Y coordinate: each row
            row = [Maze.block, Maze.block]  # Start and end of borders
            for i in range(width + 1):  # X coordinate: each column
                row.insert(-1, Maze.empty if (i, j) in self.transitions else Maze.block)
            self.maze.insert(-1, row)  # Places row (tuple) before last border

    def __repr__(self):
        """ The representation of the maze """
        return '\n'.join([''.join(row) for row in self.maze])

    def show(self, route):
        """ Shows the representation of the maze including the route """
        maze = self.maze.copy()
        for pos in route:
            maze[pos[1] + 1][pos[0] + 1] = Maze.path if "codegrade" in __file__ else f"\033[31m{Maze.path}\033[0m"
        print('\n'.join([''.join(row) for row in maze]))

# Main function

def find_route(maze, end):
    route = find_route_rec(maze, maze.start, end)  # Starting position of Maze object, helper function returns list

    # If helper function returns None
    if route is None:
        print("Warning: no route can be found!")
        return []

    return route

# Helper functions

# Depth First Search uses Python's call stack to navigate tree, branches end in None -> switching

def find_route_rec(maze, start, end):  # Children become new starting positions

    # Base Case: starting at the end
    if start == end:
        return [start]  # Returns current position as a list if you start at the endpoint

    # Base Case: current starting point in the loop or end point isn't present in the maze
    if start not in maze.transitions or end not in maze.transitions:
        return None  # Returns back to subroute -> if condition is false -> next for-loop/branch iteration gets started

    # Recursive function: every child of the current position will be evaluated
    for child in maze.transitions[start]:  # Starts with children of start
        subroute = find_route_iter(maze, child, end)  # Tree: start's children till (dead) end, returns [start] at end

        # If the tree can be followed till the endpoint
        if subroute is not None:  # Subroute is the child of start, and is the endpoint, in the top layer
            return [start] + subroute  # Then subroute becomes both for start in the layer beneath

    return None  # If a child has an empty list (dead end), the for loop will be skipped and return None


# Breath First Search creates its own call stack to act like (all) tree branches, branches end in continue -> replaced

def find_route_iter(maze, start, end):  # Children become new starting positions
    stack = [(start, [start])]  # Starting point of each loop iteration, and that point as a list; max length is 2

    while stack:
        current, path = stack.pop()  # Current becomes the point and path becomes the list

        # Base Case: Checks if you've reached the end of the maze
        if current == end:
            return path

        # Base Case: current starting point in the loop or end point isn't present in the maze
        if start not in maze.transitions or end not in maze.transitions:
            continue  # Current branch in stack won't have it's children evaluated, and was already destroyed by pop

        # Iteration: every dictionary value is a child whose children will also be examind till you've reached the end
        for child in maze.transitions[current]:
            stack.append((child, path + [child]))  # Tree: every new, possible branch will take the place of the old

    return None

if __name__ == "__main__":
    # Script code here

    # Defining properties of the maze
    transitions = {
        (0, 0): [(1, 0)],
        (1, 0): [(2, 0), (1, 1)],
        (2, 0): [],
        (1, 1): [(1, 2)],
        (1, 2): [(2, 2)],
        (2, 2): []
    }

    # Initializing variables
    start = (0, 0)
    end = (5, 2)
    maze = Maze(start, transitions)
    solution = find_route(maze, end)

    # Returning solution to user
    print(solution)
    maze.show(solution)
