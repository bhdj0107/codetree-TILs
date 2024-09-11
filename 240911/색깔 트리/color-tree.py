Q = int(input())
querys = [list(map(int, input().split())) for _ in range(Q)]

class ColorTree:
    def __init__(self, color, depth):
        self.color = color
        self.parent = None
        self.max_depth = depth
        self.children = []

    def addNode(self, child):
        if self.isNodeAddable(1):
            child.parent = self
            self.children.append(child)
            return True
        else:
            return False    
    
    def isNodeAddable(self, childDepth):
        if self.color == None: return True
        if childDepth < self.max_depth:
            return self.parent.isNodeAddable(childDepth + 1)
        else:
            return False
    
    def changeColor(self, color):
        self.color = color
        for child in self.children:
            child.changeColor(color)
            
    def getMyColor(self):
        return self.color
    
    def getMyColors(self):
        if self.color == None: return set()
        totalColor = set()
        totalColor.add(self.color)
        for child in self.children:
            totalColor.update(child.getMyColors())
        return totalColor
    
root = ColorTree(None, 100000)
nodeMemory = {
    -1: root,
}

for q in querys:
    # 노드 추가
    if q[0] == 100:
        m_id, p_id, color, max_depth = q[1:]
        newNode = ColorTree(color, max_depth)
        if nodeMemory[p_id].addNode(newNode): 
            nodeMemory[m_id] = newNode
    
    # 색상 변경
    elif q[0] == 200:
        m_id, color = q[1:]
        nodeMemory[m_id].changeColor(color)
    
    # 색상 조회
    elif q[0] == 300:
        m_id = q[1]
        print(nodeMemory[m_id].getMyColor())
    
    # 점수 조회
    elif q[0] == 400:
        eachScore = list(map(lambda x : len(x.getMyColors()) ** 2, nodeMemory.values()))
        print(sum(eachScore))