import random
import time

def algorithm_provider(possible_move, all_enemy_possible_move, current_board, check_if_king_in_check, type_algorithm):
    if type_algorithm == 1:
        return play_random(possible_move)
    elif type_algorithm == 2:
        return priority_move(possible_move, all_enemy_possible_move, current_board, check_if_king_in_check)
    # handle any algorithm
    else:
        return play_random(possible_move)

# possible_move กับ all_enemy_possible_move เป็น format 'BA2': ['BA4'], 'BB1': ['BC3', 'BA3', 'BC3'] แบบนี้

def play_random(possible_move):
    while True:
        try:
            print("This is possible move: ", possible_move)

            random_piece = random.choice(list(possible_move.keys()))
            random_move = random.choice(possible_move[random_piece])

            print(f"This is random piece: {random_piece} and random move: {random_move}")

            return random_piece, random_move
        except:
            pass

        time.sleep(1)

def priority_move(possible_move, all_enemy_possible_move, current_board, check_if_king_in_check):
    while True:
        try:
            print("This is possible move:", possible_move)
            print("This is all enemies possible move:", all_enemy_possible_move)

            random_piece = random.choice(list(possible_move.keys()))
            owner = next((piece_info['Owner'] for piece_info in current_board if piece_info['Field'] == random_piece), None)

            most_priority, most_priority_move_field, mover_field = 0, None, None
            first_set, smart_random_movers = True, []

            for piece, fields in possible_move.items():
                for field in fields:
                    priority = calculate_priority(piece ,field, owner, current_board, all_enemy_possible_move)

                    if first_set or priority > most_priority or (priority == most_priority and random.choice([True, False])):
                        most_priority, most_priority_move_field, mover_field = priority, field, piece
                        smart_random_movers.append(mover_field) if priority >= 0 else []

            if most_priority == 0:
                random_piece, random_move = choose_random_move(possible_move, smart_random_movers, current_board, check_if_king_in_check)
                print(f"This is priority piece: {random_piece} and priority move: {random_move}")
                return random_piece, random_move
            else:
                print("This is priority piece:", mover_field, "and priority move:", most_priority_move_field)
                return mover_field, most_priority_move_field

        except Exception as e:
            print(f"An error occurred: {e}")
        time.sleep(1)


