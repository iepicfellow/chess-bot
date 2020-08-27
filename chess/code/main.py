import tkinter as tk
import chessboard_detection
import cv2 
import board_basics
from game_state_classes import *
from tkinter.simpledialog import askstring
from time import sleep
import keyboard

def clear_logs():
    logs_text.delete('1.0', tk.END)

def add_log(log):
    logs_text.insert(tk.END,log + "\n")

def stop_playing():
    clear_logs()
    button_start = tk.Button(text="Start playing - RESTART NOT WORKING YET", command =start_playing)
    button_start.grid(column=0,row =1)

def start_playing():
    t = 1
    game_state = Game_state()
    add_log("Looking for a chessboard...")

    found_chessboard, position  = chessboard_detection.find_chessboard()

    if found_chessboard:
        add_log("Found the chessboard " + position.print_custom())
        game_state.board_position_on_screen = position
    else:
        add_log("Could not find the chessboard")
        add_log("Please try again when the board is open on the screen\n")
        return
    

    button_start = tk.Button(text="Stop playing", command =stop_playing)
    button_start.grid(column=0,row =1)



    add_log("Checking if we are black or white...")
    resized_chessboard = chessboard_detection.get_chessboard(game_state)
    game_state.previous_chessboard_image = resized_chessboard

    we_are_white = board_basics.is_white_on_bottom(resized_chessboard)
    game_state.we_play_white = we_are_white
    if we_are_white:
        add_log("We are white" )
        game_state.moves_to_detect_before_use_engine = 0
    else:
        add_log("We are black")
        game_state.moves_to_detect_before_use_engine = 1
        first_move_registered = False
        while first_move_registered == False:
            first_move_string = askstring('First move', 'What was the first move played by white?')
            if len(first_move_string) > 0:
                first_move = chess.Move.from_uci(first_move_string)
                first_move_registered = game_state.register_move(first_move,resized_chessboard)

        add_log("First move played by white :"+ first_move_string)        
    
    while True:
        window.update()
        if game_state.moves_to_detect_before_use_engine == 0:
            if keyboard.is_pressed('esc'):
                game_state.play_next_move()

        found_move, move = game_state.register_move_if_needed()
        if found_move:
            clear_logs()
            add_log("The board :\n" + str(game_state.board) + "\n")
            add_log("\nAll moves :\n" + str(game_state.executed_moves))
    

window = tk.Tk()
window.title("yeet")

label_titre = tk.Label(text="disappear",anchor="e", wraplength = 300)
label_titre.grid(column = 0,row = 0)


button_start = tk.Button(text="Start playing", command =start_playing)
button_start.grid(column=0,row =1)

logs_text = tk.Text(window,width=40,height=25,background='gray')
logs_text.grid(column = 0,row = 2)


window.mainloop()
