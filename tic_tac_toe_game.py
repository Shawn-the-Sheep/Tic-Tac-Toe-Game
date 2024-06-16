from random import randint

def fill_arr():

    arr = [[' ' for _ in range(3)] for _ in range(6)]

    lower_limit = -2
    index = -1

    for i in range(3):
        lower_limit += 3
        upper_limit = lower_limit + 3
        for j in range(lower_limit, upper_limit):
            index += 1
            arr[i][index] = j
        index = -1

    lower_limit = 0

    for i in range(3, 6):
        lower_limit += 1
        upper_limit = lower_limit + 7
        for j in range(lower_limit, upper_limit, 3):
            index += 1
            arr[i][index] = j
        index = -1

    arr.append([num for num in range(1, 10, 4)])
    arr.append([num for num in range(3, 8, 2)])

    return arr

win_arr = fill_arr()

class Board():

    def __init__(self):
        self.indices = [' ' for _ in range(9)]

    def display(self):

        print(self.indices[0] + '|' + self.indices[1] + '|' + self.indices[2])
        print('-----')
        print(self.indices[3] + '|' + self.indices[4] + '|' + self.indices[5])
        print('-----')
        print(self.indices[6] + '|' + self.indices[7] + '|' + self.indices[8])

    def alter_board(self, marker, index):
        self.indices[index] = marker

    def check_win(self, marker):

        counter = 0

        for element in win_arr:
            for num in element:
                if self.indices[num - 1] == marker:
                    counter += 1
            if counter == 3:
                return True
            else:
                counter = 0

        return False

    def check_tie(self):

        for i in range(len(self.indices)):
            if self.indices[i] == ' ':
                return False
        return True

class Player():

    marker = 'O'

    def __init__(self, name):
        self.name = name

    def choose_index(self, board_arr):

        '''This method shall prompt the player for a valid input'''

        valid_answer = False
        valid_range = range(1, 10)

        while not valid_answer:
            try:
                result = int(input("Enter a valid position (1-9): "))
                if result in valid_range:
                    if board_arr[result - 1] == ' ':
                        valid_answer = True
                    else:
                        print('This position is already taken')
                else:
                    print('This is not a valid position')
            except:
                print('This is not an integer')

        return result

    def __str__(self):
        return f'{self.name} has won'

class Computer():

    marker = 'X'

    def __init__(self, name):
        self.name = name

    def scan_board(self, board_arr):

        count_my_marker = 0
        count_opp_marker = 0
        count_space = 0
        potential_loss = None

        for element in win_arr:
            for num in element:
                if board_arr[num - 1] == self.marker:
                    count_my_marker += 1
                elif board_arr[num - 1] == ' ':
                    count_space += 1
                    position_space = num
                else:
                    count_opp_marker += 1

            if count_my_marker == 2 and count_space == 1:
                return position_space
            elif count_opp_marker == 2 and count_space == 1:
                potential_loss = position_space
                count_opp_marker = 0
                count_space = 0
            else:
                count_my_marker = 0
                count_opp_marker = 0
                count_space = 0

        return potential_loss

    def choose_index(self, board_arr):

        valid_answer = False

        while not valid_answer:

            answer = randint(1, 9)

            if board_arr[answer - 1] == ' ':
                valid_answer = True
            else:
                continue

        return answer

    def __str__(self):
        return f'{self.name} has won'

def ask_for_input():

    valid_answer = False

    valid_range = range(1,4)

    while not valid_answer:
        try:
            print('What would you like to do?')
            print('Enter 1 for playing a tic tac toe game against the Computer')
            print('Enter 2 for displaying current score against the Computer')
            print('Enter 3 for displaying a specific game that was previously played')

            user_input = int(input('Enter your input (1-3): '))

            if user_input in valid_range:
                valid_answer = True
            else:
                print('This integer is not in the valid range of (1-3). Try again')
        except:
            print('This is not an integer. Try again')
    
    return user_input
    
def board_on_text(board, some_txt_file):

    some_txt_file.write(board.indices[0] + '|' + board.indices[1] + '|' + board.indices[2] + '\n')
    some_txt_file.write('-----\n')
    some_txt_file.write(board.indices[3] + '|' + board.indices[4] + '|' + board.indices[5] + '\n')
    some_txt_file.write('-----\n')
    some_txt_file.write(board.indices[6] + '|' + board.indices[7] + '|' + board.indices[8] + (2 * '\n'))

