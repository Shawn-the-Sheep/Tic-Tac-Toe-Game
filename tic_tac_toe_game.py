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

def main_game():

    new_board = Board()
    new_player = Player('The user')
    new_comp = Computer('The computer')
    win = False
    n = randint(1,2)

    while not win:
        n += 1
        if new_board.check_tie():
            if n % 2 != 0:
                new_board.display()
            print("It's a tie!")
            break
        elif n % 2 == 0:
            user_answer = new_player.choose_index(new_board.indices)
            new_board.alter_board(new_player.marker, user_answer - 1)
            win = new_board.check_win(new_player.marker)
            if win:
                new_board.display()
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
            if win:
                print(new_comp)

main_game()