import heapq  # 우선순위 큐를 만들 heapq 모듈 불러오기


def dijkstra(graph, start, end):  # 다익스트라함수에 알고리즘을 적용할 graph값과 출발지점과 끝지점 호출
    distances = {
        vertex: [float("inf"), start] for vertex in graph
    }  # 거리값을 inf(무한대로) 초기화하여 distances 딕셔너리에 저장 /// 입력한 graph의 각각의 키가 반복문 안으로 들어오고, 그 반복문이 실행될때마다 해당 노드에 inf값을 넣어줌
    distances[start] = [0, start]  # 시작지점의 값을 0으로 초기화

    queue = []  # 우선순위 큐를 이용할 queue라는 리스트 생성
    heapq.heappush(
        queue, [distances[start][0], start]
    )  # heappush 함수 : 힙에 원소를 추가하는 함수 /// queue라는 우선순위 큐에 0으로 초기화한 start와 start 이루어진 리스트 추가

    while queue:
        current_distance, current_vertex = heapq.heappop(
            queue
        )  # queue값을 넘기고 삭제 / 리스트 pop연산  /// current_distance에는 queue리스트의 value값, current_vertex에는 key값 대입

        if (
            distances[current_vertex][0] < current_distance
        ):  # 만약 새로 구한 최단거리보다 원래 있던 최단거리가 더 짧으면 continue /// distances 리스트에 원래 들어있던 currnet_vertex 키의 value값과 새로 구한 current_distance 값(queue 리스트의 value값)
            continue

        for adjacent, weight in graph[
            current_vertex
        ].items():  # adjacent : 인접된 노드 이름을 대입, weight : 그 인접된 노드에 접근할때의 거리 대입 /// @@@ dict_items([])?
            distance = (
                current_distance + weight
            )  # 현재까지 들어온 거리 + 인접된 노드에 접근하는데 드는 거리 = distance

            if (
                distance < distances[adjacent][0]
            ):  # 만약 인접노드까지 기존에 distances에 들어가있던 인접노드까지의 거리의 최단 거리보다 작으면
                distances[adjacent] = [
                    distance,
                    current_vertex,
                ]  # 기존값에 새로 발견한 최단거리 값으로 업데이트해라
                heapq.heappush(queue, [distance, adjacent])  # 최단거리를 우선순위 큐에 업데이트해라

    path = end  # path(경로) 변수에 end값 대입
    path_list = []  # 경로가 순서대로 들어갈 빈 리스트
    while distances[path][1] != start:  # distances리스트의 end값 리스트의 노드 이름이 시작 노드와 다를때 반복해라
        path_list.append(distances[path][1])
        path = distances[path][1]  # 같을때까지 path_list 리스트에 대입해라

    path_list.reverse()  # 반대로 대입되었으니까 뒤집기
    path_list.insert(0, distances[path][1])  # 시작값과 같아졌으니까 따로 대입해주기
    path_list.append(end)  # 끝지점 대입

    return path_list  # 지금까지 구한 최단거리가 적힌 리스트를 return해주기
