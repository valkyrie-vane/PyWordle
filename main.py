from keyboard import rows_keyboard
from rich import print
import random
import json
import tkinter as tk

with open("wordle_answers.json", "r") as f:
    word_list = json.load(f)


hidden_word = random.choice(word_list).upper()
hidden_list = list(hidden_word)
last_click = {"x": None, "y": None}
letter_info_by_row_dict = []
player_guess = []
current_row = 0
current_column = 0
game_over = False
NUM_LETTERS = 5
NUM_TURNS = 6
CELL = 60
x = 0
y = 0
SPACE = 5
NO_SPACES = 4
CANVAS_WIDTH = 800
CANVAS_HEIGHT = 900
MARGIN_TOP = 70
MARGIN_TOP_KEYBOARD = MARGIN_TOP + ((CELL + SPACE)*NUM_TURNS) + MARGIN_TOP
MARGIN_NOT_IN_LIST = MARGIN_TOP + ((CELL + SPACE)*NUM_TURNS)

def main():
    global hidden_word, hidden_list
    root = tk.Tk()
    root.title("Wordle Canvas")

    canvas = tk.Canvas(root, width=800, height=900, bg="black")
    canvas.pack()

    input_cells(canvas)
    canvas.create_text(CANVAS_WIDTH/2, MARGIN_TOP/2, text="Guess the word", font=("Helvetica",16), fill="#CEDFE7", tags="Guess")

    global letter_info_by_row_dict

    letter_info_by_row_dict = qwerty_keyboard(canvas)


    canvas.bind("<Button-1>", lambda myevent: on_click(myevent, canvas))
    
   
    root.mainloop()


def input_cells(canvas):
    for i in range(NUM_TURNS):
        for j in range(NUM_LETTERS):
                margin = (CANVAS_WIDTH - ((NUM_LETTERS*CELL) + (NO_SPACES*SPACE)))/2
                x_start = margin + ((CELL+SPACE)*j)
                y_start = MARGIN_TOP + ((CELL+SPACE) * i)
                x_end = (x_start + CELL)
                y_end = (y_start + CELL)
                input_rectangles = canvas.create_rectangle(x_start, y_start, x_end, y_end, fill="#414142", outline="#CEDFE7", tags="input_cells")   

def qwerty_keyboard(canvas):
    for row_idx, row in enumerate(rows_keyboard):
        letter_info_by_column_branch_dict = []
        for col_idx, letter in enumerate(row):
            margin_keyboard = (CANVAS_WIDTH - (((len(row))*CELL) + (NO_SPACES*SPACE)))/2
            x_start = margin_keyboard + ((CELL+SPACE)*col_idx)
            y_start = MARGIN_TOP_KEYBOARD + ((CELL+SPACE)*row_idx)
            x_end = (x_start + CELL)
            y_end = (y_start + CELL)

            if row_idx == 2 and col_idx == 0:
                x_start = margin_keyboard + ((CELL+SPACE)*col_idx) - (CELL/2)
                rectangle_id = canvas.create_rectangle(x_start, y_start, x_end, y_end, fill="#414142", outline="#CEDFE7")
                text_x_center = x_start+CELL*0.75
                text_y_center = y_start+CELL/2
                text_id = canvas.create_text(text_x_center, text_y_center, text = "Enter", font = ("Helvetica", 16), fill = "#CEDFE7",tags="Enter")
            elif row_idx == 2 and col_idx == len(row)-1:
                x_end = (x_start + CELL) + (CELL/2)
                rectangle_id = canvas.create_rectangle(x_start, y_start, x_end, y_end, fill="#414142", outline="#CEDFE7")
                text_x_center = x_start+CELL*0.75
                text_y_center = y_start+CELL*0.5
                text_id = canvas.create_text(text_x_center, text_y_center, text = "⌫", font = ("Helvetica", 16), fill = "#CEDFE7", tags="⌫")
            else:
                rectangle_id = canvas.create_rectangle(x_start, y_start, x_end, y_end, fill="#414142", outline="#CEDFE7")
                text_x_center = x_start+CELL/2
                text_y_center = y_start+CELL/2
                text_id = canvas.create_text(text_x_center, text_y_center, text = letter, font = ("Helvetica", 16), fill = "#CEDFE7", tags="letters")

            letter_info = {
                "letter": letter,
                "rectangle_coordinates": (x_start, y_start, x_end, y_end),
                "rectangle_id": rectangle_id,
                "text_id": text_id
            }
            letter_info_by_column_branch_dict.append(letter_info)
        letter_info_by_row_dict.append(letter_info_by_column_branch_dict)
    
    return letter_info_by_row_dict


