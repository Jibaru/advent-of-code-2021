'''
--- Day 5: Hydrothermal Venture ---
You come across a field of hydrothermal vents on the ocean floor! These vents constantly produce large, opaque clouds, so it would be best to avoid them if possible.

They tend to form in lines; the submarine helpfully produces a list of nearby lines of vents (your puzzle input) for you to review. For example:

0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2
Each line of vents is given as a line segment in the format x1,y1 -> x2,y2 where x1,y1 are the coordinates of one end the line segment and x2,y2 are the coordinates of the other end. These line segments include the points at both ends. In other words:

An entry like 1,1 -> 1,3 covers points 1,1, 1,2, and 1,3.
An entry like 9,7 -> 7,7 covers points 9,7, 8,7, and 7,7.
For now, only consider horizontal and vertical lines: lines where either x1 = x2 or y1 = y2.

So, the horizontal and vertical lines from the above list would produce the following diagram:

.......1..
..1....1..
..1....1..
.......1..
.112111211
..........
..........
..........
..........
222111....
In this diagram, the top left corner is 0,0 and the bottom right corner is 9,9. Each position is shown as the number of lines which cover that point or . if no line covers that point. The top-left pair of 1s, for example, comes from 2,2 -> 2,1; the very bottom row is formed by the overlapping lines 0,9 -> 5,9 and 0,9 -> 2,9.

To avoid the most dangerous areas, you need to determine the number of points where at least two lines overlap. In the above example, this is anywhere in the diagram with a 2 or larger - a total of 5 points.

Consider only horizontal and vertical lines. At how many points do at least two lines overlap?

Your puzzle answer was 7674.
'''

#data = open('day-5-input.test.txt', 'r').read()
data = open('day-5-input.txt', 'r').read()

def build_point(point):
    return { 'x': int(point.split(',')[0]),
     'y': int(point.split(',')[1])}

def build_line(row):
    return list(map(build_point, row.split(' -> ')))

lines = list(map(build_line, data.split('\n')))

def max_diagram_point(lines):
    max_x = -1
    max_y = -1

    for line in lines:
        if line[0]['x'] > max_x:
            max_x = line[0]['x']
        if line[1]['x'] > max_x:
            max_x = line[1]['x']
        if line[0]['y'] > max_y:
            max_y = line[0]['y']
        if line[1]['y'] > max_y:
            max_y = line[1]['y']

    return { 'x': max_x, 'y': max_y }


def solve01():
    def count_in_lines(x, y):
        def is_vh(line):
            return (line[0]['x'] == line[1]['x'] or line[0]['y'] == line[1]['y'])

        def is_in_line(line):
            max_x = max(line[0]['x'], line[1]['x'])
            min_x = min(line[0]['x'], line[1]['x'])
            max_y = max(line[0]['y'], line[1]['y'])
            min_y = min(line[0]['y'], line[1]['y'])

            return (max_x >= x >= min_x) and (max_y >= y >= min_y)

        counter = 0
        for line in lines:
            if is_vh(line) and is_in_line(line):
                counter += 1

        return counter

    max_point = max_diagram_point(lines)
    overlapped = 0
    for i in range(0, max_point['x'] + 1):
        for j in range(0, max_point['y'] + 1):

            count = count_in_lines(j, i)
            if count >= 2:
                overlapped += 1

    return overlapped

'''
The first half of this puzzle is complete! It provides one gold star: *

--- Part Two ---
Unfortunately, considering only horizontal and vertical lines doesn't give you the full picture; you need to also consider diagonal lines.

Because of the limits of the hydrothermal vent mapping system, the lines in your list will only ever be horizontal, vertical, or a diagonal line at exactly 45 degrees. In other words:

An entry like 1,1 -> 3,3 covers points 1,1, 2,2, and 3,3.
An entry like 9,7 -> 7,9 covers points 9,7, 8,8, and 7,9.
Considering all lines from the above example would now produce the following diagram:

1.1....11.
.111...2..
..2.1.111.
...1.2.2..
.112313211
...1.2....
..1...1...
.1.....1..
1.......1.
222111....
You still need to determine the number of points where at least two lines overlap. In the above example, this is still anywhere in the diagram with a 2 or larger - now a total of 12 points.

Consider all of the lines. At how many points do at least two lines overlap?

Your puzzle answer was 20898.
'''

def solve02():
    def count_in_lines(x, y):

        def is_in_line(line):
            max_x = max(line[0]['x'], line[1]['x'])
            min_x = min(line[0]['x'], line[1]['x'])
            max_y = max(line[0]['y'], line[1]['y'])
            min_y = min(line[0]['y'], line[1]['y'])

            if max_x == min_x:
                return (max_x == x) and (max_y >= y >= min_y)

            if max_y == min_y:
                return (max_y == y) and (max_x >= x >= min_x)
            
            in_segment = (max_x >= x >= min_x) and (max_y >= y >= min_y)

            if not in_segment:
                return False
            
            # In left-top to right-bottom diagonal
            if (line[0]['x'] < line[1]['x'] and line[0]['y'] > line[1]['y']) or (line[1]['x'] < line[0]['x'] and line[1]['y'] > line[0]['y']):
                return max_x - x == y - min_y

            # In left-bottom to right-top diagonal
            return max_x - x == max_y - y

        counter = 0
        for line in lines:
            if is_in_line(line):
                counter += 1

        return counter

    max_point = max_diagram_point(lines)
    overlapped = 0
    for i in range(0, max_point['x'] + 1):
        for j in range(0, max_point['y'] + 1):

            count = count_in_lines(j, i)
            if count >= 2:
                overlapped += 1

    return overlapped

print(solve01())
print(solve02())

