from timeit import default_timer as timer

noOfEle = myResult = None
node_Expand = 0


class Puzzel:
    def __init__(self, puzzel):
        self.puzzel = list(puzzel)
        self.nextNode = None

    def creatList(self):
        global noOfEle, myResult
        p = self.puzzel
        k = 0
        puzzel = [[] for i in range(noOfEle)]
        result = [[] for i in range(noOfEle)]
        for i in range(noOfEle):
            for j in range(noOfEle):
                puzzel[i].append(int(p[k]))
                result[i].append(k)
                k = k + 1
        self.puzzel = puzzel
        myResult = result


class Node:
    def __init__(self, puzzel):
        self.puzzel = puzzel
        self.nextNode = None
        self.path_to_goal = []
        self.cost_of_path = 0
        self.heuristic_distance = 0


class Heap:
    def new(self, initialState):
        n = Node(initialState)
        self.rear = self.front = n
        return self.rear

    def insert(self, state):
        state.heuristic_distance = calManhatonDistance(state.puzzel)

        if self.front == None:
            self.front = self.rear = state

        elif self.front.nextNode is None:
            if (state.cost_of_path + state.heuristic_distance) < (
                        self.front.cost_of_path + self.front.heuristic_distance):
                state.nextNode = self.front
                self.front = state
            else:
                self.rear.nextNode = state
                self.rear = state
        else:
            n = previous = self.front
            while n != None:
                if (n.cost_of_path + n.heuristic_distance) > (state.cost_of_path + state.heuristic_distance):
                    if n == self.front:
                        state.nextNode = self.front
                        self.front = state
                    else:
                        state.nextNode = n
                        previous.nextNode = state
                        break
                previous = n
                n = n.nextNode
            else:
                self.rear.nextNode = state
                self.rear = state

    def deleteMin(self):
        ref = self.front
        if (ref == None):
            return None
        if (self.front == self.rear):
            self.front = self.rear = None
        else:
            self.front = self.front.nextNode
        return ref

    def decreaseKey(self, state):
        global noOfEle
        location = n = previous = self.front
        while n != None:
            loop = True
            i = 0
            while loop and i < noOfEle:
                j = 0
                while loop and j < noOfEle:
                    if (n.puzzel[i][j] != state.puzzel[i][j]):
                        loop = False
                    j += 1
                i += 1
            if loop:
                location = n
                if location.cost_of_path <= state.cost_of_path:
                    return
                else:
                    if location == self.front:
                        self.front.cost_of_path = state.cost_of_path
                        return
                    elif location == self.rear:
                        self.rear.cost_of_path = state.cost_of_path
                        return
                    else:
                        previous.nextNode = n.nextNode
                        self.insert(state)
                        return
                break
            previous = n
            n = n.nextNode

    def check(self, puzzel):
        global noOfEle
        n = self.front
        ref = False
        while n != None:
            loop = True
            i = 0
            while loop and i < noOfEle:
                j = 0
                while loop and j < noOfEle:
                    if (n.puzzel[i][j] != puzzel[i][j]):
                        loop = False
                    j += 1
                i += 1
            if loop:
                ref = True
                break;
            n = n.nextNode
        return ref

    def isEmpty(self):
        if self.front == None and self.rear == None:
            return True
        return False


class Explore:
    start = None

    def addExplore(self, ref):
        global node_Expand
        node_Expand += 1
        if self.start == None:
            self.start = Node(ref.puzzel)
            return
        else:
            n = Node(ref.puzzel)
            n.nextNode = self.start
            self.start = n
            return

    def check(self, puzzel):
        if (len(puzzel[1]) <= 0):
            return False
        global noOfEle
        n = self.start
        ref = False
        while n != None:
            loop = True
            i = 0
            while loop and i < noOfEle:
                j = 0
                while loop and j < noOfEle:
                    if (puzzel[i][j] != n.puzzel[i][j]):
                        loop = False
                    j += 1
                i += 1
            if (loop):
                ref = True
                break;
            n = n.nextNode
        return ref


def calManhatonDistance(puzzel):
    global myResult
    manhatonDis = 0
    for i in range(9):
        if i != 0:
            locationResullt = getLocation(myResult, i)
            locationPuzzel = getLocation(puzzel, i)
            manhatonDis += abs((abs(locationPuzzel[0])) - (abs(locationResullt[0]))) + abs(
                (abs(locationPuzzel[1]) - abs(locationResullt[1])))
    return manhatonDis


def goalTest(state):
    global noOfEle
    if myResult == None:
        return False
    for i in range(noOfEle):
        for j in range(noOfEle):
            if state.puzzel[i][j] != myResult[i][j]:
                return False
    print(state.path_to_goal)
    return True


def getLocation(puzzel, item):
    global noOfEle
    for i in range(noOfEle):
        for j in range(noOfEle):
            if puzzel[i][j] == item:
                return (i, j)
    return None


def getPuzzel(puzzel):
    global noOfEle
    p = [[] for i in range(noOfEle)]
    for i in range(noOfEle):
        p[i] = puzzel[i].copy()
    return p


def getNeighbor(state):
    location = getLocation(state.puzzel, 0)
    global noOfEle
    neighbor = []
    nextNeighbor = [[] for i in range(noOfEle)]
    locationSet = ((location[0] - 1, location[1]), (location[0] + 1, location[1]), (location[0], location[1] - 1),
                   (location[0], location[1] + 1))
    path = ['Up', 'Down', 'Left', 'Right']
    for i in range(4):
        nextNeighbor = getPuzzel(state.puzzel)
        if locationSet[i][0] in range(noOfEle) and locationSet[i][1] in range(noOfEle):
            nextNeighbor[locationSet[i][0]][locationSet[i][1]], nextNeighbor[location[0]][location[1]] = \
                nextNeighbor[location[0]][location[1]], nextNeighbor[locationSet[i][0]][locationSet[i][1]]
        else:
            continue
        temp = Node(nextNeighbor)
        temp.path_to_goal.extend(state.path_to_goal)
        temp.path_to_goal.append(path[i])
        temp.cost_of_path = setCost(temp)
        neighbor.append(temp)
    return neighbor


def setCost(temp):
    return (len(temp.path_to_goal))


def setSearchDepth(temp):
    search_Depth = len(temp.path_to_goal)

def ast(initialState):
    frontier = Heap()
    frontier.new(initialState)
    explore = Explore()
    while not frontier.isEmpty():
        state = frontier.deleteMin()
        explore.addExplore(state)
        if goalTest(state):
            return True, state
        puzzel = getNeighbor(state)
        for neighbor in puzzel:
            if not frontier.check(neighbor.puzzel):
                if not explore.check(neighbor.puzzel):
                    frontier.insert(neighbor)
            elif frontier.check(neighbor.puzzel):
                setSearchDepth(neighbor)
                frontier.decreaseKey(neighbor)
    return False, None


def control(list):
    global noOfEle
    start = timer()
    obj = Puzzel(list)
    noOfEle = int(len(obj.puzzel) ** .5)
    obj.creatList()
    result,state = ast(obj.puzzel)
    print("result {}".format(result))
    end = timer()
    print(end - start)
    return state.path_to_goal


