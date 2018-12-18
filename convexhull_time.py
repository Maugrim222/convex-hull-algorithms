import time

"""
   Convex Hull Assignment: COSC262 (2017)
   Student Name: Tomas Burai
   Usercode: tbu43
"""



def isCCW(ptA, ptB, ptC):
    """Takes in 3 consecutive points and determines if they make a counter clockwise turn"""

    interim_value = ((ptB[0] - ptA[0]) * (ptC[1] - ptA[1])) - ((ptB[1] - ptA[1]) * (ptC[0] - ptA[0]))

    # if interim_value if greater than 0, the line makes a counter-clockwise turn
    return interim_value > 0



def theta(pointA, pointB):
    """Calculates an approximation of the angle between the line (pointA, pointB) and a horizontal line passing
    through point A."""

    dx = pointB[0] - pointA[0]
    dy = pointB[1] - pointA[1]

    if abs(dx) < 1.e-6 and abs(dy) < 1.e-6:
        t = 0

    else:
        t = dy/(abs(dx) + abs(dy))

    if dx < 0:
        t = 2 - t

    elif dy < 0:
        t = 4 + t

    return t * 90



def readDataPts(filename, N):
    """Reads the first N lines of data from the input file
          and returns a list of N tuples
          [(x0,y0), (x1, y1), ...]"""

    list_of_points = []

    read_file = open(filename, "r")

    for line in read_file:

        point = ((line.strip()).split(" "))
        coord_tuple = []

        for coord_value in point:
            coord_value = float(coord_value)
            coord_tuple.append(coord_value)

        list_of_points.append(tuple(coord_tuple))

    # returns the list of point coordinates up to the value N specified

    return list_of_points[:N]



def giftwrap(listPts):
    """Returns the convex hull vertices computed using the
          giftwrap algorithm as a list of 'h' tuples
          [(u0,v0), (u1,v1), ...]   """

    # records the start time
    start_time = time.time()

    # finds the starting vertex - the point with the minimum y coord and in case of multiple points, chooses point
    # with highest x coord.
    starting_vertex = min(listPts, key=lambda p: (p[1], -p[0]))

    index = 0
    last_angle = 0

    # assigns the index of the starting vertex to k
    k = listPts.index(starting_vertex)
    listPts.append(listPts[k])

    # creates the list of vertices on the convex hull and inserts the starting vertex
    # (which is automatically on the hull)
    hull_list = []
    hull_list.append(starting_vertex)

    while k != len(listPts) - 1:
        listPts[index], listPts[k] = listPts[k], listPts[index]

        # sets the value of minAngle to an angle higher than the highest possible angle to make sure the next angle is
        # smaller that this first minAngle
        minAngle = 361

        # j is the min y vertex
        for j in range(index + 1, len(listPts)):
            angle = theta(listPts[index], listPts[j])

            # if the angle returned is 0, it means a whole 360 degree turn was executed and so the
            # value of angle is changed to 360 to reflect this
            if angle == 0:
                angle = 360

            # compares whether the angle is smaller than the minimum angle and larger than the previous angle we found.
            if angle < minAngle and angle > last_angle and listPts[j] != listPts[index]:
                minAngle = angle
                k = j

        hull_list.append(listPts[k])

        # increment the index and sets the value of the last angle to the min angle found in the last iteration.
        index += 1
        last_angle = minAngle

    # prints time taken to run algorithm
    print(time.time() - start_time)

    return hull_list[:-1]



def grahamscan(listPts):
    """Returns the convex hull vertices computed using the
         Graham-scan algorithm as a list of 'h' tuples
         [(u0,v0), (u1,v1), ...]  """

    # records the start time
    start_time = time.time()

    # finds the starting vertex - the point with the minimum y coord and in case of multiple points,
    # chooses point with highest x coord.
    starting_vertex = min(listPts, key=lambda p: (p[1], -p[0]))

    # initialise the list to which the vertices and associated angles are appended to as a (vertex, angle) tuple.
    list_of_angles = []

    # calculates the angle between each point in the list and the starting vertex and appends the result to the list.
    for vertex in listPts:
        angle = theta(starting_vertex, vertex)
        list_of_angles.append((vertex, angle))

    # sorts the list by the angles (in the index 1 in the tuple and in case of same angle, sorts by the y coord)
    list_of_angles.sort(key=lambda p: (p[1], p[0][1]))

    stack = [list_of_angles[0], list_of_angles[1], list_of_angles[2]]

    for point in list_of_angles[3:]:
        # while the turn is not counter clockwise..
        while isCCW(stack[-2][0], stack[-1][0], point[0]) == False:
            stack.pop()

        stack.append(point)

    # prints the time taken to run algorithm
    print("--- %s seconds ---" % (time.time() - start_time))

    # returns a list of points which lie on the convex hull (omitting their associated angle)
    return [pt for pt, angle in stack]



def amethod(listPts):

    """Returns the convex hull vertices computed using
          monotone chaining"""

    # records the start time
    start_time = time.time()

    # sorts the list and removes duplicate points
    listPts = sorted(set(listPts))

    # initialises the two lists to contain the upper and lower hulls respectively
    upper_hull = []
    lower_hull = []

    # constructs the upper hull by reversing the list and therefore starting at the highest x coord and stopping when
    # reached the lowest x coord.
    for point in reversed(listPts):
        while len(upper_hull) >= 2 and not isCCW(upper_hull[-2], upper_hull[-1], point):
            upper_hull.pop()
        upper_hull.append(point)

    # construct the lower hull by starting at the left most x coord and stopping when reached the rightmost x coord
    for point in listPts:
        while len(lower_hull) >= 2 and not isCCW(lower_hull[-2], lower_hull[-1], point):
            lower_hull.pop()
        lower_hull.append(point)

    # combines the upper and lower hull lists to create the complete convex hull
    convex_hull = upper_hull[:-1] + lower_hull[:-1]

    # prints the time taken to run algorithm
    print("--- %s seconds ---" % (time.time() - start_time))

    # return list of points lying on the convex hull
    return convex_hull



def main():
    listPts = readDataPts('Set_A.dat', 30000)  # File name, numPts given as example only

    # prime_list = grahamscan(listPts)
    # prime_list2 = giftwrap(listPts)
    # prime_list3 = amethod(listPts)
    #
    # check_list = [(526.9, 400.5), (599.4, 400.8), (599.0, 514.4), (598.8, 562.1), (594.5, 583.9), (583.0, 598.8), (554.8, 599.4), (411.2, 599.2), (401.6, 580.5), (400.7, 497.3), (400.6, 475.0), (401.0, 412.3), (401.2, 408.3), (415.6, 404.9), (438.5, 400.5)]
    #
    #
    # if check_list == prime_list and prime_list2 == check_list and len(prime_list3) == len(check_list):
    #     print("Yes!!! ")
    #
    # else:
    #     print("sad :( ")



if __name__ == "__main__":
    main()