def game_start(canvas):
    
    global player_guess, current_row, current_column, hidden_word, hidden_list, letter_info_by_row_dict, game_over
    player_guess = []
    current_row = 0
    current_column = 0
    hidden_word = random.choice(word_list).upper()
    hidden_list = list(hidden_word)
    canvas.delete("all")
    letter_info_by_row_dict.clear()
    letter_info_by_row_dict = qwerty_keyboard(canvas)
    input_cells(canvas)
    canvas.create_text(CANVAS_WIDTH/2, MARGIN_TOP/2, text="Guess the word", font=("Helvetica",16), fill="#CEDFE7", tags="Guess")
    game_over = False

 
def on_click(event, canvas):
    global letter_info_by_row_dict

    x = event.x
    y = event.y
    last_click["x"] = event.x
    last_click["y"] = event.y
    
    for letter_info_by_column_branch_dict in letter_info_by_row_dict:
        for letter_info in letter_info_by_column_branch_dict:
            x_start, y_start, x_end, y_end = letter_info["rectangle_coordinates"]
            if x_start <= x <= x_end and y_start <= y <= y_end:
                key_press(letter_info["letter"], canvas)
                
def key_press(letter, canvas):
    global player_guess, current_row, current_column, letter_info_by_row_dict, game_over
    if letter == "⌫":
        if len(player_guess) > 0:
            current_column -= 1
            clear_cell(canvas)
            player_guess.pop()

    elif (letter != "Enter" and letter != "⌫") and len(player_guess) < NUM_LETTERS:
        player_guess.append(letter)
          
        margin = (CANVAS_WIDTH - ((NUM_LETTERS*CELL) + (NO_SPACES*SPACE)))/2
        x_start = margin + ((CELL+SPACE)*current_column)
        y_start = MARGIN_TOP + ((CELL+SPACE) * current_row)
        x_end = (x_start + CELL)
        y_end = (y_start + CELL)
        input_rectangles = canvas.create_rectangle(x_start, y_start, x_end, y_end, fill="#1A1A1D", outline="#CEDFE7")
        text_x_center = x_start+CELL/2
        text_y_center = y_start+CELL/2
        text_id = canvas.create_text(text_x_center, text_y_center, text=letter, font = ("Helvetica", 16), fill = "#CEDFE7")
        
        current_column += 1  
        canvas.delete("not_in_list")

    elif game_over == True:
        if letter == "Enter":
            game_start(canvas)
        return
    
    else:
        if letter == "Enter":
            if len(player_guess) < NUM_LETTERS:
                return
            guess_word = "".join(player_guess).lower()

            if guess_word in word_list:
                game_logic(canvas)

                if player_guess == hidden_list:
                    canvas.delete("Guess")
                    canvas.delete("not_in_list")
                    canvas.create_text(CANVAS_WIDTH/2, MARGIN_TOP/2, text="Wohoo! You have won!", font=("Helvetica",16), fill="#CEDFE7")
                    game_over = True
                else:
                    if current_row == 5 and current_column == 5:
                        canvas.delete("Guess")
                        canvas.delete("not_in_list")
                        canvas.create_text(CANVAS_WIDTH/2, MARGIN_TOP/2, text=f"Game Over! The word was {hidden_word}! Press Enter to Try Again.", font=("Helvetica",16), fill="#CEDFE7")
                        game_over = True
                        return                   
            
                current_row += 1
                current_column = 0
                player_guess = []                

            else:
                canvas.delete("Guess")
                canvas.create_text(CANVAS_WIDTH/2, MARGIN_TOP/2, text="Not a valid word! Try again.", font=("Helvetica",16), fill="#CEDFE7", tags="not_in_list")
                margin = (CANVAS_WIDTH - ((NUM_LETTERS*CELL) + (NO_SPACES*SPACE)))/2
                for i in range(NUM_LETTERS):
                    x_start = margin + ((CELL+SPACE)*i)
                    y_start = MARGIN_TOP + ((CELL+SPACE) * current_row)
                    x_end = (x_start + CELL)
                    y_end = (y_start + CELL)
                    input_rectangles = canvas.create_rectangle(x_start, y_start, x_end, y_end, fill="#414142", outline="#CEDFE7")
                current_column = 0 
                player_guess.clear()                
                return

    # canvas.bind("<Key>", key_press)
    # canvas.focus_set()

                        
     

        
