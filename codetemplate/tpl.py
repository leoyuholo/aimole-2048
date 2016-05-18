#Implement your "nextMove" and "isValid" functions.
#You are free to add more functions or remove any function.
#If you are not clear about the rules, click the "Game Rules" button on the player bar.

def is_valid(board, move):
    # Check If the Move is Valid
    # Implement Your Checking Function
    return True
    
def next_move(board):
    # Implement Your AI Here
    if is_valid(board, 'UP'):
        return 'UP'
    
while True:
    # Read Game Board
    board = [[int(x) for x in raw_input().split()]for i in range(4)]
    # Compute Your Next Move
    move = next_move(board)
    # Print Your Next Move to the Standard Output
    print(move)
