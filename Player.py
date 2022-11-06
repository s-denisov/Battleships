from Grid import Grid
from tkinter import messagebox


class Player:
    # Lists all of the ship sizes here, so that they can be changed easily.
    # The order listed is the order in which the player is prompted to place the ships.
    SHIP_SIZES = [5, 4, 3, 3, 2]

    def __init__(self, name, grid):  # Initializes all of the variables
        self.ship_coordinates = []
        self.fired_coordinates = []
        self.vertical = True  # True means ships are placed vertically, False means horizontally
        self.ship_size_index = 0  # Contains the index of the ship currently being placed, based on SHIP_SIZES
        self.fired = False
        self.grid = grid
        self.name = name  # Stores the player's name. Isn't used in this class, but allows easy access outside of it.

    def place_ships(self, after):  # `after` is a function to be ran after all the ships have been placed
        messagebox.showinfo(self.name, "Placing ships")
        self.grid.reset()  # Draws a new grid, as the grid needs to be empty for ships to be placed
        for x in range(self.grid.size):
            for y in range(self.grid.size):
                square = self.grid.get_square(x, y)  # Gets the square from the ones created by the grid
                # When a mouse is hovered over a square, squares corresponding to the ship are selected
                square.bind("<Enter>", lambda event, x2=x, y2=y: self.update_ship(True, x2, y2))
                # When a mouse stops being hovered over a square, squares corresponding to the ship are deselected.
                square.bind("<Leave>", lambda event, x2=x, y2=y: self.update_ship(False, x2, y2))
                # On left click, the ship is placed.
                square.bind("<Button-1>", lambda event, x2=x, y2=y: self.place_ship(x2, y2, after))
                # On right click, the orientation of the ship placed is changed
                square.bind("<Button-3>", lambda event, x2=x, y2=y: self.flip_orientation(x2, y2))

    def flip_orientation(self, x, y):
        self.update_ship(False, x, y)  # Removes the shown ship selected
        self.vertical = not self.vertical  # Will affect all selections, until the orientation is flipped again
        # Adds a new ship selection, with the correct orientation, based on current mouse position.
        self.update_ship(True, x, y)

    # Used during the initial ship placement. If `select` is true, then squares corresponding to the ship are marked
    # as selected by coloring them with the ship color. If `select` is false, these squares are marked as unselected,
    # by coloring them with the water color
    def update_ship(self, select, x, y):  # x and y are co-ordinates of the square where the mouse is
        coordinates = self.find_coordinates(x, y)
        for (x, y) in coordinates:
            square = self.grid.get_square(x, y)
            if select:
                square["bg"] = Grid.SHIP_COLOR
            else:
                square["bg"] = Grid.WATER_COLOR

    def place_ship(self, x, y, after):
        coordinates_of_ship = self.find_coordinates(x, y)
        if not coordinates_of_ship:  # Checks if coordinates_of_ship is empty
            # If the coordinates of the current ship are invalid, then the execution of the function stops.
            # In particular, this means that the ship_size_index isn't increased.
            return
        # Adds all items from the list of found coordinates to the list of ship coordinates of the player
        self.ship_coordinates.extend(self.find_coordinates(x, y))
        self.ship_size_index += 1  # Increases the index, thus moving on to the next ship size
        if self.ship_size_index >= len(self.SHIP_SIZES):
            # If the index is out of range then all of the ships have been placed, so `after` is called, resulting in
            # the next part of the program being executed.
            after()

    # Finds the co-ordinates of the squares corresponding to the square selected during the initial ship placement
    def find_coordinates(self, x, y):
        if self.ship_size_index >= len(self.SHIP_SIZES):
            return []  # If all ships have already been selected, then no co-ordinates are returned
        coordinates = []  # The result of the function. It will be filled later, and finally returned.
        if self.vertical:
            # The co-ordinates of the mouse correspond to the top square. This means the bottom square is at
            # `y + ship size`. This means that if y is more than `grid size - ship size`, then the ship would go off
            # the grid. In this case, the vertical position of the mouse is ignored and y is set to the highest
            # possible value: `grid size - ship size`. This means that if the mouse is positioned too low, then the
            # ship is shown as if the mouse was at the lowest allowed position.
            y = min(y, self.grid.size - self.get_ship_size())
        else:
            # This follows the same logic as y, but for the horizontal orientation
            x = min(x, self.grid.size - self.get_ship_size())
        for i in range(self.get_ship_size()):
            # If the orientation is vertical, then the x position is the same as the position of the mouse, while the
            # y position varies, being 0 to `ship size - 1`, more than the position of the mouse. The opposite is true
            # if the orientation is horizontal.
            result = (x, y + i) if self.vertical else (x + i, y)
            if result in self.ship_coordinates:
                # If any of the squares match existing placed ships, then the selected ship overlaps with an existing
                # ship so its position is invalid and therefore no ship is shown until the mouse is moved to a valid
                # position.
                return []
            coordinates.append(result)
        return coordinates

    def get_ship_size(self):  # Finds the ship size based on the current index of the ship size
        return self.SHIP_SIZES[self.ship_size_index]

    def display_player_screen(self, opponent_fired_coordinates):
        self.grid.reset()  # Resets the grid, as existing square colors and mouse bindings are likely incorrect
        # Creates a copy of the opponent_fired_coordinates list. The copy can be modified without modifying the
        # original list.
        opponent_missed = opponent_fired_coordinates[:]
        for coordinates in self.ship_coordinates:
            # * is the spread operator so that instead of self.grid.get_square((x, y)),
            # self.grid.get_square(x, y) is called.
            square = self.grid.get_square(*coordinates)
            # The square is initially set to the ship color as it is one of the ship co-ordinates
            square["bg"] = Grid.SHIP_COLOR
            if coordinates in opponent_fired_coordinates:
                # In this case, the square is the co-ordinate of a ship and has also been fired at. Therefore it is a
                # hit so it is set to the hit color.
                square["bg"] = Grid.HIT_COLOR
                opponent_missed.remove(coordinates)  # This is a hit soi it is removed from the missed coordinates.
        # The list of missed co-ordinates started as the list of all fired co-ordinates but has all co-ordinates that
        # hit removed. Thus all of the remaining items are misses and are therefore set to the missed color.
        for coordinates in opponent_missed:
            self.grid.get_square(*coordinates)["bg"] = Grid.MISSED_COLOR

    def display_opponent_screen(self, opponent_ship_coordinates, after):
        self.grid.reset()
        self.fired = False  # Resets self.fired, in case it was set to True during a previous turn
        for x in range(self.grid.size):  # Iterates through all of the squares by using co-ordinates
            for y in range(self.grid.size):

                def color_on_leave(widget, x2, y2):  # Returns a square to its original color
                    if (x2, y2) in self.fired_coordinates:
                        # If the square has been fired at, then it is set to the hit or miss color, depending
                        # on if it has been hit.
                        widget["bg"] = Grid.HIT_COLOR if (x2, y2) in opponent_ship_coordinates else Grid.MISSED_COLOR
                    else:  # If the square hasn't been fired at then it must have had the default (water) color
                        widget["bg"] = Grid.WATER_COLOR

                square = self.grid.get_square(x, y)
                # When a square is hovered over, it is colored, to show the user that it is selected
                square.bind("<Enter>", lambda event: event.widget.configure(bg=Grid.SQUARE_SELECTED))
                # When a square stops being hovered over, it is returned to its original color. The color_on_leave
                # procedure is used to find and set this color.
                square.bind("<Leave>", lambda event, x2=x, y2=y: color_on_leave(event.widget, x2, y2))
                # If (x, y) is one of the co-ordinates of the opponent's ship, then the shot is a hit so the hit color
                # is used. Otherwise, the shot is a miss so the missed color is used.
                new_color = Grid.HIT_COLOR if (x, y) in opponent_ship_coordinates else Grid.MISSED_COLOR
                if (x, y) in self.fired_coordinates:
                    square["bg"] = new_color
                else:
                    # In the lambda, the variables used in the for loop
                    # are set to new variables (e.g. x2=x), because the variables used in the for loop (e.g. x)
                    # will change with each iteration, but the current ones need to be used in the lambda
                    square.bind("<Button-1>", lambda event, x2=x, y2=y, nc=new_color: self.handle_fired(
                        event.widget, x2, y2, nc, after))  # When the square is right-clicked, the shot is fired

    def handle_fired(self, square, x, y, new_color, after):
        if self.fired:  # This prevents the user from firing multiple shots in a single turn during the delay
            return  # Immediately stops execution of the procedure
        self.fired_coordinates.append((x, y))  # Adds the co-ordinates of the square to the list of fired co-ordinates
        square["bg"] = new_color
        self.fired = True
        # After the shot is fired, the next screen is shown by calling `after`.
        # Only calls `after` after 3 seconds, so that the user has time to see whether the shot hit or missed.
        self.grid.parent.after(2000, after)
