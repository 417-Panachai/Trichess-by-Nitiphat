import asyncio
import time
import MESSAGE
import Trichess
import algorithm
import threading


async def wait_connection(trichess):
    while True:
        try:
            game_start = await trichess.receive_response()
            if game_start['Status'] != "Success":
                return
        except:
            pass

        time.sleep(1)

async def wait_my_turn(trichess):
    while True:
        try:
            await trichess.check_turn()
            turn_response = await trichess.receive_response()

            if turn_response['Status'] == "Success":
                if turn_response['YourTurn']:
                    return turn_response
        except:
            pass

        time.sleep(1)

async def check_if_game_end(trichess):
    while True:
        try:
            server_response = await trichess.receive_response()
            
            if server_response['Status'] == "GameEnd":
                return True
            else:
                return False
        except:
            return False

        time.sleep(1)

async def check_for_promotion(trichess):
    while True:
        try:
            server_response = await trichess.receive_response()
            
            if server_response['Status'] == "RequirePromotion":
                return True
            else:
                return False
        except:
            return False

        time.sleep(1)


async def check_if_king_in_check(trichess):
    while True:
        try:
            await trichess.check_king
            server_response = await trichess.receive_response()
            
            if server_response['Status'] == "Success":
                return server_response['KingInCheck']
            else:
                return False
        except:
            return False

        time.sleep(1)

async def get_my_piece(trichess):
    while True:
        await trichess.myPiece()
        my_piece_response = await trichess.receive_response()

        if my_piece_response['Status'] == 'Success':
            if 'Check board for piece' in my_piece_response['Message']:
                trichess.Piece = my_piece_response['Board']
                break
            
        time.sleep(1)

    print(f"This is samle of piece {trichess.Piece[:3]}")
    return None


async def get_all_possible_move(trichess):
    field = {}
    for current_place in trichess.Piece:
        current_place = current_place['Field']
        
        await trichess.move_able(current_place)
        piece_movable = await trichess.receive_response()

        # handle no movable
        if piece_movable['Status'] == 'Fail' and 'no movable' in piece_movable['Message']:
            continue

        if piece_movable['Status'] == 'Success':
            # print(f'Test on {current_place} success')
            if 'MovableFields' in piece_movable['Message']:
                for val in piece_movable['MovableFields']:
                    if current_place not in field:
                        field[current_place] = []
                    else:
                        field[current_place].append(val['Field'])
                    
    return field

async def get_all_enemy_possible_move(trichess):
    field = {}
    for current_place in trichess.Board:
        if current_place['Owner'] != trichess.Player:
            current_place = current_place['Field']

            await trichess.move_able(current_place)
            piece_movable = await trichess.receive_response()

            # handle no movable
            if piece_movable['Status'] == 'Fail' and 'no movable' in piece_movable['Message']:
                continue

            if piece_movable['Status'] == 'Success':
                # print(f'Test on {current_place} success')
                if 'MovableFields' in piece_movable['Message']:
                    for val in piece_movable['MovableFields']:
                        if current_place not in field:
                            field[current_place] = []
                        else:
                            field[current_place].append(val['Field'])
    return field

def check_pass(possible_move):
    return all(len(value) == 0 for value in possible_move.values())


async def main(url, type_algorithm):
    trichess = Trichess.Trichess(url)
    await trichess.connect()

    # loop wait to connect to game
    await wait_connection(trichess)
    
    # loop playgame
    while True:
        # loop wait my turn
        # check_promote = await receive_resp    onse(_trichess)
        

        promotion_response = await check_for_promotion(trichess)
        if promotion_response == False:
            turn_response = await wait_my_turn(trichess)
            if turn_response:
                print(MESSAGE.MY_TURN)
                trichess.Board = turn_response['Board']
                print('my baord:' + str(trichess.Board))

                await get_my_piece(trichess)
                possible_move = await get_all_possible_move(trichess)

                if (type_algorithm == 2):
                    all_enemy_possible_move = await get_all_enemy_possible_move(trichess)
                    checking_if_king_in_check = await check_if_king_in_check(trichess)

                # print("This is possible move: ", possible_move)

                # TODO: check if all possible move is None
                if check_pass(possible_move):
                    await trichess.pass_turn()
                    pass_response = await trichess.receive_response()
                    if pass_response['Status'] == 'Success':
                        print(MESSAGE.PASS)
                    continue
        
                print("This is possible move: ", possible_move)

                '''
                TODO: call algorithm and return piece and move
                '''
                if type_algorithm == 2:
                    curr_position, move_to = algorithm.algorithm_provider(possible_move, all_enemy_possible_move, trichess.Board, checking_if_king_in_check, type_algorithm)
                else:
                    _all_enemy_possible_move = None
                    _checking_if_king_in_check = None
                    curr_position, move_to = algorithm.algorithm_provider(possible_move, _all_enemy_possible_move, trichess.Board, _checking_if_king_in_check, type_algorithm)
            
                await trichess.send_move(curr_position, move_to)
                move_response = await trichess.receive_response()
                if move_response['Status'] == 'Success':
                    print(MESSAGE.MOVE_SUCCESS)
        else:
            trichess.promote()
        
        time.sleep(1)

if __name__ == '__main__':
    # URL = 'ws://10.7.244.205:8181/game'
    user_ip = input("Enter the IP address: ")
    URL = "ws://" + user_ip +":8181/game"
    n_player = int(input("Enter number of player [int]: "))
    # URL = input("Enter URL: ")
    
    for i in range(n_player):
        print(f"Select algorithm for player {i+1}")
        print(MESSAGE.ALGORITHM)
        algo = int(input("Enter algorithm [int]: "))
        
        threading.Thread(target=asyncio.run, args=(main(URL, algo),)).start()
        print("Thread: ", i, " started")

        time.sleep(0.5)