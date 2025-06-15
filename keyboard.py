rows_keyboard = [
    ["Q","W","E","R","T","Y","U","I","O","P"],
    ["A","S","D","F","G","H","J","K","L"],
    ["Enter","Z","X","C","V","B","N","M","⌫"]
]

# A list within a list 
# qwerty keyboard has 3 elements row1, row2 , row3
# within each row row1 will have all the letter elements 
#so when we loop over qwerty keyboard - its looping the 3 rows 
#if we nest a loop of a row within it - it will loop over the letters in that row 
#very similar to when we create a grid of squares - difference is now we are also dealing with the values that are at the