def clear_cell(canvas):         
    global player_guess, current_row, current_column
    margin = (CANVAS_WIDTH - ((NUM_LETTERS*CELL) + (NO_SPACES*SPACE)))/2
    x_start = margin + ((CELL+SPACE)*current_column)
    y_start = MARGIN_TOP + ((CELL+SPACE) * current_row)
    x_end = (x_start + CELL)
    y_end = (y_start + CELL)
    input_rectangles = canvas.create_rectangle(x_start, y_start, x_end, y_end, fill="#414142", outline="#CEDFE7")


def game_logic(canvas):
    global player_guess, current_row, current_column
    

    hidden_word_dict = {}
    for letter_hidden_list in hidden_list:
        if letter_hidden_list not in hidden_word_dict:
            hidden_word_dict[letter_hidden_list] = 1 #count
        else:
            hidden_word_dict[letter_hidden_list] += 1 #count


    # keep a count of letters to track repeated letters in a word of the guess list
    guess_word_dict = {}
    for letter_player_guess in player_guess:
        if letter_player_guess not in guess_word_dict:
            guess_word_dict[letter_player_guess] = 1
        else:
            guess_word_dict[letter_player_guess] += 1

    for idx, letter_player_guess in enumerate(player_guess):
            
        if letter_player_guess in hidden_word_dict:

            letter_count_hidden_word_dict = hidden_word_dict[letter_player_guess] # if we start with "p" in poppy this is searching for how many times "p" occurs in apple
            letter_count_guess_word_dict = guess_word_dict[letter_player_guess] # this is searching for how many times "p" occurs in poppy
            
        else:
            letter_count_hidden_word_dict = 0
            letter_count_guess_word_dict = 0

        margin = (CANVAS_WIDTH - ((NUM_LETTERS*CELL) + (NO_SPACES*SPACE)))/2
        x_start = margin + ((CELL+SPACE)*idx)
        y_start = MARGIN_TOP + ((CELL+SPACE) * current_row)
        x_end = (x_start + CELL)
        y_end = (y_start + CELL)

                      
        if letter_player_guess == hidden_list[idx]:
            input_rectangles = canvas.create_rectangle(x_start, y_start, x_end, y_end, fill="#0DAA90", outline="#CEDFE7")
            text_x_center = x_start+CELL/2
            text_y_center = y_start+CELL/2
            text_id = canvas.create_text(text_x_center, text_y_center, text=letter_player_guess, font = ("Helvetica", 16), fill = "#000000")

            hidden_word_dict[letter_player_guess] -= 1
            # Condition for green

        elif letter_player_guess in hidden_list and letter_count_hidden_word_dict >= letter_count_guess_word_dict:
            input_rectangles = canvas.create_rectangle(x_start, y_start, x_end, y_end, fill="#FFB444", outline="#CEDFE7")
            text_x_center = x_start+CELL/2
            text_y_center = y_start+CELL/2
            text_id = canvas.create_text(text_x_center, text_y_center, text=letter_player_guess, font = ("Helvetica", 16), fill = "#000000")
        
        

        else:
            input_rectangles = canvas.create_rectangle(x_start, y_start, x_end, y_end, fill="#242424",stipple="gray25", outline="#CEDFE7")
            text_x_center = x_start+CELL/2
            text_y_center = y_start+CELL/2
            text_id = canvas.create_text(text_x_center, text_y_center, text=letter_player_guess, font = ("Helvetica", 16), fill = "#CEDFE7")


            



if __name__ == "__main__":
    main()


    

