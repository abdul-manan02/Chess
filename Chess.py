# First, we will import the chess library which has all the built in functionalities
import chess

# declare a score for each type of piece, this will later when trying to find the next best move
scores = {
    chess.PAWN:   1,
    chess.KNIGHT: 3,
    chess.BISHOP: 3,
    chess.ROOK:   5,
    chess.QUEEN:  9,
    chess.KING:   0
}

# to print valid moves after each iteration of the code
def print_valid_moves(board):
    print("\n\n          VALID MOVES ")
    print("", end = "                       ")
    count = 0
    
    for move in board.legal_moves:
        print(move.uci(), end = "  |  ")
        count = count+1
        if (count==10):
            print()
            print("", end = "                       ")
            count = 0
            
    print("\n")
    

# to evaluate the board to get the score (like the fitness function)
def evaluate(board):
    white = black = 0
    
    # This code basically searches for all the pieces of both players and then computes the sum of their values which have been
    # defined in the "scores" dictionary. The way it does this is by utilizing the built-in function "squares". The For Loop
    # also utilizes the function piece_type to identify each piece type on the board so that it's score can be accessed
    # from the dictionary.
    for i in chess.SQUARES:
        
        piece = board.piece_at(i)
        
        # if piece exists then add scores 
        if piece:
            worth = scores[piece.piece_type]
            
            if piece.color == chess.BLACK:
                black = black + worth
            else:
                white = white + worth
    
    # Subtract the score of white from black.
    # If white's turn, return as is 
    # Else, add - sign and return
    fScore = white - black
    
    if board.turn == chess.BLACK:
        final_score = -final_score
    
    return fScore




# def minimax(board):
#     if terminal(board):
#         return None
#     if player(board) == 'X':
#         v = -math.inf
#         action = None
#         for move in actions(board):
#             min_v = min_val
#             result_board = result(board, move)
#             max_v = max_value(result_board)
#             if max_v > v:
#                 v = max_v
#                 action = move
#         return action
#     else:
#         v = math.inf
#         action = None
#         for move in actions(board):
#             result_board = result(board, move)
#             min_v = min_value(result_board)
#             if min_v < v:
#                 v = min_v
#                 action = move
#         return action
# def alpha_beta_pruining(board):
#     alpha = -math.inf
#     beta = math.inf
#     if terminal(board):
#         return None
#     if player(board) == 'X':
#         v = -math.inf
#         action = None
#         for move in actions(board):
#             min_v = min_value
#             result_board = result(board, move)
#             max_v = max_val(result_board,alpha,beta)
#             if max_v > v:
#                 v = max_v
#                 action = move
#         return action
#     else:
#         v = math.inf
#         action = None
#         for move in actions(board):
#             result_board = result(board, move)
#             min_v = min_val(result_board,alpha,beta)
#             if min_v < v:
#                 v = min_v
#                 action = move
#         return action
    
# Depth will be specified by user, it basically represents the depth till which the algorithm will 
# search for the best solution.
# Alpha will be passed as -∞ whereas beta will be passed as ∞.   
def alphaBeta_min(board, depth, alpha, beta):
    
    # if we have reached depth 0, simply return the score of the board along with 'None' because we have 
    # more moves left to evaluate.
    if depth == 0:
        return evaluate(board), None
    
    
    # Create a 'min' variable that can store the minimum value found after applying algo #
    # Initialize it to ∞ so that the max can be found by using ">", like in PF CPP programs. #
    # 'Best' will store the best move corresponsing to the min score #
    min_ = float('inf')
    best = None
    
    # Search through all valid moves of board position using built in 'legal_moves' function.
    for i in board.legal_moves:
        
        board.push(i)
        assessment, _ = alphaBeta_max(board, depth-1, alpha, beta)
        board.pop()
        
        if assessment < min_:
            min_ = assessment
            best = i
            
        beta = min(beta, assessment)
        
        # to reduce the search space
        if beta <= alpha:
            break
        
    return min_, best
    
def alphaBeta_max(board, depth, alpha, beta):
    
    # if we have reached depth 0, simply return the score of the board along with 'None' because we have 
    # more moves left to evaluate.
    if depth == 0:
        return evaluate(board), None
    
    # Create a 'max' variable that can store the maximum value found after applying algo #
    # Initialize it to -∞ so that the max can be found by using ">", like in PF CPP programs. #
    # 'Best' will store the best move corresponsing to the max score #
    max_ = float('-inf')
    best = None
    
    # Search through all valid moves of board position using built in 'legal_moves' function.
    for i in board.legal_moves:
        
        # The current move is pushed to the board, the min score is calculated 
        # for the oppositon player and then the move is popped out.
        board.push(i)
        assessment, _ = alphaBeta_min(board, depth-1, alpha, beta)
        board.pop()
        
        if assessment > max_:
            max_ = assessment
            best = i
            
        alpha = max(alpha, assessment)
        
        # to reduce the search space
        if beta <= alpha:
            break
        
    return max_, best
    


print("\n * NOTE : CHECK END OF CODE FOR UNDERSTANDING CHESS MOVES *\n")

depth = 4
board = chess.Board()
alpha = float('-inf')
beta = float('inf')

# infinite loop until either side wins or we get a stalemate #
while not board.is_game_over():
    
    # AI's turn (White)#
    if board.turn:
        _, move = alphaBeta_max(board, depth, alpha, beta)
        board.push(move)
        
    # Human's turn #
    else:
        print("\n")
        print(board)
        print_valid_moves(board)
        
        
        action = input("ACTION : ")
        
        # Convert the suer entered value to a format that can be used by the chess library. #
        # Keep asking for input until valid move is entered.
        action = chess.Move.from_uci(action)
        
        while action not in board.legal_moves:
            print("\nINVALID ACTION. INPUT AGAIN!!!")
            action = input("\nACTION : ")
            action = chess.Move.from_uci(action)
            
        board.push(action)

# FINAL OUTPUT #
print("\n\nFINAL BOARD \n\n")
print(board)

if board.is_checkmate():
    if board.turn:
        print("HUMAN WINS")
    else:
        print("AI WINS")
else:
    print("DRAW")
    

######################################                                           
#  The rows are named a-h starting    
#        from the left.                
#  The columns are named 1-8 
#  starting from White (captial).
# The column 1,2 are occupied
#      by white at start.
# The columns 8,7 are occupied
#       by black at start.           
######################################  

#                 MOVE FORMAT                     #
# suppose you want to move the pawn from a2 to a3 #
#                 MOVE : a2a3                     #
