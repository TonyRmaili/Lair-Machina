import random


def generate_dungeon_grid(rows, cols, target_room_ratio=0.4):
    # Initialize the grid with walls represented by '-'
    dungeon_map = [['-' for _ in range(cols)] for _ in range(rows)]

    # Total number of cells
    total_cells = rows * cols
    # Calculate the target number of rooms based on the room ratio
    target_rooms = min(int(total_cells * target_room_ratio), total_cells)

    current_rooms = 0

    # Random starting point
    start_x = random.randint(0, rows - 1)
    start_y = random.randint(0, cols - 1)

    # Helper function for checking if a cell is in bounds
    def in_bounds(x, y):
        return 0 <= x < rows and 0 <= y < cols

    # Define possible directions (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Depth-First Search algorithm to carve out rooms and paths
    def carve_path(x, y):
        nonlocal current_rooms
        # Mark the current cell as a room ('O')
        dungeon_map[x][y] = 'O'
        current_rooms += 1

        # Shuffle directions to ensure random paths
        random.shuffle(directions)

        # Explore each direction
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy

            # Check if the new position is within bounds and has not been visited yet (is a wall)
            if in_bounds(new_x, new_y) and dungeon_map[new_x][new_y] == '-' and current_rooms < target_rooms:
                # Make sure the new position connects to a valid room
                if count_adjacent_rooms(new_x, new_y) <= 1:  # Avoid loops
                    carve_path(new_x, new_y)

    # Helper function to count adjacent rooms
    def count_adjacent_rooms(x, y):
        count = 0
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy
            if in_bounds(new_x, new_y) and dungeon_map[new_x][new_y] == 'O':
                count += 1
        return count

    # Start carving paths from the initial random starting point
    carve_path(start_x, start_y)

    # Now randomly add rooms to meet the target room count
    while current_rooms < target_rooms:
        random_x = random.randint(0, rows - 1)
        random_y = random.randint(0, cols - 1)

        if dungeon_map[random_x][random_y] == '-':
            dungeon_map[random_x][random_y] = 'O'
            current_rooms += 1

    return dungeon_map

def print_dungeon_map(dungeon_map):
    for row in dungeon_map:
        print(' '.join(row))

def filter_empty_rows(dungeon_map):
    # Filter out rows that are completely empty (contain only '-')
    filtered_map = [row for row in dungeon_map if not all(cell == '-' for cell in row)]

    # Optionally, you can return a grid without the first and last element after filtering
    # if len(filtered_map) > 2:
    #     filtered_map = filtered_map[1:-1]

    return filtered_map


def count_rooms(dungeon_map):
    room_count = 0
    # Loop through each row in the dungeon map
    for row in dungeon_map:
        # Count the occurrences of 'O' in each row and add to the total room count
        room_count += row.count('O')
    return room_count


def generate_room_data(dungeon_map):
    room_data = {}
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # up, down, left, right
    room_id = 1  # Initialize room ID starting at 1

    # Loop through the dungeon map using row and column indices
    for row_index, row in enumerate(dungeon_map):
        for col_index, cell in enumerate(row):
            # If the cell is a room ('O'), add it to the dictionary with coordinates
            if cell == 'O':
                # Use 1-based indexing for coordinates
                room_data[room_id] = {
                    'coord': (row_index + 1, col_index + 1),  # 1-based coordinates
                    'connections': []  # Initialize an empty list for connections
                }

                # Check for connections to adjacent rooms
                for dx, dy in directions:
                    new_x = row_index + dx
                    new_y = col_index + dy
                    # Ensure the new position is within bounds and is a room
                    if 0 <= new_x < len(dungeon_map) and 0 <= new_y < len(row) and dungeon_map[new_x][new_y] == 'O':
                        room_data[room_id]['connections'].append((new_x + 1, new_y + 1))  # Store 1-based coordinates

                room_id += 1  # Increment room ID for the next room

    return room_data


def room_data_to_text(room_data):
    # Reverse the room_data dictionary to map coordinates to room IDs
    coord_to_room_id = {info['coord']: room_id for room_id, info in room_data.items()}
    
    # Create a list to store the formatted text for each room
    output_lines = []

    # Loop through each room in room_data
    for room_id, info in room_data.items():
        # Map coordinates of connections to their respective room IDs
        connected_rooms = [coord_to_room_id[coord] for coord in info['connections']]
        # Format the output for the current room
        connected_rooms_str = ', '.join(str(room) for room in connected_rooms)
        room_info = f"Room ID: {room_id}, Coordinates: {info['coord']}, Connections: to room {connected_rooms_str}"
        output_lines.append(room_info)

    # Return the formatted text as a single string, with each room's info on a new line
    return '\n'.join(output_lines)


def run_dungeon_maker(rows=4,cols=4,room_ratio=0.3):
    dungeon_map = generate_dungeon_grid(rows=rows,cols=cols,target_room_ratio=room_ratio)
    filtered_map = filter_empty_rows(dungeon_map=dungeon_map)
    room_count = count_rooms(dungeon_map=filtered_map)

    room_data = generate_room_data(dungeon_map=filtered_map)

    return filtered_map,room_count,room_data


if __name__=='__main__':


    map,room_count,data = run_dungeon_maker()

    print_dungeon_map(dungeon_map=map)

    print(data)

    print(room_count)

    # rows = 4
    # cols = 4
    # target_room_ratio = 0.3 # Adjust the ratio of rooms

    # dungeon_map = generate_dungeon_grid(rows, cols, target_room_ratio)
    # filtered_map = filter_empty_rows(dungeon_map=dungeon_map)
    # print_dungeon_map(dungeon_map=filtered_map)

    # rooms = count_rooms(filtered_map)
    # print(f'room count {rooms}')

    # room_data = generate_room_data(filtered_map)

    # for room_id, info in room_data.items():
    #     print(f"Room ID: {room_id}, Coordinates: {info['coord']}, Connections: {info['connections']}")