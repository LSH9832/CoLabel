from image_client import get_image, get_anno, change_anno

from PyQt5 import QtWidgets
from PyQt5.QtGui import *

import cv2
import numpy as np


__all__ = ["get_color", "Image"]


FlexChooseBoxEdgeRange = 8
__Colors = np.array(
        [
            0.000, 0.447, 0.741,
            0.850, 0.325, 0.098,
            0.929, 0.694, 0.125,
            0.494, 0.184, 0.556,
            0.466, 0.674, 0.188,
            0.301, 0.745, 0.933,
            0.635, 0.078, 0.184,
            0.300, 0.300, 0.300,
            0.600, 0.600, 0.600,
            1.000, 0.000, 0.000,
            1.000, 0.500, 0.000,
            0.749, 0.749, 0.000,
            0.000, 1.000, 0.000,
            0.000, 0.000, 1.000,
            0.667, 0.000, 1.000,
            0.333, 0.333, 0.000,
            0.333, 0.667, 0.000,
            0.333, 1.000, 0.000,
            0.667, 0.333, 0.000,
            0.667, 0.667, 0.000,
            0.667, 1.000, 0.000,
            1.000, 0.333, 0.000,
            1.000, 0.667, 0.000,
            1.000, 1.000, 0.000,
            0.000, 0.333, 0.500,
            0.000, 0.667, 0.500,
            0.000, 1.000, 0.500,
            0.333, 0.000, 0.500,
            0.333, 0.333, 0.500,
            0.333, 0.667, 0.500,
            0.333, 1.000, 0.500,
            0.667, 0.000, 0.500,
            0.667, 0.333, 0.500,
            0.667, 0.667, 0.500,
            0.667, 1.000, 0.500,
            1.000, 0.000, 0.500,
            1.000, 0.333, 0.500,
            1.000, 0.667, 0.500,
            1.000, 1.000, 0.500,
            0.000, 0.333, 1.000,
            0.000, 0.667, 1.000,
            0.000, 1.000, 1.000,
            0.333, 0.000, 1.000,
            0.333, 0.333, 1.000,
            0.333, 0.667, 1.000,
            0.333, 1.000, 1.000,
            0.667, 0.000, 1.000,
            0.667, 0.333, 1.000,
            0.667, 0.667, 1.000,
            0.667, 1.000, 1.000,
            1.000, 0.000, 1.000,
            1.000, 0.333, 1.000,
            1.000, 0.667, 1.000,
            0.333, 0.000, 0.000,
            0.500, 0.000, 0.000,
            0.667, 0.000, 0.000,
            0.833, 0.000, 0.000,
            1.000, 0.000, 0.000,
            0.000, 0.167, 0.000,
            0.000, 0.333, 0.000,
            0.000, 0.500, 0.000,
            0.000, 0.667, 0.000,
            0.000, 0.833, 0.000,
            0.000, 1.000, 0.000,
            0.000, 0.000, 0.167,
            0.000, 0.000, 0.333,
            0.000, 0.000, 0.500,
            0.000, 0.000, 0.667,
            0.000, 0.000, 0.833,
            0.000, 0.000, 1.000,
            0.000, 0.000, 0.000,
            0.143, 0.143, 0.143,
            0.286, 0.286, 0.286,
            0.429, 0.429, 0.429,
            0.571, 0.571, 0.571,
            0.714, 0.714, 0.714,
            0.857, 0.857, 0.857,
            0.000, 0.447, 0.741,
            0.314, 0.717, 0.741,
            0.500, 0.500, 0.000
        ]
).astype(np.float32).reshape(-1, 3)


def get_color(index):
    return tuple(int(c) for c in (255 * __Colors[index % len(__Colors)]))


