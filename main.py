# Welcome to
# __________         __    __  .__                               __
# \______   \_____ _/  |__/  |_|  |   ____   ______ ____ _____  |  | __ ____
#  |    |  _/\__  \\   __\   __\  | _/ __ \ /  ___//    \\__  \ |  |/ // __ \
#  |    |   \ / __ \|  |  |  | |  |_\  ___/ \___ \|   |  \/ __ \|    <\  ___/
#  |________/(______/__|  |__| |____/\_____>______>___|__(______/__|__\\_____>
#
# This file can be a nice home for your Battlesnake logic and helper functions.
#
# To get you started we've included code to prevent your Battlesnake from moving backwards.
# For more info see docs.battlesnake.com

import random
import typing
import sys
import copy
import math


# info is called when you create your Battlesnake on play.battlesnake.com
# and controls your Battlesnake's appearance
# TIP: If you open your Battlesnake URL in a browser you should see this data
def info() -> typing.Dict:
    print("INFO")

    return {
        "apiversion": "1",
        "author": "lalaloo",  # TODO: Your Battlesnake Username
        "color": "#FFA500",  # TODO: Choose color
        "head": "bendr",  # TODO: Choose head
        "tail": "sharp",  # TODO: Choose tail
    }


# start is called when your Battlesnake begins a game
def start(game_state: typing.Dict):
    print("GAME START")
    boardHeight = game_state['board']['height']
    boardWidth = game_state['board']['width']
    timeout = game_state['game']['timeout']
    print('Starting game with %dx%d board and %dms timeout' % (boardHeight, boardWidth, timeout))


# end is called when your Battlesnake finishes a game
def end(game_state: typing.Dict):
    print("GAME OVER\n")


# TODO: calculate the evaluation function value for the current state
# the value should be a function of various attributes of the game state
# such as the current number of move options available, length of each snake,
# number of squares controlled, snake health, distance to nearest food etc.
def distance(a, b):
    """Calculate Manhattan distance between two points"""
    return abs(a['x'] - b['x']) + abs(a['y'] - b['y'])


def get_closest_food(head, food_list):
    """Find the closest food to the snake's head"""
    if not food_list:
        return None, float('inf')
    
    closest = food_list[0]
    min_dist = distance(head, closest)
    
    for food in food_list[1:]:
        dist = distance(head, food)
        if dist < min_dist:
            min_dist = dist
            closest = food
            
    return closest, min_dist


def evaluation_function(game_state):
    """Calculate the evaluation score for the current game state"""
    my_snake = game_state['you']
    my_head = my_snake['body'][0]
    my_health = my_snake['health']
    my_length = my_snake['length']
    
    opponent = game_state['board']['snakes'][0]
    if opponent['id'] == my_snake['id'] and len(game_state['board']['snakes']) > 1:
        opponent = game_state['board']['snakes'][1]
    
    # food calculations
    closest_food, food_dist = get_closest_food(my_head, game_state['board']['food'])
    
    # area control calc
    safe_moves = 0
    for move in ["up", "down", "left", "right"]:
        new_head = get_new_head_position(my_head, move)
        if is_position_safe(new_head, game_state):
            safe_moves += 1
    
    # main eval components
    health_score = my_health / 100.0
    length_score = my_length / (opponent['length'] + 1)
    food_score = 1.0 / (food_dist + 1)
    safety_score = safe_moves / 4.0
    
    # weighted sum
    score = (
        0.3 * health_score +
        0.4 * length_score +
        0.2 * food_score +
        0.1 * safety_score
    )
    
    return score


def get_new_head_position(head, move):
    """Calculate new head position based on move"""
    new_head = head.copy()
    if move == "up":
        new_head["y"] += 1
    elif move == "down":
        new_head["y"] -= 1
    elif move == "left":
        new_head["x"] -= 1
    elif move == "right":
        new_head["x"] += 1
    return new_head


