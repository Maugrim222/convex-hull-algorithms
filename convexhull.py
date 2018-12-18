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

    return hull_list[:-1]



def grahamscan(listPts):
    """Returns the convex hull vertices computed using the
         Graham-scan algorithm as a list of 'h' tuples
         [(u0,v0), (u1,v1), ...]  """

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

    # main section of the algorithm looks at pairs of points and appends points which are on the convex hull.
    # Pops the points which lie inside the hull and are thus not on the hull.
    for point in list_of_angles[3:]:
        # while the turn is not counter clockwise..
        while isCCW(stack[-2][0], stack[-1][0], point[0]) == False:
            stack.pop()

        stack.append(point)

    # returns a list of points which lie on the convex hull (omitting their associated angle)
    return [pt for pt, angle in stack]



def amethod(listPts):

    """Returns the convex hull vertices computed using
          monotone chaining"""

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

    # return list of points lying on the convex hull
    return convex_hull



def main():
    listPts = readDataPts('Set_B.dat', 30000)  # File name, numPts given as example only

    chull_list = grahamscan(listPts)
    chull_list2 = giftwrap(listPts)
    chull_list3 = amethod(listPts)

    check_list = [(500.0, 50.0), (520.0, 50.4), (539.9, 51.8), (559.8, 54.0), (579.6, 57.1), (599.2, 61.1), (618.6, 65.9), (637.8, 71.6), (656.7, 78.1), (675.2, 85.5), (693.5, 93.7), (711.3, 102.7), (728.8, 112.5), (745.8, 123.0), (762.3, 134.3), (778.3, 146.4), (793.7, 159.1), (808.6, 172.4), (822.8, 186.5), (836.4, 201.1), (849.4, 216.4), (861.6, 232.2), (873.2, 248.5), (884.0, 265.3), (894.0, 282.6), (903.3, 300.4), (911.8, 318.5), (919.4, 336.9), (926.2, 355.7), (932.2, 374.8), (937.4, 394.1), (941.6, 413.7), (945.0, 433.4), (947.6, 453.2), (949.2, 473.2), (949.9, 493.1), (949.8, 513.1), (948.8, 533.1), (946.9, 553.0), (944.1, 572.8), (940.4, 592.5), (935.9, 612.0), (930.4, 631.2), (924.2, 650.2), (917.1, 668.9), (909.2, 687.3), (900.5, 705.3), (890.9, 722.9), (880.7, 740.0), (869.6, 756.7), (857.8, 772.8), (845.4, 788.5), (832.2, 803.5), (818.4, 818.0), (804.0, 831.8), (788.9, 845.0), (773.3, 857.5), (757.1, 869.3), (740.5, 880.4), (723.3, 890.7), (705.8, 900.2), (687.8, 908.9), (669.4, 916.9), (650.7, 924.0), (631.8, 930.3), (612.5, 935.7), (593.0, 940.3), (573.4, 944.0), (553.6, 946.8), (533.7, 948.7), (513.7, 949.8), (493.7, 950.0), (473.7, 949.2), (453.8, 947.6), (434.0, 945.1), (414.2, 941.8), (394.7, 937.5), (375.4, 932.4), (356.3, 926.4), (337.5, 919.6), (319.0, 912.0), (300.9, 903.5), (283.1, 894.3), (265.8, 884.3), (249.0, 873.5), (232.6, 862.0), (216.8, 849.7), (201.6, 836.8), (186.9, 823.2), (172.8, 809.0), (159.4, 794.1), (146.7, 778.7), (134.7, 762.7), (123.4, 746.3), (112.8, 729.3), (103.0, 711.8), (94.0, 694.0), (85.7, 675.8), (78.3, 657.2), (71.8, 638.3), (66.1, 619.1), (61.2, 599.7), (57.2, 580.1), (54.1, 560.4), (51.8, 540.5), (50.5, 520.6), (50.0, 500.6), (50.4, 480.6), (51.7, 460.6), (53.9, 440.7), (57.0, 421.0), (60.9, 401.4), (65.8, 382.0), (71.4, 362.8), (77.9, 343.9), (85.3, 325.3), (93.5, 307.0), (102.4, 289.2), (112.2, 271.7), (122.7, 254.7), (134.0, 238.2), (146.0, 222.2), (158.7, 206.7), (172.1, 191.9), (186.1, 177.6), (200.7, 164.0), (215.9, 151.0), (231.7, 138.7), (248.0, 127.2), (264.9, 116.3), (282.1, 106.3), (299.8, 97.0), (317.9, 88.5), (336.4, 80.8), (355.2, 73.9), (374.3, 67.9), (393.6, 62.8), (413.1, 58.5), (432.8, 55.0), (452.7, 52.5), (472.6, 50.8)]

    if check_list == chull_list and chull_list2 == check_list and len(chull_list3) == len(check_list):
        print("All Correct :D")

    else:
        print("Incorrect :(")



if __name__ == "__main__":
    main()
