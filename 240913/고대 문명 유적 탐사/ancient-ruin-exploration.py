# 240913 1327 start
from collections import deque
K, M = map(int, input().split())
field = [list(map(int, input().split())) for _ in range(5)]
walls = deque(list(map(int, input().split())))
delta = ((0, 1), (1, 0), (-1, 0), (0, -1))
ans = []
class RotationableField:
    def __init__(self, field):
        self.field = field
        self.maskLeftTop = (0, 0)
        self.rotateDegree = 0
        self.rotateMask = (

            # 90 degree
            "(2 - dx, dy)",

            # 180 degree
            "(2 - dy, 2 - dx)",

            # 270 degree
            "(dx, -dy + 2)",
        )

    def rotatedField(self):
        field = [[self.getitem((i, j)) for j in range(5)] for i in range(5)]
        return field

    def setLeftTop(self, idx):
        self.maskLeftTop = idx

    def setRotateDegree(self, value):
        self.rotateDegree = value

    def getitem(self, idx):
        y, x = idx
        if self.isPosInMask(idx):
            dy, dx = y - self.maskLeftTop[0], x - self.maskLeftTop[1]
            dy, dx = eval(self.rotateMask[self.rotateDegree])
            return self.field[self.maskLeftTop[0] + dy][self.maskLeftTop[1] + dx]
        return self.field[y][x]

    def setitem(self, idx, item):
        y, x = idx
        if self.isPosInMask(idx):
            dy, dx = y - self.maskLeftTop[0], x - self.maskLeftTop[1]
            dy, dx = eval(self.rotateMask[self.rotateDegree])
            self.field[self.maskLeftTop[0] + dy][self.maskLeftTop[1] + dx] = item
        else: self.field[y][x] = item

    def isPosInMask(self, idx):
        y, x = idx
        if y >= self.maskLeftTop[0] and y < self.maskLeftTop[0] + 3:
            if x >= self.maskLeftTop[1] and x < self.maskLeftTop[1] + 3:
                return True
        return False

def getCollectableCntandBlockPoses(rtField: RotationableField):
    visited = [[False for _ in range(5)] for _ in range(5)]
    blockPoses = []
    for i in range(5):
        for j in range(5):
            if visited[i][j]: continue
            else:
                q = deque()
                q.append((i, j))
                blockNum = rtField.getitem((i, j))
                blockSize = 0
                tmpBlockPoses = []
                while q:
                    now = q.popleft()
                    if visited[now[0]][now[1]]: continue
                    else:
                        visited[now[0]][now[1]] = True
                        blockSize += 1
                        tmpBlockPoses.append(now)
                        for d in range(4):
                            ny, nx = now[0] + delta[d][0], now[1] + delta[d][1]
                            if not (0 <= ny < 5 and 0 <= nx < 5): continue
                            if rtField.getitem((ny, nx)) == blockNum: q.append((ny, nx))
                if blockSize >= 3:
                    blockPoses.extend(tmpBlockPoses)
    return len(blockPoses), sorted(blockPoses, key=lambda x: (x[1], -x[0]))


for _ in range(K):
    rtField = RotationableField(field)
    score = 0
    maxRemoveCnt = 0
    maxRemoveStatus = [-1, -1, -1]
    maxRemoveBlocks = []
    # 최선의 선택지 선택
    # (1) 가장 많은 블록이 지워지고
    # (2) 가장 회전 각도가 작으며
    # (3) 가장 열 번호가 작으며 (x)
    # (4) 가장 행 번호가 작은 순서 (y)
    for k in range(3):
        for j in range(3):
            for i in range(3):
                rtField.setLeftTop((i, j))
                rtField.setRotateDegree(k)
                removeCnt, blocks = getCollectableCntandBlockPoses(rtField)
                if maxRemoveCnt < removeCnt:
                    maxRemoveCnt = removeCnt
                    maxRemoveStatus = (i, j, k)
                    maxRemoveBlocks = blocks


    if maxRemoveCnt == 0: break
    # # 최선의 선택지를 기준으로 유물 먹기
    rtField.setLeftTop(maxRemoveStatus[0:2])
    rtField.setRotateDegree(maxRemoveStatus[2])
    score += maxRemoveCnt

    # 블록 지우고 채우기
    for ii, jj in maxRemoveBlocks:
        rtField.setitem((ii, jj), walls.popleft())

    # 연쇄 획득
    # 현재 필드 상태에서 추가적으로 먹을 수 있는 칸 먹고 채우기, 더 이상 못 먹을 때 까지 채우기
    while True:
        # 먹을 수 있는 칸 체크
        removeCnt, blocks = getCollectableCntandBlockPoses(rtField)
        # 더 먹을 칸이 있다면
        if removeCnt > 0:
            score += removeCnt
            for ii, jj in blocks:
                rtField.setitem((ii, jj), walls.popleft())
        else: break

    ans.append(score)
    field = rtField.rotatedField()

print(" ".join(list(map(str, ans))))