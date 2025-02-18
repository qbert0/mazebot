import subprocess

#Các tham số của mê cung
MAZESIZE = 20           #Giá trị >=6
SPEED = 10               #Giá trị 1 - 100
SHOWINFO = False           #Ẩn hiện thông tin
CENTER_TARGET = True      #Vị trí của đích True: ở trung tâm, False: ở góc dưới bên phải
ASIAN = False            #Chế độ tạo mê cung True: Phức tạp, False: Đơn giản
STEP = 43  # 18 step 54 
# 14 step 61 
# 8 step 106

class State:
    def __init__(self, x, y, direct, turn):
        self.x = x
        self.y = y
        self.DIRECT = direct
        self.TURN = turn
        self.hValue = 0
        self.gValue = 0
        self.fValue = self.gValue + self.hValue
        self.parent = None
        self.isGranpd = False
        self.listChild = []
        self.huong = []
        self.noleindex = []

    def setParent(self, node: 'State' ):
        self.parent = node
    
    def setGranpa(self , node : 'State') :
        self.granpa = node
    
    def setIsGrandPd(self) :
        self.isGranpd = True

    def setDriectGranpdToChild(self, direct, node :'State' ) :
        self.DIRECTGRANPA = direct
        self.child = node
        string : str = str(node.x) + "," + str(node.y)
        self.listChild.append(string)
        self.huong.append(direct)

    def setnole(self, node : 'State') :
        self.noleindex.append(node)
        
    def getfValue(self) :
        return self.hValue + self.gValue
    
