import matplotlib.pyplot as plt

# Room data (coordinates and passageways)
rooms = [
    {'coords': (0, -5), 'passages': 'Staircase leads down to this room; passageway to Room 2'},
    {'coords': (2, -5), 'passages': 'Staircase from Room 1; passageway to Room 3'},
    {'coords': (3, -3), 'passages': 'Corridor from Room 2; passageway to Room 4'},
    {'coords': (1, -3), 'passages': 'Corridor from Room 3; passageway to Room 5'},
    {'coords': (4, -1), 'passages': 'Laboratory from Room 4; passageway to Room 6'},
    {'coords': (3, 1), 'passages': 'Laboratory from Room 5; passageway to Room 7'},
    {'coords': (6, 1), 'passages': 'Corridor from Room 6; passageway to Room 8'},
    {'coords': (6, -1), 'passages': 'Laboratory from Room 7; passageway to Room 9'},
    {'coords': (8, -1), 'passages': 'Control room from Room 8; exit to the outside world'}
]

# Function to plot the dungeon map
def plot_dungeon(rooms):
    fig, ax = plt.subplots()

    # Plot each room
    for i, room in enumerate(rooms):
        x, y = room['coords']
        ax.plot(x, y, 'bo')  # plot the room as a blue dot
        ax.text(x, y, f'Room {i+1}', fontsize=9, ha='right')  # label the room

        # Plot passage connections (straight lines between rooms)
        if i > 0:
            prev_x, prev_y = rooms[i-1]['coords']
            ax.plot([prev_x, x], [prev_y, y], 'k-', lw=1)  # draw line between current and previous room

    # Setting up the plot limits and grid
    ax.set_xlim(-1, 9)
    ax.set_ylim(-6, 2)
    ax.grid(True)
    ax.set_title("Dungeon Map")

    plt.show()

# Call the function to draw the map
plot_dungeon(rooms)