def calculate_priority(piece, field, owner, current_board, all_enemy_possible_move):
    priority = 0

    if not any(item['Field'] == field for item in current_board):
        priority = 0
    elif any(item['Field'] == field and item['Piece'] == 'Pawn' and item['Owner'] != owner for item in current_board):
        priority = 1
    elif any(item['Field'] == field and item['Piece'] == 'Bishop' and item['Owner'] != owner for item in current_board):
        priority = 2
    elif any(item['Field'] == field and item['Piece'] == 'Knight' and item['Owner'] != owner for item in current_board):
        priority = 3
    elif any(item['Field'] == field and item['Piece'] == 'Rook' and item['Owner'] != owner for item in current_board):
        priority = 5
    elif any(item['Field'] == field and item['Piece'] == 'Queen' and item['Owner'] != owner for item in current_board):
        priority = 50
    elif any(item['Field'] == field and item['Piece'] == 'King' and item['Owner'] != owner for item in current_board):
        priority = 100

    for item in all_enemy_possible_move.keys():
        if any(piece_info['Field'] == field and current_board[index]['Piece'] == 'Pawn' for index, piece_info in enumerate(current_board) if piece_info['Field'] == item):
            priority -= 1
        elif any(piece_info['Field'] == field and current_board[index]['Piece'] == 'ฺBishop' for index, piece_info in enumerate(current_board) if piece_info['Field'] == item):
            priority -= 2
        elif any(piece_info['Field'] == field and current_board[index]['Piece'] == 'Knight' for index, piece_info in enumerate(current_board) if piece_info['Field'] == item):
            priority -= 3
        elif any(piece_info['Field'] == field and current_board[index]['Piece'] == 'Rook' for index, piece_info in enumerate(current_board) if piece_info['Field'] == item):
            priority -= 4
        elif any(piece_info['Field'] == field and current_board[index]['Piece'] == 'Queen' for index, piece_info in enumerate(current_board) if piece_info['Field'] == item):
            priority -= 5

    #     for item_key, item_value in all_enemy_possible_move.items():
    #         enemy_bishop_fields = [enemy_piece['Field'] for enemy_piece, my_piece in current_board if my_piece['Field'] == field and enemy_piece['Field'] == item_value and my_piece['Piece'] == 'Bishop']
    #         enemy_knight_fields = [enemy_piece['Field'] for enemy_piece, my_piece in current_board if my_piece['Field'] == field and enemy_piece['Field'] == item_value and my_piece['Piece'] == 'Knight']
    #         enemy_rook_fields = [enemy_piece['Field'] for enemy_piece, my_piece in current_board if my_piece['Field'] == field and enemy_piece['Field'] == item_value and my_piece['Piece'] == 'Rook']
    #         enemy_queen_fields = [enemy_piece['Field'] for enemy_piece, my_piece in current_board if my_piece['Field'] == field and enemy_piece['Field'] == item_value and my_piece['Piece'] == 'Queen']
    #         enemy_pawn_fields = [enemy_piece['Field'] for enemy_piece, my_piece in current_board if my_piece['Field'] == field and enemy_piece['Field'] == item_value and my_piece['Piece'] == 'Pawn']

    #         if enemy_bishop_fields:
    #             if any(piece_info['Field'] == item_key and piece_info['Piece'] in ['Rook', 'Knight', 'Queen', 'Pawn'] for piece_info in current_board):
    #                 priority += 5
    #         elif enemy_knight_fields:
    #             if any(piece_info['Field'] == item_key and piece_info['Piece'] in ['Rook', 'Bishop', 'Queen', 'Pawn'] for piece_info in current_board):
    #                 priority += 10
    #         elif enemy_rook_fields:
    #             if any(piece_info['Field'] == item_key and piece_info['Piece'] in ['Bishop', 'Knight', 'Queen', 'Pawn'] for piece_info in current_board):
    #                 priority += 20
    #         elif enemy_queen_fields:
    #             if any(piece_info['Field'] == item_key and piece_info['Piece'] in ['Knight', 'Queen', 'Pawn'] for piece_info in current_board):
    #                 priority += 50
    #         elif enemy_pawn_fields:
    #             if any(piece_info['Field'] == item_key and piece_info['Piece'] in ['Pawn', 'Bishop'] for piece_info in current_board):
    #                 priority += 25
    #             elif any(piece_info['Field'] == item_key and piece_info['Piece'] in ['Knight', 'Rook'] for piece_info in current_board):
    #                 priority += 50
    #             elif any(piece_info['Field'] == item_key and piece_info['Piece'] == 'Queen' for piece_info in current_board):
    #                 priority += 100

    return priority


def choose_random_move(possible_move, smart_random_movers, current_board, check_if_king_in_check):
    random_piece, random_move = None, None

    if check_if_king_in_check:
        random_piece = random.choice(list(possible_move.keys()))
        random_move = random.choice(possible_move[random_piece])
    else:
        smart_random = True
        print('Insection of smart random')
        print(smart_random_movers)

        while smart_random:
            random_piece = random.choice(smart_random_movers)
            castles_priority = {'BC1', 'BG1', 'GC1', 'GG1', 'RC1', 'RG1'}
            filtered_piece_info = [piece_info for piece_info in possible_move[random_piece] if
                                   piece_info in castles_priority if
                                   any(piece.get('Piece') == 'King' and random_piece == piece.get('Field') for piece in
                                       current_board)]

            if filtered_piece_info:
                random_move = random.choice(filtered_piece_info)
                print("Case1")
                smart_random = False
            elif any(item['Field'] == random_piece and item['Piece'] == 'King' for item in current_board):
                if any(item['Field'] == random_piece and item['Piece'] == 'King' and check_if_king_in_check == False for
                       item in current_board):
                    # กรณีพบ "King" ใน 'Field' เดียวกัน ทำการเลือก random ใหม่
                    random_move = random.choice(possible_move[random_piece])
                    print("Cast2.1")
                    smart_random = False
                else:
                    random_move = random.choice(possible_move[random_piece])
                    print("Cast2.2")
                    smart_random = False
            else:
                random_move = random.choice(possible_move[random_piece])
                print("Cast3")
                smart_random = False

    return random_piece, random_move