class Image:

    mode = None   # "move", "resize1-4"
    press_xy = [0, 0]
    isSaved = True

    def __init__(self, img=None, items=None, image_type=None, image_name=None, all_labels=None, msg=None):
        if msg is not None:
            self.img_name = msg["image_name"]
            self.img_type = msg["image_type"]
            self.all_labels = msg["all_labels"]
            self.img = get_image(**msg)
            if len(self.img.shape) == 2:
                self.img = cv2.cvtColor(self.img, cv2.COLOR_GRAY2BGR)
            else:
                self.img = self.img[..., :3]


            self.items = get_anno(**msg)

        else:
            self.img = img
            self.img_name = image_name
            self.img_type = image_type
            self.items = items if items is not None else []
            self.all_labels = all_labels



        self.show_w, self.show_h, _ = self.img.shape if self.img is not None else (0, 0, 3)
        self.ratio = 1

    def to(self, label: QtWidgets.QLabel):

        if self.img is not None:
            area_w, area_h = label.rect().width(), label.rect().height()
            img_h, img_w, _ = self.img.shape

            self.ratio = min(area_w / img_w, area_h / img_h)

            self.image_pad = np.ones([area_h, area_w, 3], dtype="uint8") * 127
            self.show_w, self.show_h = int(self.ratio * img_w), int(self.ratio * img_h)
            self.image_pad[:self.show_h, :self.show_w] = cv2.resize(self.img, (self.show_w, self.show_h))

            self._to(self.image_pad, label)
            return True
        return False

    def _to(self, img, label: QtWidgets.QLabel):
        label.setPixmap(
            QPixmap(
                QImage(
                    img,
                    label.rect().width(),
                    label.rect().height(),
                    label.rect().width() * 3,
                    QImage.Format_RGB888
                )
            ).scaled(label.rect().width(), label.rect().height())
        )

    def anno2list(self, anno_list: QtWidgets.QListWidget):
        anno_list.clear()
        for item in self.items:
            anno_list.addItem(f"{item['name']}")   # {item['location']}

    def draw_bbox(self, label: QtWidgets.QLabel, index=-1, draw=True):
        image = None
        if self.img is not None:

            now_index_data = None
            image = self.image_pad.copy()
            for i, item in enumerate(self.items):

                label_name = item["name"]

                if label_name in self.all_labels:
                    color = get_color(self.all_labels.index(label_name))
                else:
                    color = get_color(len(self.all_labels))
                # print(color)
                x1, y1, x2, y2 = [int(self.ratio * loc) for loc in item["location"]]



                point1, point2 = (x1, y1), (x2, y2)
                color = (70, 255, 96) if index == i else color    # (244, 108, 47)

                if index == i:
                    now_index_data = [x1, y1, x2, y2, point1, point2, color, ]
                    continue

                cv2.rectangle(image, point1, point2, color, 2, cv2.LINE_AA)
            if now_index_data is not None:
                x1, y1, x2, y2, point1, point2, color = now_index_data
                mask = (np.ones([y2 - y1, x2 - x1, 3]) * np.array([[[c for c in color]]])).astype(float)
                ori = image[y1:y2, x1:x2, :].astype(float)
                image[y1:y2, x1:x2, :] = (mask * 0.3 + ori * 0.7).astype("uint8")
                cv2.rectangle(image, point1, point2, color, 2, cv2.LINE_AA)

            if draw:
                self._to(image, label)
        return image

    def changeMode(self, x, y, index):
        if self.img is not None:
            if index >= 0:
                o_loc = self.items[index]["location"]
                x1, y1, x2, y2 = [int(self.ratio * loc) for loc in self.items[index]["location"]]
                if max(abs(x-x2), abs(y-y2)) <= FlexChooseBoxEdgeRange:
                    self.mode = "resize4"
                elif max(abs(x-x1), abs(y-y2)) <= FlexChooseBoxEdgeRange:
                    self.mode = "resize3"
                elif max(abs(x-x2), abs(y-y1)) <= FlexChooseBoxEdgeRange:
                    self.mode = "resize2"
                elif max(abs(x-x1), abs(y-y1)) <= FlexChooseBoxEdgeRange:
                    self.mode = "resize1"
                elif x1 < x < x2 and y1 < y < y2:
                    self.mode = "move"
                    self.press_xy = [x, y]
                    self.w, self.h = int((o_loc[2] - o_loc[0]) * self.ratio), int((o_loc[3] - o_loc[1]) * self.ratio)
                else:
                    self.mode = None
            if self.mode is None:
                for i, item in enumerate(self.items):
                    x1, y1, x2, y2 = [int(self.ratio * loc) for loc in item["location"]]
                    if x1 < x < x2 and y1 < y < y2:
                        return i

        return -1

    def runMode(self, nx, ny, index, label):
        if self.img is not None and index >= 0 and self.mode is not None:
            self.isSaved = False
            o_loc = self.items[index]["location"]
            x1, y1, x2, y2 = [int(self.ratio * loc) for loc in o_loc]

            x1 = max(0, x1)
            y1 = max(0, y1)
            x2 = min(self.show_w, x2)
            y2 = min(self.show_h, y2)
            if self.mode == "resize4":
                x2 = min(self.show_w, max(x1 + 3, nx))
                y2 = min(self.show_h, max(y1 + 3, ny))
            elif self.mode == "resize3":
                x1 = max(0, min(x2 - 3, nx))
                y2 = min(self.show_h, max(y1 + 3, ny))
            elif self.mode == "resize2":
                x2 = min(self.show_w, max(x1 + 3, nx))
                y1 = max(0, min(y2 - 3, ny))
            elif self.mode == "resize1":
                x1 = max(0, min(x2 - 3, nx))
                y1 = max(0, min(y2 - 3, ny))
            elif self.mode == "move":
                minx = -x1
                miny = -y1
                maxx = self.show_w - x2
                maxy = self.show_h - y2
                dx = min(maxx, max(minx, nx - self.press_xy[0]))
                dy = min(maxy, max(miny, ny - self.press_xy[1]))
                self.press_xy = [nx, ny]
                x1, x2, y1, y2 = x1 + dx, x1 + dx + self.w, y1 + dy, y1 + dy + self.h
            now_loc = [x1, y1, x2, y2]
            # print(x2-x1, y2-y1)
            self.items[index]["location"] = [float(loc)/self.ratio for loc in now_loc]
            self.to(label)
            self.draw_bbox(label, index)

    def clearMode(self):
        self.mode = None

    def vh_line(self, x, y, label):
        # image = self.image_pad.copy()
        image = self.draw_bbox(label, draw=False)
        image[:, x] = 0
        image[y, :] = 0
        self._to(image, label)

    def current_box(self, x1, y1, x2, y2, label):
        if x1 > x2:
            x1, x2 = x2, x1
        if y1 > y2:
            y1, y2 = y2, y1

        image = self.draw_bbox(label, draw=False)
        cv2.rectangle(image, (x1, y1), (x2, y2), (70, 255, 96), 2, cv2.LINE_AA)
        self._to(image, label)

    def add_bbox(self, location, name):
        self.isSaved = False
        x1, y1, x2, y2 = location
        location = [max(0, min(x1, x2, self.show_w - 4)),
                    max(0, min(y1, y2, self.show_h - 4)),
                    max(3, min(max(x1, x2), self.show_w - 1)),
                    max(3, min(max(y1, y2), self.show_h - 1))]
        self.items.append({
            "name": name,
            "location": [loc / self.ratio for loc in location]
        })
        return len(self.items) - 1

    def get_items(self):
        items = []
        img_h, img_w, _ = self.img.shape
        for item in self.items:
            x1, y1, x2, y2 = item["location"]
            x1 = int(max(0, x1))
            y1 = int(max(0, y1))
            x2 = int(min(x2, img_w))
            y2 = int(min(y2, img_h))
            items.append({
                "name": item["name"],
                "location": [x1, y1, x2, y2]
            })
        return items

    def remove_item(self, index):
        self.isSaved = False
        del self.items[index]

    def change_label(self, index, name):
        self.isSaved = False
        self.items[index]["name"] = name

    def save(self, **kwargs):
        try:
            change_anno(**kwargs)
            self.isSaved = True
        except:
            pass
