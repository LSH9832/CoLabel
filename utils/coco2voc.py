try:
    from .voc2coco import COCO
except:
    try:
        from utils.voc2coco import COCO
    except:
        from voc2coco import COCO

from glob import glob
import os.path as osp
import os
import warnings
from multiprocessing import Queue
import shutil


class COCODataset:

    data = {}
    length = 0

    def __init__(self, json_file, image_path: str, image_type="jpg", q: Queue=None):
        self.json_file = json_file
        self.image_path = image_path
        self.image_list = [f.replace("\\", "/") for f in glob(osp.join(image_path, f"*.{image_type}"))]
        # print(self.image_list)

        self.q = q
        self.show_data = ""
        self.init_data()


    def init_data(self):
        self.data = {}
        with COCO(self.json_file) as coco:
            coco._count_category_num()
            self.length = len(coco.images)
            self.show_data = coco.show_each_category_num(35, True)
            for img_data in coco.get_images():
                self.data[img_data["id"]] = {
                    "file_name": img_data["file_name"],
                    "size": [img_data["width"], img_data["height"]],
                    "labels": []
                }

            for anno_data in coco.annotations:
                # print(anno_data)
                self.data[anno_data["image_id"]]["labels"].append({
                    "bbox": anno_data["bbox"],
                    "name": coco._get_name_by_category_id(anno_data["category_id"])
                })

    def toVOC(self, dist_path: str, dataset_name: str):

        dist_path = osp.join(dist_path, dataset_name).replace('\\', '/')

        anno_dir = osp.join(dist_path, "annotations").replace('\\', '/')
        img_dir = osp.join(dist_path, "images").replace('\\', '/')

        os.makedirs(anno_dir, exist_ok=True)
        os.makedirs(img_dir, exist_ok=True)

        max_i = 1000

        for i, img_data in enumerate(self.data.items()):
            _, img_data = img_data
            print(f"\rConverting {str(i+1).zfill(len(str(self.length)))} / {self.length}", end="")

            file_name: str = img_data["file_name"]
            ori_file_path = osp.join(self.image_path, file_name).replace('\\', '/')

            if ori_file_path not in self.image_list:
                warnings.warn(f"file {ori_file_path} not found!", osp.exists(ori_file_path))
                continue
            dist_file_path = osp.join(img_dir, file_name).replace('\\', '/')
            anno_path = osp.join(anno_dir, f"{file_name.split('.')[0]}.xml").replace('\\', '/')

            img_part = f"""    <folder>{img_dir}</folder>
    <filename>{file_name}</filename>
    <path>{ori_file_path}</path>
    <source>
        <database>{dataset_name}</database>
    </source>
    <size>
        <width>{img_data["size"][0]}</width>
        <height>{img_data["size"][1]}</height>
        <depth>3</depth>
    </size>
    <segmented>0</segmented>"""

            anno_part = ""
            for item in img_data["labels"]:
                anno_part += f"""\n\t<object>
\t\t<name>{item["name"]}</name>
\t\t<pose>Unspecified</pose>
\t\t<truncated>0</truncated>
\t\t<difficult>0</difficult>
\t\t<bndbox>
\t\t\t<xmin>{item["bbox"][0]}</xmin>
\t\t\t<ymin>{item["bbox"][1]}</ymin>
\t\t\t<xmax>{item["bbox"][2]}</xmax>
\t\t\t<ymax>{item["bbox"][3]}</ymax>
\t\t</bndbox>
\t</object>""".replace("\t", "    ")

            with open(anno_path, "w") as f:
                f.write(f"<annotation>\n{img_part}{anno_part}\n</annotation>")

            shutil.copyfile(ori_file_path, dist_file_path)

            if self.q is not None:
                if self.q.empty() or i + 1 == self.length:
                    self.q.put(int(float(i) / float(self.length) * max_i))

        if self.q is not None:
            self.q.put(max_i)
            self.q.put(self.show_data)
        print()
        print("Conversion finish.")


def coco2voc(
        image_path,
        json_file,
        target_dir,
        dataset_name,
        q: Queue
):
    COCODataset(json_file, image_path, q=q).toVOC(target_dir, dataset_name)


if __name__ == '__main__':
    coco_datset = COCODataset("H:/testDataset/test/annotations/test.json", "H:/testDataset/test/images")
    coco_datset.toVOC("H:/testDataset/", "testVOC")
