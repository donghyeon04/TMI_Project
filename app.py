from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect,
    url_for,
    send_from_directory,
)
import cv2, base64
import module.Node_map as Node_map
import module.main as main
import module.openCVTMI as openCVTMI

app = Flask(__name__)
app.secret_key = "TMI"

floor = {
    "비전타워 B3층": "vision_B3f",
    "비전타워 B2층": "vision_B2f",
    "비전타워 B1층": "vision_B1f",
    "비전타워 1층": "vision_1f",
    "비전타워 2층": "vision_2f",
    "비전타워 3층": "vision_3f",
    "비전타워 4층": "vision_4f",
    "비전타워 5층": "vision_5f",
    "비전타워 6층": "vision_6f",
    "비전타워 7층": "vision_7f",
}
start_node = {}


def node_find(floor):
    # select_start_floor에 따라 적절한 노드 정보를 로드
    if floor == "vision_B3f":
        start_node = list(Node_map.vision_B3f[floor + "_node"].keys())
        start_node = [x for x in start_node if "node_" not in x]
    elif floor == "vision_B2f":
        start_node = list(Node_map.vision_B2f[floor + "_node"].keys())
        start_node = [x for x in start_node if "node_" not in x]
    elif floor == "vision_B1f":
        start_node = list(Node_map.vision_B1f[floor + "_node"].keys())
        start_node = [x for x in start_node if "node_" not in x]
    elif floor == "vision_1f":
        start_node = list(Node_map.vision_1f[floor + "_node"].keys())
        start_node = [x for x in start_node if "node_" not in x]
    elif floor == "vision_2f":
        start_node = list(Node_map.vision_2f[floor + "_node"].keys())
        start_node = [x for x in start_node if "node_" not in x]
    elif floor == "vision_3f":
        start_node = list(Node_map.vision_3f[floor + "_node"].keys())
        start_node = [x for x in start_node if "node_" not in x]
    elif floor == "vision_4f":
        start_node = list(Node_map.vision_4f[floor + "_node"].keys())
        start_node = [x for x in start_node if "node_" not in x]
    elif floor == "vision_5f":
        start_node = list(Node_map.vision_5f[floor + "_node"].keys())
        start_node = [x for x in start_node if "node_" not in x]
    elif floor == "vision_6f":
        start_node = list(Node_map.vision_6f[floor + "_node"].keys())
        start_node = [x for x in start_node if "node_" not in x]
    elif floor == "vision_7f":
        start_node = list(Node_map.vision_7f[floor + "_node"].keys())
        start_node = [x for x in start_node if "node_" not in x]
    else:
        start_node = []
    return start_node


def process_floor_image_start(selected_floor, selected_node):
    # 선택된 층 정보에 해당하는 이미지 가져오기

    if selected_floor == "wating_img":
        selected_floor_img = "Vision_Tower_Image/wating_img.png"

        img = cv2.imread(selected_floor_img)

        _, encoded_image = cv2.imencode(".png", img)
        selected_floor_img = base64.b64encode(encoded_image).decode("utf-8")

        return selected_floor_img
    else:
        path_dict = getattr(Node_map, selected_floor)

        path = selected_floor + "_img"

        image_path = path_dict[path]

        # 이미지 로드
        img = cv2.imread(image_path)

        if not isinstance(selected_node, list):
            point_dict = getattr(Node_map, selected_floor)
            point = selected_floor + "_location"
            point_name = selected_node

            point = point_dict[point][point_name]
            img = openCVTMI.displaypoint_start(img, point, point)

        # 이미지 인코딩 및 변환
        _, encoded_image = cv2.imencode(".png", img)
        selected_floor_img = base64.b64encode(encoded_image).decode("utf-8")

        return selected_floor_img


