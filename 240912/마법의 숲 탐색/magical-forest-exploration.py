from collections import deque

# direction {0:N, 1:E, 2:S, 3:W}
class Forest:
    def __init__(self, R, C):
        self.cells = [[0 for _ in range(C)] for _ in range(R + 3)]
        self.R = R + 3
        self.C = C
        
    def chkCanMove(self, golem_center_pos, direction):
        # 아래 방향일 때
        if direction == 2: dcells2chk = ((1, -1), (2, 0), (1, 1))
        # 왼쪽 방향일 때
        elif direction == 3: dcells2chk = ((-1, -1), (0, -2), (1, -1))
        # 오른쪽 방향일 때
        elif direction == 1: dcells2chk = ((-1, 1), (0, 2), (1, 1))
        for dcell in dcells2chk:
            ny, nx = golem_center_pos[0] + dcell[0], golem_center_pos[1] + dcell[1]
            if ny < 0 or ny >= self.R or nx < 0 or nx >= self.C: return False
            if self.cells[ny][nx] != 0: return False
        return True
        
    def setGolem_and_Move2southest(self, golem_c, golem_d, golem_id):
        golem_pos = [1, golem_c]
        golem_d = golem_d
        while True:
            # 아래로 이동가능한지 체크
            if self.chkCanMove(golem_pos, 2):
                # 아래로 이동 가능하면
                # 중심 좌표를 아래로 한칸 내림
                golem_pos[0] += 1
                continue
            # 좌측으로 이동 가능한지
            elif self.chkCanMove(golem_pos, 3):
                tmp_golem_pos = (golem_pos[0], golem_pos[1] - 1)
                # 이동 후에 아래로 이동이 가능한지
                if self.chkCanMove(tmp_golem_pos, 2):
                    # 최종 위치로 이동 가능하면
                    # 중심 좌표를 좌로 한칸, 아래로 한칸 옮김
                    golem_pos[0] += 1
                    golem_pos[1] -= 1
                    # 골렘을 반시계 방향으로 돌림
                    golem_d = (golem_d + 3) % 4
                    continue
            # 우측으로 이동 가능한지
            elif self.chkCanMove(golem_pos, 1):
                tmp_golem_pos = (golem_pos[0], golem_pos[1] + 1)
                # 이동 후에 아래로 이동이 가능한지
                if self.chkCanMove(tmp_golem_pos, 2):
                    # 최종 위치로 이동 가능하면
                    # 중심 좌표를 우로 한칸, 아래로 한칸 옮김
                    golem_pos[0] += 1
                    golem_pos[1] += 1
                    # 골렘을 시계 방향으로 돌림
                    golem_d = (golem_d + 1) % 4
                    continue
            
            # 여기까지 도달하면 더이상 이동이 불가하므로,
            break
        
        # 최종 결정된 골렘의 중심좌표 R이 3 이하 일 경우, 골렘이 숲 바깥으로 빠져나온 것이다
        # 이를 바깥에 return 한다.
        if golem_pos[0] <= 3: return False
        
        # 최종으로 정해진 위치에 골렘을 설치한다.
        # 홀수는 골렘의 출구로 판정한다
        # 북, 동, 남, 서
        final_golem_delta = ((-1, 0), (0, 1), (1, 0), (0 , -1), (0, 0))
        golem_outlet = None
        for d in range(5):
            ny, nx = golem_pos[0] + final_golem_delta[d][0], golem_pos[1] + final_golem_delta[d][1]
            if d == golem_d:
                golem_outlet = (ny, nx)
                self.cells[ny][nx] = golem_id * 2 + 1
            else:
                self.cells[ny][nx] = golem_id * 2 + 2
        
        # 골렘이 정상적으로 설치되고 나면, 이동 가능한 경로를 계산해야 하므로
        # 골렘의 출구 좌표를 return 한다
        return golem_outlet

    def getSpritsSouthestRow(self, start_pos):
        q = deque()
        visited = [[False for _ in range(self.C)] for _ in range(self.R)]
        ret = (-1, -1)
        q.append(start_pos)
        delta = ((1, 0), (0, 1), (-1, 0), (0, -1))
        while q:
            y, x = q.popleft()
            if visited[y][x]: continue
            else:
                visited[y][x] = True
                if ret[0] < y: ret = (y, x)
                # 현재 칸이 골렘의 출구라면
                # 주변의 빈칸이 아닌 어떤 칸이라도 움직일 수 있음
                if self.cells[y][x] % 2 == 1:
                    for d in range(4):
                        ny, nx = y + delta[d][0], x + delta[d][1]
                        if ny < 0 or nx < 0 or ny >= self.R or nx >= self.C: continue
                        if self.cells[ny][nx] == 0: continue
                        q.append((ny, nx))
                        
                # 현재 칸이 골렘의 출구가 아니라면
                # 현재 칸과 같은 값을 가지는 (같은 골렘 내부에서만) 움직일 수 있음
                elif self.cells[y][x] % 2 == 0:
                    for d in range(4):
                        ny, nx = y + delta[d][0], x + delta[d][1]
                        if ny < 0 or nx < 0 or ny >= self.R or nx >= self.C: continue
                        if self.cells[ny][nx] in (self.cells[y][x], self.cells[y][x] - 1):
                            q.append((ny, nx))
                            
        return (ret[0] - 2, ret[1])
    
    def clearField(self):
        self.cells = [[0 for _ in range(self.C)] for _ in range(self.R)]

R, C, K = map(int, input().split())
querys = [map(int, input().split()) for _ in range(K)]
forest = Forest(R, C)

ret = 0
for id, (c, d) in enumerate(querys):
    c -= 1
    is_golem_set = forest.setGolem_and_Move2southest(c, d, id)
    if is_golem_set:
        thisGolemOutlet = is_golem_set
        reachableSoutestPos = forest.getSpritsSouthestRow(thisGolemOutlet)
        reachableSoutest = reachableSoutestPos[0]
        ret += reachableSoutest
    else:
        forest.clearField()
print(ret)