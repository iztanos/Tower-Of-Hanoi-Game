from enum import Enum

# Enum for representing tower positions
class Position(Enum):
    LEFT = 1
    CENTER = 2
    RIGHT = 3

# Disk class with comparison support for sorting by width
class Disk:
    def __init__(self, width):
        self.width = width

    def __lt__(self, other):
        return self.width < other.width

    def __str__(self):
        return f"Disk({self.width})"

# Basic LinkedStack implementation for tower storage
class LinkedStack:
    class Node:
        def __init__(self, data, next_node=None):
            self.data = data
            self.next = next_node

    def __init__(self):
        self.top_node = None
        self._size = 0

    @property
    def size(self):
        return self._size

    def is_empty(self):
        return self.top_node is None

    def peek(self):
        if self.is_empty():
            raise IndexError("Peek from empty stack")
        return self.top_node.data

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        data = self.top_node.data
        self.top_node = self.top_node.next
        self._size -= 1
        return data

    def push(self, data):
        self.top_node = self.Node(data, self.top_node)
        self._size += 1

    def __len__(self):
        return self._size

    def __str__(self):
        elems = []
        current = self.top_node
        while current:
            elems.append(str(current.data))
            current = current.next
        return "[" + ", ".join(elems) + "]"

# Tower class inheriting LinkedStack with rules for disk placement
class Tower(LinkedStack):
    def __init__(self, position):
        super().__init__()
        self._position = position

    @property
    def position(self):
        return self._position

    # Push method enforcing Tower of Hanoi rule: no larger disk on smaller disk
    def push(self, disk):
        if disk is None:
            raise ValueError("Disk cannot be None")
        if self.is_empty() or self.peek() > disk:
            super().push(disk)
        else:
            raise Exception("Cannot place larger disk on smaller disk")

    def __str__(self):
        return f"Tower {self.position.name}: {super().__str__()}"

# Main solver class for the Tower of Hanoi puzzle
class HanoiSolver:
    def __init__(self, num_disks):
        self.num_disks = num_disks
        self.left = Tower(Position.LEFT)
        self.center = Tower(Position.CENTER)
        self.right = Tower(Position.RIGHT)

        # Initialize all disks on the left tower, largest at bottom
        for width in range(num_disks, 0, -1):
            self.left.push(Disk(width))

    def get_tower(self, pos):
        if pos == Position.LEFT:
            return self.left
        elif pos == Position.CENTER:
            return self.center
        elif pos == Position.RIGHT:
            return self.right
        else:
            raise ValueError("Invalid tower position")

    # Moves a disk from one tower to another and prints the action
    def move(self, source, destination):
        disk = source.pop()
        destination.push(disk)
        print(f"Move {disk} from {source.position.name} to {destination.position.name}")
        self.print_towers()

    # Recursive method to solve the Tower of Hanoi problem
    def solve_towers(self, n, start_pole, temp_pole, end_pole):
        if n == 1:
            self.move(start_pole, end_pole)
            return
        self.solve_towers(n - 1, start_pole, end_pole, temp_pole)
        self.move(start_pole, end_pole)
        self.solve_towers(n - 1, temp_pole, start_pole, end_pole)

    # Starts the solving process and prints the initial state
    def solve(self):
        self.print_towers()
        self.solve_towers(self.num_disks, self.left, self.center, self.right)

    # Prints the current state of all towers
    def print_towers(self):
        print(self.left)
        print(self.center)
        print(self.right)
        print("-" * 40)

# Example usage when running this file directly
if __name__ == "__main__":
    solver = HanoiSolver(3)
    solver.solve()

