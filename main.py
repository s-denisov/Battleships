import tkinter as tk
from tkinter import messagebox
from Player import Player
from Grid import Grid

GRID_SIZE = 10  # Makes the size of the grid clear so that it can be modified easily


class Game:
    def __init__(self, parent):  # Initializes the variables
        self.parent = parent
        self.grid = Grid(parent, GRID_SIZE)

    def new_game(self):
        # New players are created, with new (initially empty) lists of ship coordinates and shots fired
        player1 = Player("Player 1", self.grid)
        player2 = Player("Player 2", self.grid)
        # player1 is prompted to place ships. An anonymous function is passed in so that after player1 has finished,
        # this function is called by player1 and player2 may begin. An anonymous function is also passed to player2
        # so that once player2 has finished, the player screen of player1 is shown, and thus player1 starts a move.
        player1.place_ships(lambda: player2.place_ships(lambda:
                                                        self.show_player_screen(player1, player2)))
    
    def show_player_screen(self, current_player, other_player):
        # A messagebox is used to make it clear what is happening, and also so that the player ships aren't shown until
        # tbe messagebox is closed, thus preventing the opponent from seeing the ships after the opponent's move.
        messagebox.showinfo(current_player.name, "Next turn")
        self.parent.title(current_player.name)  # Sets the title of the window to the player name
        current_player.display_player_screen(other_player.fired_coordinates)

        game_over = True
        # If for all ship co-ordinates of the current player, these are in the list of fired co-ordinates of the
        # opponent, then all of the current player's ships have been hit so the game is over. This is checked by
        # setting game_over to True initially, and setting it to False if any ship co-ordinates are found, at which
        # the opponent hasn't fired.
        for coords in current_player.ship_coordinates:
            if coords not in other_player.fired_coordinates:
                game_over = False
                # Stops the execution of the for loop, as we know that game_over is False so more checks are unnecessary
                break

        if game_over:
            new_game_chosen = messagebox.askyesno(other_player.name + " won", "New game?")
            if new_game_chosen:  # If "yes" was clicked
                self.grid.reset()
                self.new_game()  # A new game is started, with new players created.
            else:
                self.parent.destroy()  # Destroys the parent, thus terminating the application
        else:
            # Gives the current player 3 seconds to look at what ships the opponent has hit, and how the opponent
            # has missed. After that, shows the opponent screen, allowing the player to fire.
            self.parent.after(3000, lambda: self.show_opponent_screen(current_player, other_player))
    
    def show_opponent_screen(self, current_player, other_player):
        # First shows the opponent screen. After the current player has fired, the game moves on to the next move,
        # by showing the other player's player screen. This is done by calling show_player_screen, with
        # current_player and other_player swapped.
        current_player.display_opponent_screen(other_player.ship_coordinates,
                                               lambda: self.show_player_screen(other_player, current_player))


root = tk.Tk()
root.resizable(0, 0)  # Prevents the user from resizing the application, as resizing it would ruin the layout
root.geometry("500x500")  # Sets the width and height of the application to 500 pixels.

game = Game(root)
game.new_game()  # Starts a new_game

root.mainloop()  # Starts the mainloop, so that the application isn't immediately closed