def is_position_safe(position, game_state):
    """Check if a position is safe to move to"""
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    
    # Check boundaries
    if (position['x'] < 0 or position['x'] >= board_width or
        position['y'] < 0 or position['y'] >= board_height):
        return False
    
    # Check self collision (skip head)
    for body_part in game_state['you']['body'][1:]:
        if position == body_part:
            return False
    
    # Check other snakes
    for snake in game_state['board']['snakes']:
        if snake['id'] != game_state['you']['id']:
            for body_part in snake['body']:
                if position == body_part:
                    return False
    
    return True

# simulates what the next state will be after a given move
def get_next_state(game_state, move, is_maximizing_player):
    next_game_state = copy.deepcopy(game_state)
    your_snake_index = 0 if game_state['board']['snakes'][0]['id'] == game_state['you']['id'] else 1
    opponent_snake_index = 1 - your_snake_index

    snake = next_game_state['board']['snakes'][your_snake_index] if is_maximizing_player \
            else next_game_state['board']['snakes'][opponent_snake_index]
    new_head = copy.deepcopy(game_state['you']['body'][0])
    if move == "up":
        new_head["y"] += 1
    elif move == "down":
        new_head["y"] -= 1
    elif move == "left":
        new_head["x"] -= 1
    elif move == "right":
        new_head["x"] += 1
    
    snake['health'] -= 1
    snake['head'] = new_head
    snake['body'].insert(0, new_head)
    snake['body'].pop()

    if is_maximizing_player:
        next_game_state['you']['health'] -= 1
        next_game_state['you']['head'] = new_head
        next_game_state['you']['body'].insert(0, new_head)
        next_game_state['you']['body'].pop()

    for food in next_game_state['board']['food']:
        if food == new_head:
            next_game_state['board']['food'].remove(food)
            snake['health'] = 100
            snake['body'].append(snake['body'][-1])
            snake['length'] += 1
            if is_maximizing_player:
                next_game_state['you']['health'] = 100
                next_game_state['you']['body'].append(snake['body'][-1])
                next_game_state['you']['length'] += 1
            break

    return next_game_state

# TODO: implement the minimax algorithm
# game_state: object that stores the current game state
# depth: remaining depth to be searched
#       depth=0 indicates that this is a leaf node / terminal node
# is_maximizing_player:
#       True if your snake (maximizing player) is taking an action
#       False if the opponent's snake (minimizing player) is taking an action
def minimax(game_state, depth, is_maximizing_player, alpha=-math.inf, beta=math.inf):
    """Minimax algorithm with alpha-beta pruning"""
    if depth == 0:
        return evaluation_function(game_state), None
    
    if is_maximizing_player:
        max_eval = -math.inf
        best_move = None
        
        for move in ["up", "down", "left", "right"]:
            new_head = get_new_head_position(game_state['you']['body'][0], move)
            if not is_position_safe(new_head, game_state):
                continue
                
            next_state = get_next_state(game_state, move, True)
            eval_score, _ = minimax(next_state, depth-1, False, alpha, beta)
            
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = move
                
            alpha = max(alpha, eval_score)
            if beta <= alpha:
                break
                
        return max_eval, best_move
    else:
        min_eval = math.inf
        best_move = None
        
        # Find opponent snake
        opponent = None
        for snake in game_state['board']['snakes']:
            if snake['id'] != game_state['you']['id']:
                opponent = snake
                break
        
        if opponent:  # Only if there's an opponent
            for move in ["up", "down", "left", "right"]:
                new_head = get_new_head_position(opponent['head'], move)
                if not is_position_safe(new_head, game_state):
                    continue
                    
                next_state = get_next_state(game_state, move, False)
                eval_score, _ = minimax(next_state, depth-1, True, alpha, beta)
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_move = move
                    
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
                    
        return min_eval, best_move

