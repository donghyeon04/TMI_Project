import cv2, numpy
import module.Node_map as Node_map


def displayline(img, path, path_location, BGR, t):
    """
    최단경로 노드들을 직선으로 표시해줌

    img : 경로가 표시될 이미지
    path : 최단경로 노드 리스트
    path_location : 각 노드들의 위치값
    BGR : 색상
    t : 선 두께"""
    for point_x, point_y in zip(path, path[1:]):
        cv2.line(img, path_location[point_x], path_location[point_y], BGR, t)

    return img


def displaypoint_start(img, coordinate, location):
    """
    시작지점 좌표에 시작 마커를 표시해줌

    img : 이미지
    coordinate : 좌표
    """
    marker = cv2.imread("Vision_Tower_Image/start_marker.png", -1)

    h, w, _ = marker.shape
    marker = cv2.resize(marker, (w // 6, h // 6))
    h, w, _ = marker.shape

    if isinstance(coordinate, str):
        coordinate = location[coordinate]
        x_offset, y_offset = coordinate

    else:
        x_offset, y_offset = coordinate

    x_offset -= 42
    y_offset -= 80

    for c in range(0, 3):
        img[y_offset : y_offset + h, x_offset : x_offset + w, c] = marker[:, :, c] * (
            marker[:, :, 3] / 255.0
        ) + img[y_offset : y_offset + h, x_offset : x_offset + w, c] * (
            1.0 - marker[:, :, 3] / 255.0
        )

    return img


def displaypoint_end(img, coordinate, location):
    """
    도착지점 좌표에 도착 마커를 표시해줌

    img : 이미지
    coordinate : 좌표
    """
    marker = cv2.imread("Vision_Tower_Image/end_marker.png", -1)

    h, w, _ = marker.shape
    marker = cv2.resize(marker, (w // 6, h // 6))
    h, w, _ = marker.shape

    if isinstance(coordinate, str):
        coordinate = location[coordinate]
        x_offset, y_offset = coordinate

    else:
        x_offset, y_offset = coordinate

    x_offset -= 14
    y_offset -= 84

    for c in range(0, 3):
        img[y_offset : y_offset + h, x_offset : x_offset + w, c] = marker[:, :, c] * (
            marker[:, :, 3] / 255.0
        ) + img[y_offset : y_offset + h, x_offset : x_offset + w, c] * (
            1.0 - marker[:, :, 3] / 255.0
        )

    return img
    return img


def find_node(floor_key, user_input):
    """
    floor_key로 층정보를 입력하고, user_input을 통해 노드값을 전달한다.

    이를 통해 각 노드값, 층정보에 알맞는
    node값, floor값, node_map 값을 리턴한다.
    """
    floor_info = getattr(Node_map, floor_key)
    node_map = floor_info[f"{floor_key}_node"]
    floor = floor_info[f"{floor_key}_floor"]
    node = None

    for key in node_map:
        if key == user_input:
            node = key
            break

    return node, floor, node_map
