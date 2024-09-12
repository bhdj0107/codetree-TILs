from collections import defaultdict
import math
# 명령의 수 Q, 도시 의 수 n, 간선의 수 m
# v 도시와 u 도시는 w 길이의 간선으로 연결됨

Q = int(input())
querys = [map(int, input().split()) for _ in range(Q)]


def daijkstra(connection, startPt):
    dist = [math.inf for _ in range(len(connection))]
    visited = [False for _ in range(len(connection))]
    dist[startPt] = 0
    while True:
        # 방문하지 않은 점 중 가장 거리가 짧은 점을 선택
        minPos = -1
        minDist = math.inf
        for i in range(len(connection)):
            if visited[i]: continue
            else:
                if minDist > dist[i]: minPos, minDist = i, dist[i]
        
        # 방문할 점이 없다면 break
        if minPos == -1: break
        
        else:
            visited[minPos] = True
            # 해당 지점의 연결정보를 기반으로 거리배열 갱신
            for i in range(len(connection)):
                dist[i] = min(dist[i], minDist + connection[minPos][i])
    return dist
def sellablePackage(package, dist):
    ret = []
    for package_id, (rev, dst) in package.items():
        if rev - dist[dst] >= 0: ret.append((package_id, rev - dist[dst]))
    ret.sort(key=lambda x: (-x[1], x[0]), reverse=True)
    return ret

package = {}
lastUpdated = -1
lastCalculated = -1

for t, query in enumerate(querys):
    query = list(query)
    if query[0] == 100:
        N, M = query[1:3]
        connection = [[math.inf for _ in range(N)] for _ in range(N)]
        for i in range(N): connection[i][i] = 0
        for i in range(3, len(query), 3):
            v, u, w = query[i:i+3]
            connection[v][u] = min(connection[v][u], w)
            connection[u][v] = min(connection[u][v], w)
        dist = daijkstra(connection, 0)
        
    elif query[0] == 200:
        package_id, rev, dst = query[1:]
        package[package_id] = (rev, dst)
        lastUpdated = t

    elif query[0] == 300:
        package_id = query[1]
        if package.get(package_id):
            del package[package_id]
            lastUpdated = t
    
    elif query[0] == 400:
        if lastUpdated > lastCalculated:
            sellable = sellablePackage(package, dist)
            lastCalculated = t
        if len(sellable):
            pid = sellable.pop()[0]
            print(pid)
            del package[pid]
            
        else: print(-1)
        
    elif query[0] == 500:
        newSrc = query[1]
        dist = daijkstra(connection, newSrc)
        lastUpdated = t