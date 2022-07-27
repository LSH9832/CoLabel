from flask import *
from glob import glob
from lxml import etree
import os.path as osp
import cv2
import numpy as np

app = Flask(__name__)


DEFAULT_ROOT_PATH = "./images"


def file2int(file_name):
    if not osp.isfile(file_name):
        cv2.imwrite("temp.jpg", np.array([[[0,0, 255]]]).astype("uint8"))
        file_name = "temp.jpg"
    return [i for i in open(file_name, "rb").read()]


class __RootPath:

    def __init__(self, path="./images"):
        self.__root_path = path

    def set(self, path: str):
        if osp.isdir(path):
            self.__root_path = path

    def get(self):
        return self.__root_path

    def __repr__(self):
        return self.__root_path


class __UserPwd:

    def __init__(self, username="admin", password="admin"):
        self.__user = username
        self.__password = password

    def set(self, user=None, password=None):
        if user is not None:
            self.__user = user
        if password is not None:
            self.__password = password

    def get(self):
        return self.__user, self.__password

    def check(self, data):
        if "user" in data and "password" in data:
            if data["user"] == self.__user and data["password"] == self.__password:
                return True
        return False


UserPwd = __UserPwd()
ROOTPATH = __RootPath()


# 获取信息
####################################################################
@app.route("/test_connect", methods=["POST"])
def test_connect():
    return {"data": UserPwd.check(request.json)}


@app.route("/get_image_type", methods=["POST"])
def get_image_type():
    all_dirs = []
    if UserPwd.check(request.json):
        [all_dirs.append(this_dir.replace("\\", "/").split("/")[-1]) if osp.isdir(this_dir) else None
         for this_dir in glob(osp.join(ROOTPATH.get(), "*"))]
    return {"data": all_dirs}


@app.route("/get_image_list", methods=["POST"])
def get_image_list():
    data = request.json
    # print(data, type(data))
    all_images = []
    if UserPwd.check(data):
        if "image_type" in data:
            if osp.isdir(osp.join(ROOTPATH.get(), data['image_type'])):
                for file_type in ["jpg", "png", "bmp", "gif", "webp", "jpeg"]:
                    all_images += glob(osp.join(ROOTPATH.get(), data['image_type'], f"*.{file_type}"))
                all_images = sorted([image_name.replace("\\", "/").split("/")[-1] for image_name in all_images])
    return {"data": all_images}


@app.route("/get_image", methods=["POST"])
def get_image():
    data = request.json
    
    ret_data = "./utils/wrong.jpg"
    if UserPwd.check(data):
        if "image_type" in data and "image_name" in data:
            file_name = osp.join(ROOTPATH.get(), data['image_type'], data['image_name'])
            if osp.isfile(file_name):
                ret_data = file_name

    return {"data": file2int(ret_data)}


@app.route("/get_anno", methods=["POST"])
def get_anno():

    data = request.json

    ret_data = []
    if UserPwd.check(data):
        if "image_type" in data and "image_name" in data:
            file_name = osp.join(ROOTPATH.get(), data['image_type'], data['image_name'][:-4] + ".xml")
            if osp.isfile(file_name):
                xml = etree.HTML(open(file_name).read())
                for obj in xml.xpath("//object"):
                    bndbox = obj.xpath("bndbox")[0]
                    ret_data.append({
                        "name": obj.xpath("name")[0].text,
                        "location": [
                            int(bndbox.xpath("xmin")[0].text),
                            int(bndbox.xpath("ymin")[0].text),
                            int(bndbox.xpath("xmax")[0].text),
                            int(bndbox.xpath("ymax")[0].text),
                        ]
                    })

    return {"data": ret_data}


# 修改信息
#######################################################################
@app.route("/change_xml", methods=["POST"])
def change_xml():
    data = request.json

    ret_data = False
    if UserPwd.check(data):
        if "image_type" in data and "image_name" in data and "items" in data:
            file_name = osp.join(ROOTPATH.get(), data['image_type'], data['image_name'][:-4] + ".xml")
            w, h, d = 0, 0, 0
            if "image_size" in data:
                h, w, d = data["image_size"]
            xml_str = f"""    <folder>FOLDER</folder>
    <filename>{data['image_name']}</filename>
    <path>PATH</path>
    <source>
        <database>DATABASE</database>
    </source>
    <size>
        <width>{w}</width>
        <height>{h}</height>
        <depth>{d}</depth>
    </size>
    <segmented>0</segmented>"""
            insert_str = ""
            for item in data["items"]:
                insert_str += f"""\n\t<object>
\t\t<name>{item["name"]}</name>
\t\t<pose>Unspecified</pose>
\t\t<truncated>0</truncated>
\t\t<difficult>0</difficult>
\t\t<bndbox>
\t\t\t<xmin>{item["location"][0]}</xmin>
\t\t\t<ymin>{item["location"][1]}</ymin>
\t\t\t<xmax>{item["location"][2]}</xmax>
\t\t\t<ymax>{item["location"][3]}</ymax>
\t\t</bndbox>
\t</object>""".replace("\t", "    ")
            total_str = f"""<annotation>
{xml_str}{insert_str}
</annotation>"""
            open(file_name, "w").write(total_str)
            ret_data = True
    return {"data": ret_data}


if __name__ == '__main__':
    ROOTPATH.set("./images")
    app.run("0.0.0.0", 12345, False)
