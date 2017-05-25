def get_next_turn(active_turn):
    # Change player
    # 1 -> o
    #-1 -> x
    if active_turn == 1:
        next_turn = -1
    else:
        next_turn = 1
    return next_turn

def score(matrix, i_am, depth):
    # Returns +-10 points -+ depth
    # It is the score for user i_am depending on matrix
    # If matrix correspond to a win for user i_am, get 10 points - depth
    # If matrix correspond to a win for the other user, return depth - 10
    # If matrix if not a winning condition, then returns 0
    # The maximum depth is 8 so it seems natural that the max points are 10
    points = 10
    status = game_status(matrix)
    if status==0:
        return 0
    if status==i_am:
        return points - depth
    if status!=i_am:
        return depth - points
    
def get_childs(matrix, turn):
    # turn is 1 or -1
    # 1 -> o
    #-1 -> x
    # 0 -> Free space
    # return all posible plays for user 'turn' ('x' or 'o')
    N = 3
    childs = []
    for i in range(N):
        for j in range(N):
            if matrix[i,j]==0:
                child = matrix.copy()
                child[i,j] = turn
                childs.append(child) 
    return childs

def game_status(matrix):
    # Returns 1 if 'o' win, -1 if 'x' win, 0 if draw 
    points = 1
    if (matrix[0,:].sum() == 3)|(matrix[1,:].sum() == 3)|(matrix[2,:].sum() == 3)|(matrix[:,0].sum() == 3)|(matrix[:,1].sum() == 3)|(matrix[:,2].sum() == 3):
        return points
    if (matrix[0,0]==matrix[1,1])&(matrix[2,2]==matrix[1,1])&(matrix[0,0]==1):
        return points
    if (matrix[0,2]==matrix[1,1])&(matrix[2,0]==matrix[1,1])&(matrix[2,0]==1):
        return points
    if (matrix[0,:].sum() == -3)|(matrix[1,:].sum() == -3)|(matrix[2,:].sum() == -3)|(matrix[:,0].sum() == -3)|(matrix[:,1].sum() == -3)|(matrix[:,2].sum() == -3):
        return -points
    if (matrix[0,0]==matrix[1,1])&(matrix[2,2]==matrix[1,1])&(matrix[0,0]==-1):
        return -points
    if (matrix[0,2]==matrix[1,1])&(matrix[2,0]==matrix[1,1])&(matrix[2,0]==-1):
        return -points
    return 0

def game_over(matrix):
    # status <- Returns 1 if 'o' win, -1 if 'x' win, 0 if draw 
    # game_finished: true is game is over
    game_finished = False
    status = game_status(matrix)
    if status!=0:
        #Game finishes, someone won
        game_finished = True
    if abs(matrix).sum() == 9:
        #No more moves
        game_finished = True
    return game_finished, status

def maximize(matrix, active_turn, player, depth, alpha, beta, nodes_visited):
    game_finished,_ = game_over(matrix)
    if game_finished:
        return None, score(matrix, player, depth), nodes_visited
    depth += 1
    
    infinite_number = 100000
    maxUtility = -infinite_number
    choice = None
    
    childs = get_childs(matrix, active_turn)
    for child in childs:
        nodes_visited = nodes_visited + 1
        _, utility, nodes_visited = minimize(child, get_next_turn(active_turn), player, depth, alpha, beta, nodes_visited)
        
        if utility > maxUtility:
            choice = child
            maxUtility = utility
                
        if maxUtility >= beta:
            break
        if maxUtility > alpha:
            alpha = maxUtility
    return choice, maxUtility, nodes_visited

def minimize(matrix, active_turn, player, depth, alpha, beta, nodes_visited):
    game_finished,_ = game_over(matrix)
    if game_finished:
        return None, score(matrix, player, depth), nodes_visited
    depth += 1
    infinite_number = 100000
    minUtility = infinite_number
    choice = None
    
    childs = get_childs(matrix, active_turn)
    for child in childs:
        nodes_visited = nodes_visited + 1
        _, utility, nodes_visited = maximize(child, get_next_turn(active_turn), player, depth, alpha, beta, nodes_visited)
        
        if utility < minUtility:
            choice = child
            minUtility = utility
            
        if minUtility <= alpha:
            break
        if minUtility < beta:
            beta = minUtility
    return choice, minUtility, nodes_visited

def minimax(matrix, player):
    infinite_number = 1000
    alpha = -infinite_number
    beta = infinite_number
    choice, score, nodes_visited = maximize(matrix, player, player, 0, alpha, beta, 0)
    return choice, score, nodes_visited