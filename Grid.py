import tkinter as tk


class Grid:
    # All colors used are listed here so that they can be changed easily
    SHIP_COLOR = "LightSteelBlue3"
    HIT_COLOR = "red"
    MISSED_COLOR = "midnight blue"
    WATER_COLOR = "dodger blue"
    SQUARE_SELECTED = "white"

    # Initializes the object by initializing the variables
    def __init__(self, parent, size):
        self.parent = parent
        self.size = size  # The grid is a square so this is both the vertical and horizontal size
        self.squares = []
        for x in range(self.size):
            parent.grid_columnconfigure(x, weight=1)
            # Nested for loops so that a grid of squares is created, with all possible rows and columns
            # up to the specified size
            for y in range(self.size):
                parent.grid_rowconfigure(y, weight=1)
                square = tk.Label(parent, bg=self.WATER_COLOR, borderwidth=1, relief=tk.RIDGE)
                square.grid(column=x, row=y, sticky=tk.NSEW)
                self.squares.append(square)

    def reset(self):  # Resets all of the squares to their original attributes
        for square in self.squares:
            square["bg"] = self.WATER_COLOR  # The color is reset to the default color
            # All possible bindings are removed so that squares don't follow behaviour of the old grid
            # (e.g. ships aren't placed when in the firing grid). New bindings can then be created
            square.unbind("<Enter>")
            square.unbind("<Leave>")
            square.unbind("<Button-1>")
            square.unbind("<Button-3>")

    def get_square(self, x, y):  # Gets a square based on its x and y co-ordinates
        # The outer for loop in `redraw` iterated over x. This means that when x increases by 1, all of the possible
        # y values have been iterated over. There are `self.size` such values, so when x has increased by 1, the
        # number of squares has increased by `self.size`. y is increased in the inner for loop, so when y increases
        # by 1, the number of squares increases by 1. Thus to get a square by co-ordinates we use x * self.size + y.
        return self.squares[x * self.size + y]
