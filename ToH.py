from enum import Enum
import os

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
        self.steps = 0  # Add step counter

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
    def move(self, source, destination, clear_screen=True):
        if source.is_empty():
            raise Exception("Source tower is empty.")
        disk = source.peek()
        if not destination.is_empty() and destination.peek().width < disk.width:
            raise Exception("Cannot place larger disk on smaller disk")
        disk = source.pop()
        destination.push(disk)
        self.steps += 1  # Increment step counter
        print(f"Step {self.steps}: Move {disk} from {source.position.name} to {destination.position.name}")
        self.print_towers(clear_screen=clear_screen)

    # Recursive method to solve the Tower of Hanoi problem
    def solve_towers(self, n, start_pole, temp_pole, end_pole):
        if n == 1:
            self.move(start_pole, end_pole, clear_screen=False)
            return
        self.solve_towers(n - 1, start_pole, end_pole, temp_pole)
        self.move(start_pole, end_pole, clear_screen=False)
        self.solve_towers(n - 1, temp_pole, start_pole, end_pole)

    # Starts the solving process and prints the initial state
    def solve(self):
        self.steps = 0  # Reset step counter for auto-solve
        self.print_towers(clear_screen=False)
        self.solve_towers(self.num_disks, self.left, self.center, self.right)

    # Interactive game loop for Tower of Hanoi
    def play(self):
        """
        Runs the interactive Tower of Hanoi game.
        Prompts the user to select source and destination towers for each move.
        Validates moves and prints the state after each move.
        Ends when all disks are moved to the right tower or the user quits.
        Displays the number of steps taken.
        Offers a retry option after quitting.
        """
        while True:
            print("Welcome to the Tower of Hanoi!")
            print("Type 'Q' at any prompt to quit and give up.")
            self.print_towers()
            steps = 0  # Step counter
            # Main game loop: continue until all disks are on the right tower
            while not self.right.size == self.num_disks:
                try:
                    # Get user input for source and destination towers
                    src = input("Enter source tower (L/C/R or Q to quit): ").strip().upper()
                    if src == "Q":
                        print(f"You gave up after {steps} moves. Better luck next time!")
                        break
                    dst = input("Enter destination tower (L/C/R or Q to quit): ").strip().upper()
                    if dst == "Q":
                        print(f"You gave up after {steps} moves. Better luck next time!")
                        break
                    src_tower = self._parse_tower(src)
                    dst_tower = self._parse_tower(dst)
                    # Check if source tower is empty
                    if src_tower.is_empty():
                        print("Source tower is empty. Try again.")
                        continue
                    try:
                        # Attempt to move disk and print towers
                        self.move(src_tower, dst_tower)
                        steps += 1  # Increment step counter
                    except Exception as e:
                        print(f"Invalid move: {e}")
                except (KeyboardInterrupt, EOFError):
                    # Handle user exit
                    print(f"\nGame exited after {steps} moves.")
                    break
            # Congratulate user if puzzle is solved
            if self.right.size == self.num_disks:
                print(f"Congratulations! You solved the puzzle in {steps} moves.")
            # Ask if user wants to retry
            retry = input("Do you want to play again? (Y/N): ").strip().upper()
            if retry != "Y":
                print("Thanks for playing!")
                break
            # Reset towers for retry
            self.left = Tower(Position.LEFT)
            self.center = Tower(Position.CENTER)
            self.right = Tower(Position.RIGHT)
            for width in range(self.num_disks, 0, -1):
                self.left.push(Disk(width))

    def _parse_tower(self, s):
        """
        Helper method to convert user input (L/C/R) to the corresponding tower object.
        Raises ValueError for invalid input.
        """
        if s == "L":
            return self.left
        elif s == "C":
            return self.center
        elif s == "R":
            return self.right
        else:
            raise ValueError("Invalid tower selection. Use L, C, or R.")

    # Prints the current state of all towers with terminal GUI
    def print_towers(self, clear_screen=True):
        # ANSI color codes
        RESET = "\033[0m"
        CYAN = "\033[96m"
        YELLOW = "\033[93m"
        GREEN = "\033[92m"
        MAGENTA = "\033[95m"
        RED = "\033[91m"
        BOLD = "\033[1m"

        def get_disks(tower):
            disks = []
            current = tower.top_node
            while current:
                disks.append(current.data.width)
                current = current.next
            return disks[::-1] 

        left_disks = get_disks(self.left)
        center_disks = get_disks(self.center)
        right_disks = get_disks(self.right)
        max_height = max(len(left_disks), len(center_disks), len(right_disks), self.num_disks)
        max_disk = self.num_disks

        # Helper to draw a disk or empty space
        def draw_disk(width, color):
            if width == 0:
                return f"{BOLD}{color}{' ' * max_disk}|{' ' * max_disk}{RESET}"
            else:
                return f"{BOLD}{color}{' ' * (max_disk - width)}" + \
                       "=" * width + "|" + "=" * width + \
                       " " * (max_disk - width) + RESET

        if clear_screen:
            os.system('cls' if os.name == 'nt' else 'clear')
        print(f"{MAGENTA}{BOLD}\n╔════════════════════════════════════════════════════════════╗")
        print("║                  TOWER OF HANOI QUEST!                     ║")
        print("╚════════════════════════════════════════════════════════════╝\n" + RESET)
        print(f"   {CYAN}L".ljust(max_disk*2+2), f"{YELLOW}C".ljust(max_disk*2+2), f"{GREEN}R".ljust(max_disk*2+2) + RESET)
        # Print from bottom to top so largest disks are at the bottom
        for i in range(max_height-1, -1, -1):
            l = left_disks[i] if i < len(left_disks) else 0
            c = center_disks[i] if i < len(center_disks) else 0
            r = right_disks[i] if i < len(right_disks) else 0
            print(draw_disk(l, CYAN), draw_disk(c, YELLOW), draw_disk(r, GREEN))
        print(f"{MAGENTA}{'-' * ((max_disk*2+2)*3)}{RESET}")

# Example usage when running this file directly
if __name__ == "__main__":
    import time
    try:
        os.system('cls' if os.name == 'nt' else 'clear')
        print("\033[95m\033[1m")
        print("╔════════════════════════════════════════════════════════════╗")
        print("║                  WELCOME TO TOWER OF HANOI                 ║")
        print("╚════════════════════════════════════════════════════════════╝")
        print("\033[0m")
        time.sleep(0.5)
        num = int(input("Enter number of disks (default 3): ") or "3")
    except ValueError:
        num = 3
    solver = HanoiSolver(num)
    print("\nChoose your mode:")
    print("  1. Play (interactive)")
    print("  2. Auto-solve (watch the magic!)")
    print("  3. ??? (mystery mode)")  # New mode
    mode = input("Type 'play' for interactive game, 'mystery' for the new mode, anything else for auto-solve: ").strip().lower()
    if mode == "play":
        print("\n\033[92mGet ready for your quest!\033[0m")
        time.sleep(0.5)
        solver.play()
    elif mode == "mystery":
        print("\n\033[95mYou have entered the mystery mode. (Coming soon!)\033[0m")
        # Placeholder: does nothing for now
    else:
        print("\n\033[93mAuto-solving the puzzle...\033[0m")
        time.sleep(0.5)
        solver.solve()

