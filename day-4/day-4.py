'''
--- Day 4: Giant Squid ---
You're already almost 1.5km (almost a mile) below the surface of the ocean, already so deep that you can't see any sunlight. What you can see, however, is a giant squid that has attached itself to the outside of your submarine.

Maybe it wants to play bingo?

Bingo is played on a set of boards each consisting of a 5x5 grid of numbers. Numbers are chosen at random, and the chosen number is marked on all boards on which it appears. (Numbers may not appear on all boards.) If all numbers in any row or any column of a board are marked, that board wins. (Diagonals don't count.)

The submarine has a bingo subsystem to help passengers (currently, you and the giant squid) pass the time. It automatically generates a random order in which to draw numbers and a random set of boards (your puzzle input). For example:

7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
After the first five numbers are drawn (7, 4, 9, 5, and 11), there are no winners, but the boards are marked as follows (shown here adjacent to each other to save space):

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
After the next six numbers are drawn (17, 23, 2, 0, 14, and 21), there are still no winners:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
Finally, 24 is drawn:

22 13 17 11  0         3 15  0  2 22        14 21 17 24  4
 8  2 23  4 24         9 18 13 17  5        10 16 15  9 19
21  9 14 16  7        19  8  7 25 23        18  8 23 26 20
 6 10  3 18  5        20 11 10 24  4        22 11 13  6  5
 1 12 20 15 19        14 21 16 12  6         2  0 12  3  7
At this point, the third board wins because it has at least one complete row or column of marked numbers (in this case, the entire top row is marked: 14 21 17 24 4).

The score of the winning board can now be calculated. Start by finding the sum of all unmarked numbers on that board; in this case, the sum is 188. Then, multiply that sum by the number that was just called when the board won, 24, to get the final score, 188 * 24 = 4512.

To guarantee victory against the giant squid, figure out which board will win first. What will your final score be if you choose that board?

Your puzzle answer was 32844.
'''

from functools import reduce

# data = open('day-4-input.test.txt', 'r').read()
data = open('day-4-input.txt', 'r').read()

items = data.replace('\n\n', '*').split('*')
bingo_numbers = list(map(int, items[0].split(',')))
del items[0]


def map_board(boardstr):
    rowstr = boardstr.split('\n')
    return list(map(lambda row: list(map(int, filter(lambda i: i != '', row.split(' ')))), rowstr))


def build_bingo_board(board):
    def build_bingo_items(row):
        return list(map(lambda i: {'number': i, 'marked': False}, row))
    return list(map(build_bingo_items, board))


def build_bingo_boards():
    return list(map(build_bingo_board, boards))


boards = list(map(map_board, items))
bingo_boards = build_bingo_boards()


def mark_board(number, bingo_board):
    for row in bingo_board:
        for element in row:
            if element['number'] == number:
                element['marked'] = True
                return False


def check_win(board):
    rows = {}
    columns = {}

    for i, row in enumerate(board):
        for j, element in enumerate(row):
            if element['marked']:
                if i not in rows:
                    rows[i] = 1
                else:
                    rows[i] += 1

                if j not in columns:
                    columns[j] = 1
                else:
                    columns[j] += 1

    for i in rows:
        if rows[i] == 5:
            return True

    for j in columns:
        if columns[j] == 5:
            return True

    return False


def get_unmarked_numbers(board):
    unmarked_numbers = []
    for row in board:
        for element in row:
            if not element['marked']:
                unmarked_numbers.append(element['number'])

    return unmarked_numbers


def solve01():
    for number in bingo_numbers:
        for board in bingo_boards:
            mark_board(number, board)
            if check_win(board):
                unmarked_numbers = get_unmarked_numbers(board)
                sum = reduce(lambda a, b: a + b, unmarked_numbers)
                return number * sum


'''
--- Part Two ---
On the other hand, it might be wise to try a different strategy: let the giant squid win.

You aren't sure how many bingo boards a giant squid could play at once, so rather than waste time counting its arms, the safe thing to do is to figure out which board will win last and choose that one. That way, no matter which boards it picks, it will win for sure.

In the above example, the second board is the last to win, which happens after 13 is eventually called and its middle column is completely marked. If you were to keep playing until this point, the second board would have a sum of unmarked numbers equal to 148 for a final score of 148 * 13 = 1924.

Figure out which board will win last. Once it wins, what would its final score be?

Your puzzle answer was 4920.
'''


def solve02():
    total_boards = len(bingo_boards)
    winning_boards = []
    for number in bingo_numbers:
        for board in bingo_boards:
            mark_board(number, board)
            if board not in winning_boards and check_win(board):
                winning_boards.append(board)

            if len(winning_boards) == total_boards:
                unmarked_numbers = get_unmarked_numbers(board)
                sum = reduce(lambda a, b: a + b, unmarked_numbers)
                return number * sum


print(solve01())
print(solve02())
