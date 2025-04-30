# Global counter variable
move_count = 0

def tower_of_hanoi(n, source, auxiliary, destination):
    global move_count
    if n == 1:
        move_count += 1
        print(f"Move {move_count}: Move disc 1 from {source} to {destination}")
        return
    tower_of_hanoi(n - 1, source, destination, auxiliary)
    move_count += 1
    print(f"Move {move_count}: Move disc {n} from {source} to {destination}")
    tower_of_hanoi(n - 1, auxiliary, source, destination)

# Solve for 6 discs
num_discs = 6
print(f"Solving Tower of Hanoi with {num_discs} discs:\n")
tower_of_hanoi(num_discs, 'A', 'B', 'C')
print(f"\nTotal moves: {move_count}")