def number_in_line(line):

    new_str = str() 
    
    for i in range(len(line)):

        if line[i].isdigit():

            for j in range(i, len(line)):

                if not line[j].isdigit():
                    break
                else:
                    new_str += line[j]
            break 
    
    return int(new_str)

def retrieve_game(some_txt_file):

    contents = some_txt_file.readlines()
    display_to_user = f'Enter the game number you would like to display to the console (1 - {number_in_line(contents[-2])}): '
    valid_game = False

    while not valid_game:

        try:
            game_to_retrieve = int(input(display_to_user))
            if game_to_retrieve >= 1 and game_to_retrieve <= number_in_line(contents[-2]):
                valid_game = True            
            else:                
                print('This input is not in the valid range of inputs. Try again')       
        except:
            print('This is not a valid integer. Try again')
    
    encountered_desired_lines = False 

    for line in contents: 

        if 'Game ' + str(game_to_retrieve + 1) in line:

            break 

        elif encountered_desired_lines:

            print(line)

        elif 'Game ' + str(game_to_retrieve) in line:

            encountered_desired_lines = True

def main_game():

    new_board = Board()
    new_player = Player('The user')
    new_comp = Computer('The computer')
    win = False
    n = randint(1,2)
    game_reference = open('game_reference.txt', 'a') 
    game_file = open('cps109_a1_output.txt', 'w') 

    with open('game_reference.txt', 'r') as game_ref2:

        contents = game_ref2.readlines()
        current_game = number_in_line(contents[-2]) + 1
    
    current_computer_score = number_in_line(contents[2])
    current_player_score = number_in_line(contents[3])     
    current_draws = number_in_line(contents[4])            

    game_reference.write(f'Game {current_game}' + (2 * '\n'))
        
    while not win:
        n += 1  
        if new_board.check_tie():
            if n % 2 != 0: 
                new_board.display()
                board_on_text(new_board, game_reference)
            print("It's a tie!")
            game_reference.write(f'Game {current_game} has ended in a draw\n\n')
            contents[4] = f'Draw : {current_draws + 1}\n'
            with open('game_reference.txt', 'w') as text_file:
                for line in contents:
                    text_file.write(line)
            game_file.write("It's a tie!")
            break
        elif n % 2 == 0:
            user_answer = new_player.choose_index(new_board.indices)
            new_board.alter_board(new_player.marker, user_answer - 1)
            win = new_board.check_win(new_player.marker)
            if win:
                new_board.display()
                board_on_text(new_board, game_reference)
                board_on_text(new_board, game_file)
                game_reference.write(f'The Player has won Game {current_game}\n\n')
                game_file.write('The Player has won')
                contents[3] = f'Player : {current_player_score + 1}\n'
                with open('game_reference.txt', 'w') as text_file:
                    for line in contents:
                        text_file.write(line)
                print(new_player)
        else:
            comp_answer = new_comp.scan_board(new_board.indices)
            try:
                new_board.alter_board(new_comp.marker, comp_answer - 1)
            except:
                comp_answer = new_comp.choose_index(new_board.indices)
                new_board.alter_board(new_comp.marker, comp_answer - 1)
            finally:
                win = new_board.check_win(new_comp.marker)
                new_board.display()
                board_on_text(new_board, game_reference)
                board_on_text(new_board, game_file)
            if win:
                game_reference.write(f'The Computer has won Game {current_game}\n\n')
                game_file.write('The Computer has won')
                contents[2] = f'Computer : {current_computer_score + 1}\n'
                with open('game_reference.txt', 'w') as text_file:
                    for line in contents:
                        text_file.write(line)
                print(new_comp)
    
    game_reference.close()

def main_func():
    
    user_desire = ask_for_input()
    if user_desire == 1:
        main_game()
    elif user_desire == 2:
        with open('game_reference.txt', 'r') as text_file:
            content = text_file.readlines()
        for i in range(2, 5):
            print(content[i])
    else:
        with open('game_reference.txt', 'r') as text_file:
            retrieve_game(text_file)

main_func()
