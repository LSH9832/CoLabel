import requests
import numpy as np
from io import BytesIO
from PIL.Image import open as imgopen


def base_request(url, json=None, data=None, method="post"):
    method = method.lower()
    if method == "post":
        r = requests.post(url, data, json)
    elif method == "get":
        r = requests.get(url, json)
    else:
        return []

    if r.status_code == 200:
        return r.json()["data"]
    else:
        return []


def file_request(url, json=None, data=None, method="post"):
    method = method.lower()
    if method == "post":
        r = requests.post(url, data, json)
    elif method == "get":
        r = requests.get(url, json)
    else:
        return None
    data = r.json()["data"]
    if data is not None:
        try:
            return bytes(data)
        except:
            pass
    return None


###############################################################################
def test_connect(ip="127.0.0.1", port=12345, user="admin", pwd="admin", **_):
    url = f"http://{ip}:{int(port)}/test_connect"
    json = {"user": user, "password": pwd}
    e = "发生未知错误！"
    try:
        ret = base_request(url, json, method="post")
        if not ret:
            e = "用户名或密码错误！"
    except Exception as err:
        e = "请检查：\n1. IP地址或端口是否正确\n2. 服务器是否打开"
        ret = False
    # print("ret", ret)
    if isinstance(ret, list):
        ret = False
    return ret, e


def get_type_list(ip="127.0.0.1", port=12345, user="admin", pwd="admin", **_):
    url = f"http://{ip}:{int(port)}/get_image_type"
    json = {"user": user, "password": pwd}
    return sorted(base_request(url, json, method="post"))


def get_image_list(ip="127.0.0.1", port=12345, image_type="default", user="admin", pwd="admin", **_):
    url = f"http://{ip}:{int(port)}/get_image_list"
    json = {"user": user, "password": pwd, "image_type": image_type}
    return base_request(url, json, method="post")


def get_image(ip="127.0.0.1", port=12345, image_type="default", image_name="1.jpg", user="admin", pwd="admin", **_):
    url = f"http://{ip}:{int(port)}/get_image"
    json = {"user": user, "password": pwd, "image_type": image_type, "image_name": image_name}

    data = file_request(url, json, method="post")
    if data is not None:
        try:
            file_data = BytesIO(data)
            return np.asarray(imgopen(file_data))
        except:
            pass
    return np.array([[[127, 127, 127]]])


def get_anno(ip="127.0.0.1", port=12345, image_type="default", image_name="1.jpg", user="admin", pwd="admin", **_):
    url = f"http://{ip}:{int(port)}/get_anno"
    json = {"user": user, "password": pwd, "image_type": image_type, "image_name": image_name}
    return base_request(url, json, method="post")


def change_anno(ip="127.0.0.1", port=12345, image_type="default", image_name="1.jpg", items=None, user="admin", pwd="admin", **kwargs):
    url = f"http://{ip}:{int(port)}/change_xml"
    json = {
        "user": user,
        "password": pwd,
        "image_type": image_type,
        "image_name": image_name,
        "items": items if items is not None else []
    }
    # print("kwargs", kwargs)
    for kw in kwargs:
        json[kw] = kwargs[kw]
    return base_request(url, json, method="post")


if __name__ == '__main__':

    test_type = "机枪"
    print(test_connect(port=13579))
    # for image_name in get_image_list(image_type=test_type)[:1]:
    #     # image = get_image(image_type=test_type, image_name=image_name)
    #     # cv2.imshow("test", image)
    #     # cv2.waitKey(0)
    #
    #     for item in get_anno(image_type=test_type, image_name=image_name):
    #         print(item["name"], item["location"])
    #
    #     print(change_anno(image_type=test_type, image_name=image_name, items=[{"name": "person", "location": [100, 100, 200, 203]}]))
    #
    #     for item in get_anno(image_type=test_type, image_name=image_name):
    #         print(item["name"], item["location"])