# move is called on every turn and returns your next move
# Valid moves are "up", "down", "left", or "right"
# See https://docs.battlesnake.com/api/example-move for available data
def move(game_state: typing.Dict) -> typing.Dict:
    # Initialize all moves as safe by default
    is_move_safe = {"up": True, "down": True, "left": True, "right": True}

    # We've included code to prevent your Battlesnake from moving backwards
    my_head = game_state["you"]["body"][0]  # Coordinates of your head
    my_neck = game_state["you"]["body"][1]  # Coordinates of your "neck"

    if my_neck["x"] < my_head["x"]:  # Neck is left of head, don't move left
        is_move_safe["left"] = False
    elif my_neck["x"] > my_head["x"]:  # Neck is right of head, don't move right
        is_move_safe["right"] = False
    elif my_neck["y"] < my_head["y"]:  # Neck is below head, don't move down
        is_move_safe["down"] = False
    elif my_neck["y"] > my_head["y"]:  # Neck is above head, don't move up
        is_move_safe["up"] = False

    # TODO: Prevent your Battlesnake from moving out of bounds
    # board_width = game_state['board']['width']
    # board_height = game_state['board']['height']
    board_width = game_state['board']['width']
    board_height = game_state['board']['height']
    
    # boundary checks 
    if my_head["x"] == 0:
        is_move_safe["left"] = False
    if my_head["x"] == board_width - 1:
        is_move_safe["right"] = False
    if my_head["y"] == 0:
        is_move_safe["down"] = False
    if my_head["y"] == board_height - 1:
        is_move_safe["up"] = False
        
    # TODO: Prevent your Battlesnake from colliding with itself
    # my_body = game_state['you']['body']
    my_body = game_state['you']['body']
    
    # self-collision check (wrapping yourself up)
    for move_dir in is_move_safe:
        if not is_move_safe[move_dir]:
            continue
            
        new_head = get_new_head_position(my_head, move_dir)
        
        # check all body parts except tail 
        for body_part in my_body[:-1]:  
            if new_head == body_part:
                is_move_safe[move_dir] = False
                break

    # TODO: Prevent your Battlesnake from colliding with other Battlesnakes
    # opponents = game_state['board']['snakes']
    opponents = game_state['board']['snakes']
    
    # check collision with other snakes
    for move_dir in is_move_safe:
        if not is_move_safe[move_dir]:
            continue
            
        new_head = get_new_head_position(my_head, move_dir)
        for snake in opponents:
            if snake['id'] == game_state['you']['id']:
                continue  
                
            # check agaisnt all parts of other snakes
            for body_part in snake['body']:
                if new_head == body_part:
                    is_move_safe[move_dir] = False
                    break

    # trying to avoid moves that trap mah snake
    safe_moves = [move for move, isSafe in is_move_safe.items() if isSafe]
    if len(safe_moves) > 1:  
        for move_dir in safe_moves[:]: 
            new_head = get_new_head_position(my_head, move_dir)
            
            
            future_moves = 0
            for future_dir in ["up", "down", "left", "right"]:
                future_pos = get_new_head_position(new_head, future_dir)
                if is_position_safe(future_pos, game_state):
                    future_moves += 1
            
            if future_moves == 0:
                safe_moves.remove(move_dir)
                is_move_safe[move_dir] = False

    # how many safe moves left???
    safe_moves = []
    for move, isSafe in is_move_safe.items():
        if isSafe:
            safe_moves.append(move)

    if len(safe_moves) == 0:
        print(f"MOVE {game_state['turn']}: No safe moves detected! Moving down")
        return {"move": "down"}

    # TODO: Instead of making a random move, use the minimax algorithm to find the optimal move
    # Use minimax with depth 3 for reasonable performance
    _, best_move = minimax(game_state, depth=3, is_maximizing_player=True)
    
    # back to rando if minimax fails
    if best_move is None or best_move not in safe_moves:
        best_move = random.choice(safe_moves) if safe_moves else "down"

    # if health low->food
    if game_state['you']['health'] < 50:
        closest_food, _ = get_closest_food(my_head, game_state['board']['food'])
        if closest_food:
            # move closest to food
            best_dist = float('inf')
            for move_dir in safe_moves:
                new_pos = get_new_head_position(my_head, move_dir)
                dist = distance(new_pos, closest_food)
                if dist < best_dist:
                    best_dist = dist
                    best_move = move_dir

    print(f"MOVE {game_state['turn']}: {best_move}")
    return {"move": best_move}

# Start server when `python main.py` is run
if __name__ == "__main__":
    from server import run_server
    port = "8000"
    for i in range(len(sys.argv) - 1):
        if sys.argv[i] == '--port':
            port = sys.argv[i+1]

    run_server({"info": info, "start": start, "move": move, "end": end, "port": port})
