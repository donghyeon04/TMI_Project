import cv2
import module.openCVTMI as openCVTMI
import module.dijkstra as dijkstra
import module.Node_map as Node_map


def TMI(
    user_input_floor_key_1, user_input_node_1, user_input_floor_key_2, user_input_node_2
):
    """
    시작층, 시작노드, 도착층, 도착노드 를 인자로 주면

    시작층과 도착층이 같을때, 해당하는 경로와 이미지경로를,

    시작층과 도착층이 다를때, 해당하는 경로와 이미지경로를 return해주는 함수
    """
    try:
        start_node, start_floor, start_node_map = openCVTMI.find_node(
            user_input_floor_key_1, user_input_node_1
        )
        if start_node is None:
            raise ValueError
    except ValueError:
        print("start_node가 None입니다. 다른 값을 사용해주세요.")
        return
    except AttributeError:
        print(
            "user_input_floor_key_1 에 잘못된 정보를 입력하여 start_floor과 start_node_map에 에러가 발생했습니다."
        )
        return

    try:
        end_node, end_floor, end_node_map = openCVTMI.find_node(
            user_input_floor_key_2, user_input_node_2
        )
        if end_node is None:
            raise ValueError
    except ValueError:
        print("end_node가 None입니다. 다른 값을 사용해주세요.")
        return
    except AttributeError:
        print(
            "user_input_floor_key_2 에 잘못된 정보를 입력하여 end_floor과 end_node_map에 에러가 발생했습니다."
        )
        return

    if start_floor == end_floor:
        path_list = dijkstra.dijkstra(start_node_map, start_node, end_node)
        if start_floor <= -1:
            start_floor = "B" + str(abs(start_floor))
        if end_floor <= -1:
            end_floor = "B" + str(abs(end_floor))
        img_path = eval(f"Node_map.vision_{start_floor}f['vision_{start_floor}f_img']")

    elif start_floor != end_floor:
        min_paths = []

        if (
            "엘리베이터1_(컨벤션센터쪽)" in end_node_map.keys()
            and (start_floor == "5" or start_floor == "7")
            and end_node != "가천 컨벤션 센터"
        ):
            path_elevator_A = [
                len(dijkstra.dijkstra(end_node_map, end_node, "엘리베이터1_(컨벤션센터쪽)")),
                "엘리베이터1_(컨벤션센터쪽)",
            ]
            min_paths.append(path_elevator_A)
        elif "엘리베이터2_(컨벤션센터쪽)" in end_node_map.keys():
            path_elevator_B = [
                len(dijkstra.dijkstra(end_node_map, end_node, "엘리베이터2_(컨벤션센터쪽)")),
                "엘리베이터2_(컨벤션센터쪽)",
            ]
            min_paths.append(path_elevator_B)
        elif "엘리베이터3_(법과대학쪽)" in end_node_map.keys():
            path_elevator_C = [
                len(dijkstra.dijkstra(end_node_map, end_node, "엘리베이터3_(법과대학쪽)")),
                "엘리베이터3_(법과대학쪽)",
            ]
            min_paths.append(path_elevator_C)
        elif "엘리베이터4_(법과대학쪽)" in end_node_map.keys():
            path_elevator_D = [
                len(dijkstra.dijkstra(end_node_map, end_node, "엘리베이터4_(법과대학쪽)")),
                "엘리베이터4_(법과대학쪽)",
            ]
            min_paths.append(path_elevator_D)

        min_path = min(min_paths, key=lambda x: x[0])[1]

        path_list_first = dijkstra.dijkstra(start_node_map, start_node, min_path)
        path_list_second = dijkstra.dijkstra(end_node_map, min_path, end_node)

        if start_floor <= -1:
            start_floor = "B" + str(abs(start_floor))
        if end_floor <= -1:
            end_floor = "B" + str(abs(end_floor))
        first_img_path = eval(
            f"Node_map.vision_{start_floor}f['vision_{start_floor}f_img']"
        )
        second_img_path = eval(
            f"Node_map.vision_{end_floor}f['vision_{end_floor}f_img']"
        )

    if start_floor == end_floor:  # 시작층과 도착층이 같을때
        path = (start_floor, path_list, img_path, True)
        return path
    else:  # 시작층과 도착층이 다를때
        path = (
            (start_floor, path_list_first, first_img_path),
            (end_floor, path_list_second, second_img_path),
            False,
        )
        return path


# 첫번째 튜플은 (첫번째 경로, 첫번째 이미지경로)/두번째 튜플은 (두번째 경로, 두번째 이미지경로)
def TMI_img(path):
    if path[-1] == True:  # 같은 층정보
        img = cv2.imread(path[2])
        # img = cv2.resize(img, (1117, 628)) #이미지 불러오기

        floor_key = f"{path[0]}f"
        location_key = f"vision_{floor_key}_location"
        location = getattr(Node_map, f"vision_{floor_key}")[location_key]

        openCVTMI.displayline(img, path[1], location, (140, 73, 0), 3)
        openCVTMI.displaypoint_start(img, path[1][0], location)
        openCVTMI.displaypoint_end(img, path[1][-1], location)

        return img

    else:  # 다른층정보
        img_first = cv2.imread(path[0][-1])
        # img = cv2.resize(img, (1117, 628)) #이미지 불러오기

        floor_key = f"{path[0][0]}f"
        location_key = f"vision_{floor_key}_location"
        location = getattr(Node_map, f"vision_{floor_key}")[location_key]

        openCVTMI.displayline(img_first, path[0][1], location, (140, 73, 0), 3)
        openCVTMI.displaypoint_start(img_first, path[0][1][0], location)
        openCVTMI.displaypoint_end(img_first, path[0][1][-1], location)

        img_second = cv2.imread(path[1][-1])
        # img = cv2.resize(img, (1117, 628)) #이미지 불러오기

        floor_key = f"{path[1][0]}f"
        location_key = f"vision_{floor_key}_location"
        location = getattr(Node_map, f"vision_{floor_key}")[location_key]
        openCVTMI.displayline(img_second, path[1][1], location, (140, 73, 0), 3)
        openCVTMI.displaypoint_start(img_second, path[1][1][0], location)
        openCVTMI.displaypoint_end(img_second, path[1][1][-1], location)

        return img_first, img_second