startPos = State(0, 0, "DOWN", "AHEAD")
startPos.setGranpa(startPos)
pos = (MAZESIZE // 2 ) * STEP
goalPos = State(pos, pos, "a", "a")


openList = [startPos] # các node để duyệt tiếp theo nếu tồn tại
closeList = [startPos] # thể hiện vị trí hiện tại
stopControll = [False]
localList = [startPos] # các node được duyệt mới thêm vào tại vị trí nào đó
visited = []
propertie = {
    'goback' : False
}
#Chương trình chính điều khiển

def control(robot):
    # if stopControll[0] :
        # return
    if len(openList) == 0 :
        return
    currentState = openList[0]
    if len(openList) != 1 :
        for visit in openList :
            if currentState.getfValue() > visit.getfValue() :
                currentState = visit
            if currentState.getfValue() == visit.getfValue() and currentState.hValue > visit.hValue :
                currentState = visit
            print("(" + str(visit.x)+ "," + str(visit.y)+ "," + str(visit.getfValue()) +")" , end=' ')
    # print("lay node da duyet  (" + str(currentState.x)+ "," + str(currentState.y)+  ")")

    if robot.checkFirstGoal() : 
        return
    
    if currentState not in localList:
        backDef(robot, currentState, closeList[0])

    move(robot, currentState)
    openList.remove(currentState)
    closeList.clear()
    closeList.append(currentState)
    visited.append(currentState)
    listNeighbour = []
    if robot.look("AHEAD") == False :
        state = findNeightHead(currentState)
        listNeighbour.append(state)
    # if robot.look("BEHIND") == False :
    #     state = findNeightBEHIND(currentState)
    #     listNeighbour.append(state)
    if robot.look("LEFT") == False:
        state = findNeightLeft(currentState)
        listNeighbour.append(state)
    if robot.look("RIGHT") == False:
        state = findNeightRight(currentState)
        listNeighbour.append(state)
    
    # print("them vao laf  {",  end=' ')
    localList.clear()
    if len(listNeighbour) > 1 :
        currentState.setIsGrandPd()
    for neightState in listNeighbour :
        if neightState in visited :
            continue

        movemet = currentState.gValue + STEP
        # if neightState not in openList or movemet < neightState.gValue :
        neightState.gValue = movemet
        neightState.hValue = calculate(neightState, goalPos)

        neightState.setParent(currentState)
        if len(listNeighbour) == 1:
            neightState.setGranpa(currentState.granpa)
        else :
            neightState.setGranpa(currentState)

        currentState.setnole(neightState)
        openList.append(neightState)
        localList.append(neightState)
        # print("(" + str(neightState.x)+ "," + str(neightState.y)+ ")", end=' ')
    # print(" }")

def backDef (robot, node: State, state: State) :
    
    target = findGranpa(node,state)
    
    state = goBackTargetGranpa(robot, state, target)
    
    moveToNodeGranpa(robot, node.parent, state)

def moveToNodeGranpa (robot, target: State, state: State) :
    virTarget = target
    # if target == state :
    
    # print("kiem tra target   (" + str(target.x) + "," + str(target.y) + ")")
    # print("kiem tra state   (" + str(state.x) + "," + str(state.y) + ")")
    # print("kiem tra target   (" + str(target.x) + "," + str(target.y) + ")")
    # print("kiem tra state   (" + str(state.x) + "," + str(state.y) + ") ", end= '')
        
    # print(state.listChild, end= '')
    # print(state.huong)
    while target != state:

        while state != virTarget.granpa :
            virTarget = virTarget.granpa
        key: str = str(virTarget.x) + "," + str(virTarget.y)
        
        # print("kiem tra vir target   (" + str(virTarget.x) + "," + str(virTarget.y) + ")")
        # print("kiem tra state   (" + str(state.x) + "," + str(state.y) + ") ", end= '')
        # print(state.listChild, end= '')
        # print(state.huong)

        index = state.listChild.index(key)
        
        robot.turn(state.huong[index])
        # print("update robot after" + "(" + str(robot.x) + "," + str(robot.y) + ")")
        robot.go()
        # print("update robot befor" + "(" + str(robot.x) + "," + str(robot.y) + ")")

        for nole in state.noleindex :
            if nole.x == robot.x and nole.y == robot.y :
                state = nole
                # print("nole   " + "(" + str(nole.x) + "," + str(nole.y) + ")")
            else :
                continue
        # print("update state after" + "(" + str(state.x) + "," + str(state.y) + ")")
        # print(state.listChild, end= '')
        # print(state.huong)

        while state != virTarget :
            robot.turn(state.huong[0])
            robot.go()
            for nole in state.noleindex :
                if nole.x == robot.x and nole.y == robot.y :
                    state = nole
                    # print("nole   " + "(" + str(nole.x) + "," + str(nole.y) + ")")
                else :
                    continue
            # virTarget = target
        virTarget = target

def goBackTargetGranpa(robot, state : State, target : State) :
    turn = state.TURN
    robot.turn("BEHIND")
    childNode = state
    while state != target :
        turn = state.TURN
        robot.go()
        # print("adad" + "(" + str(robot.x) + "," + str(robot.y) + ")")
        state = state.parent
        # print("state node " + "(" + str(state.x) + "," + str(state.y) + ")")
        
        if turn == "LEFT" :
            robot.turn("RIGHT")
            state.setDriectGranpdToChild("LEFT", childNode)
        elif turn == "RIGHT" :
            robot.turn("LEFT")
            state.setDriectGranpdToChild("RIGHT", childNode)
        else :
            state.setDriectGranpdToChild("AHEAD", childNode)
            
        if state.isGranpd == True:
            childNode = state
            # print("child node " + "(" + str(childNode.x) + "," + str(childNode.y) + ")")

            # print("no da duojc check laf grand ba ma sao no mai van khong duoc len chuc the har ")
    robot.turn("BEHIND")
    return state

def findGranpa(source : State, target: State) :
    node1 = source
    node2 = target
    if node1 == node2 :
        return node1
    while True :
        node1 = source
        while True :
            if node1 == node2 :
                return node2
            if node1 == node1.granpa :
                break
            node1 = node1.granpa
        if node2 == node2.granpa :
            break
        node2 = node2.granpa
        
def move(robot, node: State) :
    if robot.x == node.x and robot.y == node.y :
        pass
    elif robot.x == node.x or robot.y == node.y :
        robot.turn(node.TURN)
        robot.go()
        print("move robot after" + "(" + str(robot.x) + "," + str(robot.y) + ")")
        print("move to node after" + "(" + str(node.x) + "," + str(node.y) + ")")
        
    else :
        pass

def findNeightHead(node : State) :
    if node.DIRECT == "DOWN":
        return State(node.x, node.y + STEP,"DOWN","AHEAD" )
    elif node.DIRECT == "RIGHT" :
        return State(node.x + STEP, node.y, "RIGHT","AHEAD")
    elif node.DIRECT == "LEFT" :
        return State(node.x - STEP, node.y, "LEFT","AHEAD")
    else :
        return State(node.x, node.y - STEP, "UP","AHEAD")

def findNeightBEHIND(node : State) :
    if node.DIRECT == "DOWN":
        return State(node.x, node.y - STEP,"UP","BEHIND" )
    elif node.DIRECT == "RIGHT" :
        return State(node.x - STEP, node.y, "LEFT","BEHIND")
    elif node.DIRECT == "LEFT" :
        return State(node.x + STEP, node.y, "RIGHT","BEHIND")
    else :
        return State(node.x, node.y + STEP, "DOWN","BEHIND")
    
def findNeightLeft(node : State) :
    if node.DIRECT == "DOWN":
        return State(node.x + STEP, node.y,"RIGHT","LEFT" )
    elif node.DIRECT == "RIGHT" :
        return State(node.x, node.y - STEP, "UP","LEFT")
    elif node.DIRECT == "LEFT" :
        return State(node.x , node.y + STEP, "DOWN","LEFT")
    else :
        return State(node.x - STEP, node.y, "LEFT","LEFT")   

def findNeightRight(node : State) :
    if node.DIRECT == "DOWN":
        return State(node.x - STEP, node.y,"LEFT","RIGHT" )
    elif node.DIRECT == "RIGHT" :
        return State(node.x, node.y + STEP, "DOWN","RIGHT")
    elif node.DIRECT == "LEFT" :
        return State(node.x , node.y - STEP, "UP","RIGHT")
    else :
        return State(node.x + STEP, node.y, "RIGHT","RIGHT")  

def calculate(node : State, end : State) :
    distX = abs(node.x - end.x)
    distY = abs(node.y - end.y)
    return (distX + distY) // STEP + 2

#Các câu lệnh hỗ trợ 
if __name__ == "__main__": 
    subprocess.run("..//main.exe")   


    
    
    
    
    