def process_floor_image_end(selected_floor, selected_node):
    # 선택된 층 정보에 해당하는 이미지 가져오기

    if selected_floor == "wating_img":
        selected_floor_img = "Vision_Tower_Image/wating_img.png"

        img = cv2.imread(selected_floor_img)

        _, encoded_image = cv2.imencode(".png", img)
        selected_floor_img = base64.b64encode(encoded_image).decode("utf-8")

        return selected_floor_img
    else:
        path_dict = getattr(Node_map, selected_floor)

        path = selected_floor + "_img"

        image_path = path_dict[path]

        # 이미지 로드
        img = cv2.imread(image_path)

        if not isinstance(selected_node, list):
            point_dict = getattr(Node_map, selected_floor)
            point = selected_floor + "_location"
            point_name = selected_node

            point = point_dict[point][point_name]
            img = openCVTMI.displaypoint_end(img, point, point)

        # 이미지 인코딩 및 변환
        _, encoded_image = cv2.imencode(".png", img)
        selected_floor_img = base64.b64encode(encoded_image).decode("utf-8")

        return selected_floor_img


@app.route("/")  # 첫페이지
def index():
    return render_template("index.html")


@app.route("/start_info")  # 시작 층정보 선택
def start_infomaition():
    return render_template("index_start.html", start_floor=floor)


@app.route("/start_info", methods=["POST"])  # 시작 노드 선택
def select_start():
    selected_floor_start = request.form.get("start_floor")
    session["selected_floor_start"] = selected_floor_start

    selected_node_start = request.form.get("start_node")
    session["selected_node_start"] = selected_node_start

    start_node = node_find(selected_floor_start)

    if selected_floor_start == "wating_img" or selected_floor_start is None:
        selected_floor_start = "wating_img"
        selected_floor_start_img = process_floor_image_start(
            selected_floor_start, selected_node_start
        )
    elif selected_node_start is not None and selected_node_start != "default":
        selected_floor_start_img = process_floor_image_start(
            selected_floor_start, selected_node_start
        )
    else:
        selected_floor_start_img = process_floor_image_start(
            selected_floor_start, start_node
        )

    return render_template(
        "index_start.html",
        start_floor=floor,
        start_node=start_node,
        selected_floor_start_img=selected_floor_start_img,
    )


@app.route("/end_info", methods=["POST"])  # 도착 층정보 선택
def select_end():
    selected_floor_end = request.form.get("end_floor")
    session["selected_floor_end"] = selected_floor_end

    selected_node_end = request.form.get("end_node")
    session["selected_node_end"] = selected_node_end

    end_node = node_find(selected_floor_end)

    if selected_floor_end == "wating_img" or selected_floor_end is None:
        selected_floor_end = "wating_img"
        selected_floor_end_img = process_floor_image_end(
            selected_floor_end, selected_node_end
        )
    elif selected_node_end is not None and selected_node_end != "default":
        selected_floor_end_img = process_floor_image_end(
            selected_floor_end, selected_node_end
        )
    else:
        selected_floor_end_img = process_floor_image_end(selected_floor_end, end_node)

    return render_template(
        "index_end.html",
        end_floor=floor,
        end_node=end_node,
        selected_floor_end_img=selected_floor_end_img,
    )


@app.route("/selected", methods=["POST"])  # 도착 노드를 받고, 세션화, 그리고 TMI_img로 리다이렉트
def select_end_node():
    user_input_floor_key_1 = session["selected_floor_start"]
    user_input_node_1 = session["selected_node_start"]

    user_input_floor_key_2 = session["selected_floor_end"]
    user_input_node_2 = session["selected_node_end"]

    session["path"] = main.TMI(
        user_input_floor_key_1,
        user_input_node_1,
        user_input_floor_key_2,
        user_input_node_2,
    )

    return redirect(url_for("TMI_img"))


@app.route("/img_displaying")
def TMI_img():
    img_result = main.TMI_img(session["path"])
    if isinstance(img_result, tuple):
        img1, img2 = img_result
        trash1, encoded_image1 = cv2.imencode(".png", img1)
        trash2, encoded_image2 = cv2.imencode(".png", img2)

        first_img = base64.b64encode(encoded_image1).decode("utf-8")
        second_img = base64.b64encode(encoded_image2).decode("utf-8")

        return render_template(
            "index_img.html", first_img=first_img, second_img=second_img
        )
    else:
        img = img_result
        tarsh1, encoded_image = cv2.imencode(".png", img)
        img = base64.b64encode(encoded_image).decode("utf-8")

        return render_template("index_img.html", img=img)


@app.route("/Vision_Tower_Image/<path:filename>")
def vision_tower_image(filename):
    return send_from_directory("Vision_Tower_Image", filename)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
