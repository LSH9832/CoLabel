import json
import datetime
import os
from glob import glob, iglob
import shutil
from time import sleep
from threading import Thread


def get_file_list(image_dirs, annotation_dirs, image_type="jpg"):
    if isinstance(image_dirs, str):
        image_dirs = [image_dirs]
    if isinstance(annotation_dirs, str):
        annotation_dirs = [annotation_dirs]

    image_name_list = []
    anno_name_list = []

    for image_dir in image_dirs:
        for image_name in iglob("%s/*.%s" % (image_dir, image_type)):
            image_name = image_name.replace("\\", "/")
            image_name_list.append(image_name)

    for anno_dir in annotation_dirs:
        for anno_name in sorted(glob("%s/*.xml" % anno_dir)):
            anno_name = anno_name.replace("\\", "/")
            anno_name_list.append(anno_name)

    return image_name_list, anno_name_list


class XML:
    string = ""

    def __init__(self, string: str):
        self.string = string

    def __repr__(self):
        return self.string

    def __getitem__(self, item):
        return self.string[item]

    def find(self, patten):
        """
        get string in keyword patten
        :param patten: string
        :return: string in between (XML)
        """
        results = []
        start = "<%s>" % patten
        end = "</%s>" % patten
        now_index = 0
        while now_index < len(self.string) - len(start) - len(end):
            if self.string[now_index:].startswith(start):
                flag = 1
                n_i = now_index + len(start)
                while n_i < len(self.string) - len(start):
                    if self.string[n_i:].startswith(start):
                        flag += 1
                    elif self.string[n_i:].startswith(end):
                        flag -= 1
                        if flag == 0:
                            # print(now_index + len(start), n_i-1)
                            results.append(XML(string=self.string[now_index + len(start):n_i]))
                            break
                    n_i += 1
            now_index += 1
        return results


def decode_VOC(fp):
    """
    get key infomation of annotation of VOC format
    :param fp: xml file
    :return: information data (dict)
    """
    if isinstance(fp, str):
        assert os.path.exists(fp)
        fp = open(fp)

    my_xml = XML(fp.read())

    objects = my_xml.find("object")
    w, h = int(my_xml.find("width")[0][:]), int(my_xml.find("height")[0][:])
    bboxes = []
    for this_obj in objects:
        bbox = this_obj.find("bndbox")[0]
        msg = {
            "class": this_obj.find("name")[0][:],
            "loc": [int(bbox.find("xmin")[0][:]), int(bbox.find("ymin")[0][:]),
                    int(bbox.find("xmax")[0][:]), int(bbox.find("ymax")[0][:])],
            "difficult": bool(int(this_obj.find("difficult")[0][:]))
        }
        bboxes.append(msg)
    data = {
        "width": w,
        "height": h,
        "bboxes": bboxes
    }
    return data


class COCO:

    def __init__(self, fp=None):
        """
        :param fp: json file
        """
        self.info = {
            'description': "UnNamed",
            'url': "",
            'version': "1.0",
            'year': datetime.datetime.now().year,
            'contributor': "UnNamed",
            'date_created': '%s/%s/%s' % (str(datetime.datetime.now().year),
                                          str(datetime.datetime.now().month).zfill(2),
                                          str(datetime.datetime.now().day).zfill(2))
        }
        self.lic = []
        self.images = []
        self.annotations = []
        self.categories = []
        self.categorie_num = {}

        if isinstance(fp, str):
            assert os.path.exists(fp)
            fp = open(fp)
        self.load(fp)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        del self.lic
        del self.images
        del self.annotations
        del self.categories
        del self.categorie_num
        return False

    def son_of(self, coco_parent, name="son"):
        """
        Copy messages from parent coco dataset without images and annotations
        :param coco_parent: parent coco dataset
        :param name: name of this dataset, /train/val/test
        """
        self.info = coco_parent.get_info()
        # print(parent.get_info())

        self.info["description"] += "_%s" % name
        self.lic = coco_parent.get_license()
        self.categories = coco_parent.get_categories()
        self.categorie_num = {idx: 0 for idx in coco_parent.get_category_num()}
        # print(coco_parent.get_category_num())

    def get_info(self):
        return self.info.copy()

    def get_license(self):
        return self.lic.copy()

    def get_images(self):
        return self.images

    def get_categories(self):
        return self.categories.copy()

    def get_category_num(self):
        return self.categorie_num.copy()

    def _count_category_num(self):
        """
        count and update number of each category
        """
        # print("counting categories")
        self.categorie_num = {}
        for anno in self.annotations:
            if anno['category_id'] - 1 in self.categorie_num:
                self.categorie_num[anno['category_id'] - 1] += 1
            else:
                self.categorie_num[anno['category_id'] - 1] = 1

    def _image_id_exists(self, image_id):
        """
        whether this image id exists
        :param image_id: image id
        """
        flag = False
        for image in self.images:
            if image["id"] == image_id:
                flag = True
                break
        return flag

    def _get_image_data_by_id(self, image_id):
        """
        get image data by its id
        :param image_id:
        :return: image data(dict)
        """
        for image in self.images:
            if image["id"] == image_id:
                return image
        return None

    def _get_category_id_by_name(self, name, add_mode=True):
        """
        get category id by its name
        :param name: category name
        :return: category id(int)
        """
        for this_category in self.categories:
            if this_category['name'] == name:
                return this_category["id"]
        if add_mode:
            self.add_category(name)
            return self._get_category_id_by_name(name, False)
        else:
            assert add_mode, "category %s not Found" % name

    def _get_name_by_category_id(self, cid):
        for c in self.categories:
            if c["id"] == cid:
                return c["name"]
        return None

    def total_image_number(self):
        return len(self.images)

    def total_annotation_number(self):
        # TODO
        return len(self.annotations)

    def load(self, fp):
        """
        load data from json file
        :param fp: file
        """

        if fp is not None:
            from time import time
            print("loading json...")
            t0 = time()
            data = json.load(fp)
            print("loading time: %.2fs" % (time()-t0))
            self.info = data["info"]
            self.lic = data["licenses"]
            self.images = data["images"]
            self.annotations = data["annotations"]
            self.categories = data["categories"]
            self._count_category_num()

    def change_info(self, data_name, version="1.0", url="", author=""):
        """
        change information of this dataset
        :param data_name: name of this dataset
        :param version: version of this dataset
        :param url: url link of this dataset
        :param author: author of this dataset
        """
        self.info = {
            'description': data_name,
            'url': url,
            'version': version,
            'year': datetime.datetime.now().year,
            'contributor': author,
            'date_created': '%s/%s/%s' % (str(datetime.datetime.now().year),
                                          str(datetime.datetime.now().month).zfill(2),
                                          str(datetime.datetime.now().day).zfill(2))
        }

    def add_license(self, name, url=""):
        """
        add license of this dataset
        :param name: name of this license
        :param url: url link of this license
        """
        self.lic.append({
            'url': url,
            'id': len(self.lic) + 1,
            'name': name
        })

    def add_category(self, name, supercategory=None):
        """
        add category of this dataset
        :param name: category name
        :param supercategory: supercategory name
        """
        self.categories.append({
            'supercategory': supercategory,
            'id': len(self.categories) + 1,
            'name': name
        })
        self.categorie_num[len(self.categories) - 1] = 0

    def load_categories(self, txt_file_name):
        """
        load category from txt file
        :param txt_file_name: file name
        """
        if txt_file_name is not None:
            with open(txt_file_name) as fp:
                classes = fp.read().split("\n")
                for this_class in classes:
                    if len(this_class):
                        this_class = this_class.split(":")
                        self.add_category(name=this_class[0], supercategory=this_class[-1])
        self.categorie_num = {}

    def add_image(
            self,
            image_id,
            file_name,
            width,
            height,
            date_captured=None,
            license_id=1,
            url="",
            flickr_url=None
    ):
        """
        add image data to this dataset
        :param image_id: image id
        :param file_name: file name e.g: 00001.jpg
        :param width: image width
        :param height: image height
        :param date_captured: e.g 2022-02-22 22:22:22
        :param license_id: license id
        :param url: image url
        :param flickr_url: image flickr url
        """
        assert not self._image_id_exists(image_id), "Image ID %d already exists!" % image_id
        self.images.append({
            'license': license_id,
            'file_name': file_name,
            'coco_url': url,
            'height': height,
            'width': width,
            'date_captured': str(datetime.datetime.now()).split(".")[0] if date_captured is None else date_captured,
            'flickr_url': url if flickr_url is None else flickr_url,
            'id': image_id
        })

    def add_annotation(
            self,
            image_id,
            anno_id,
            category_id,
            bbox=None,
            segmentation=None,
            area=None,
            iscrowd=0
    ):
        """
        add annotation of any image exists in this dataset
        :param image_id: image id
        :param anno_id: annotation id
        :param category_id: category id
        :param bbox: bounding box [xmin, ymin, w, h]
        :param segmentation: segmentation [[x00, y00, x01, y01, ....], [x10, y10, x11, y11, ....], ....]
        :param area: area of segmentation if segmentation is not empty else area of bounding box
        :param iscrowd: is crowd
        """
        assert bbox or segmentation, "bbox or segmentation is required"
        assert self._image_id_exists(image_id), "Image ID %d does not exist!" % image_id

        if bbox is None:
            bbox = []
        if segmentation is None:
            segmentation = []
        if area is None and len(bbox):
            area = bbox[2] * bbox[3]

        self.annotations.append({
            'segmentation': segmentation,
            'area': area,
            'iscrowd': iscrowd,
            'image_id': image_id,
            'bbox': bbox,
            'category_id': category_id,
            'id': anno_id
        })
        if category_id - 1 in self.categorie_num:
            self.categorie_num[category_id - 1] += 1
        else:
            self.categorie_num[category_id - 1] = 1

    def save(self, file_name: str = None):
        """
        save data to a json file
        :param file_name: file name with path
        """
        file_name = self.info["description"] if file_name is None else file_name
        file_name = file_name if file_name.endswith(".json") else "%s.json" % file_name
        json.dump({
            'info': self.info,
            'licenses': self.lic,
            'images': self.images,
            'annotations': self.annotations,
            'categories': self.categories
        }, open(file_name, "w"))
        print("coco annotation saved to %s." % os.path.abspath(file_name).replace("\\", "/"))

    def show_each_category_num(self, width=50, simple=False):
        """
        show number of each category in a table
        :param width: tabel width
        :param simple: show simple table
        """
        if simple:
            categories_str = ""
            for cate in self.categories:
                categories_str += cate["name"].ljust(width//3 * 2) + \
                                  str(self.categorie_num[cate["id"] - 1]
                                      if (cate["id"] - 1) in self.categorie_num else 0).rjust(width - width//3*2) + "\n"
            return f"""
{"=" * width}
Category Count
{"%s images" % str(len(self.images)).rjust(10)}
{"%s annotations" % str(len(self.annotations)).rjust(10)}
{"=" * width}
{categories_str}{"=" * width}"""
        width = max(28, int(width))
        head = "╒%s╕\n" \
               "│%sCategory Count%s│\n" \
               "╞%s╡\n" % ("═" * width, " " * int((width - 14) / 2), " " * int((width - 14) / 2), "═" * width)
        msg = ""
        msgs = ["%s images" % str(len(self.images)).rjust(10),
                "%s annotations" % str(len(self.annotations)).rjust(10)]
        for this_msg in msgs:
            msg += "│%s│\n" % this_msg.ljust(width)

        neck = "╞%s╤%s╡\n" % ("═" * (width - 1 - int(width / 3)), "═" * int(width / 3))



        body = ""
        for cate in self.categories:
            body += "│%s│%s│\n" % (
                cate["name"].ljust(width - 1 - int(width / 3)),
                str(self.categorie_num[cate["id"] - 1] if (cate["id"] - 1) in self.categorie_num else 0).rjust(int(width / 3))
            )
            # print("│%s│%s│" % (
            #     cate["name"].ljust(width - 1 - int(width / 3)),
            #     str(self.categorie_num[cate["id"] - 1] if (cate["id"] - 1) in self.categorie_num else 0).rjust(int(width / 3))
            # ))

            if self.categories.index(cate) < len(self.categories) - 1:
                body += "├%s┼%s┤\n" % ("─" * (width - 1 - int(width / 3)), "─" * int(width / 3))
                # print("├%s┼%s┤" % ("─" * (width - 1 - int(width / 3)), "─" * int(width / 3)))
            else:
                body += "╘%s╧%s╛" % ("═" * (width - 1 - int(width / 3)), "═" * int(width / 3))
                # print("╘%s╧%s╛" % ("═" * (width - 1 - int(width / 3)), "═" * int(width / 3)))

        show_str = head + msg + neck + body
        print()
        print(show_str)
        print()

        return show_str


def voc2coco(image_dirs,
             annotation_dirs,
             class_file=None,
             data_name=None,
             image_target_dir: str = None,
             image_type="jpg",
             version="1.0",
             url="",
             author="",
             save=True,
             coco_dataset: COCO = None,
             q=None) -> COCO:

    assert image_target_dir is not None, "IMAGE TARGET DIR should not be None!"

    image_name_list, anno_name_list = get_file_list(image_dirs, annotation_dirs, image_type)

    if coco_dataset is None:
        coco_dataset = COCO()
        coco_dataset.change_info(data_name=data_name, version=version, url=url, author=author)
        coco_dataset.add_license(name="FAKE LICENSE", url="")
        coco_dataset.load_categories(txt_file_name=class_file)

    start = coco_dataset.total_image_number()
    anno_id = coco_dataset.total_annotation_number()
    # start = image_id
    minous = 0
    anno_file_num = len(anno_name_list)
    max_num = 1000

    def one_thread(index, total):
        nonlocal anno_id, minous, coco_dataset

        for i, anno_name in enumerate(anno_name_list):

            if not i % total == index:
                continue

            if q is not None:
                if q.empty() or i + 1 == anno_file_num:
                    q.put(int(float(i)/float(anno_file_num) * max_num))

            image_name = "%s.%s" % (anno_name.split("/")[-1].split(".")[0], image_type)
            image_match = [image_path.endswith(image_name) for image_path in image_name_list]
            if any(image_match):
                image_id = start + i + 1 - minous
                image_path = image_name_list[image_match.index(True)]
                image_name = str(image_id).zfill(10) + ".%s" % image_type
                shutil.copyfile(image_path, os.path.join(image_target_dir, image_name))

                print("\rConverting: %d / %d" % (image_id, anno_file_num + start), end="")

                anno_data = decode_VOC(anno_name)
                coco_dataset.add_image(
                    image_id=image_id,
                    file_name=image_name,
                    width=anno_data["width"],
                    height=anno_data["height"]
                )
                for anno in anno_data["bboxes"]:
                    anno_id += 1
                    bbox = anno["loc"]
                    coco_dataset.add_annotation(
                        image_id=image_id,
                        anno_id=anno_id,
                        category_id=coco_dataset._get_category_id_by_name(anno["class"]),
                        bbox=[bbox[0], bbox[1], bbox[2] - bbox[0], bbox[3] - bbox[1]],
                        iscrowd=int(anno["difficult"])
                    )
            else:
                minous += 1

    num_threads = os.cpu_count()
    threads = [Thread(target=one_thread, args=(i, num_threads)) for i in range(num_threads)]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

    print("\nConvert finished. Images saved to %s" % image_target_dir.replace("\\", "/"))
    coco_dataset.save(data_name) if save else None

    if q is not None:
        q.put(max_num)
        sleep(0.04)
        try:
            json_path = q.get(timeout=1)
            coco_dataset.save(json_path)
            dir_name = os.path.dirname(json_path)

            json_log = os.path.join(dir_name, "category_msg.txt")
            with open(json_log, "w") as f:
                f.write(coco_dataset.show_each_category_num())
            label_file = os.path.join(dir_name, "classes.txt")
            label_str = ""
            for label in coco_dataset.get_categories():
                label_str += f"{label['name']}\n"
            with open(label_file, "w") as f:
                f.write(label_str[:-1])
            q.put(coco_dataset.show_each_category_num(35, True))
        except:
            pass

    return coco_dataset


def divide_coco_by_image(coco_dataset: COCO, train: float, val: float, save=True):
    assert 0. < train < 1. and 0. < val < 1. and 0. < train + val <= 1.

    import random

    datasets = {
        "train": COCO(),
        "val": COCO(),
        "test": COCO()
    }
    for item in datasets:
        datasets[item].son_of(coco_dataset, name=item)

    image_map = [i for i in range(len(coco_dataset.images))]
    random.shuffle(image_map)
    train_img_num = round(len(coco_dataset.images) * train)
    val_img_num = round(len(coco_dataset.images) * val)

    for anno in coco_dataset.annotations:
        # anno['image_id']
        img_id = anno['image_id'] - 1
        this_rank = image_map.index(img_id)

        kw = "test"
        if this_rank < train_img_num:
            kw = "train"
        elif this_rank < train_img_num + val_img_num:
            kw = "val"

        datasets[kw].annotations.append(anno)
        if not datasets[kw]._image_id_exists(anno['image_id']):
            datasets[kw].images.append(coco_dataset._get_image_data_by_id(anno['image_id']))

    [datasets[item]._count_category_num() and
     (datasets[item].save(file_name=datasets[item].info["description"]) if save else None)
     for item in datasets]

    return datasets


def divide_COCO_by_annotation(coco_dataset: COCO, train: float, val: float, save=True):
    assert 0. < train < 1. and 0. < val < 1. and 0. < train + val <= 1.

    import random

    datasets = {
        "train": COCO(),
        "val": COCO(),
        "test": COCO()
    }
    for item in datasets:
        datasets[item].son_of(coco_dataset, name=item)
    anno_map = []
    # coco_dataset._count_category_num()

    for num in coco_dataset.categorie_num:
        cate_map = [(i + 1) for i in range(num)]
        random.shuffle(cate_map)
        anno_map.append(cate_map)
    train_cate_num = [round(num * train) for num in coco_dataset.categorie_num]
    val_cate_num = [round(num * val) for num in coco_dataset.categorie_num]

    count_num = [0 for _ in coco_dataset.categorie_num]

    for anno in coco_dataset.annotations:
        cate_id = anno['category_id'] - 1
        count_num[cate_id] += 1
        this_rank = anno_map[cate_id].index(count_num[cate_id])

        kw = "test"
        if this_rank < train_cate_num[cate_id]:
            kw = "train"
        elif this_rank < train_cate_num[cate_id] + val_cate_num[cate_id]:
            kw = "val"

        datasets[kw].annotations.append(anno)
        datasets[kw].categorie_num[cate_id] += 1
        if not datasets[kw]._image_id_exists(anno['image_id']):
            datasets[kw].images.append(coco_dataset._get_image_data_by_id(anno['image_id']))

    if save:
        for item in datasets:
            datasets[item].save(file_name=datasets[item].info["description"])
    return datasets


def convert_only(image_dirs,
                 annotation_dirs,
                 image_type,
                 data_name,
                 coco_image_dir,
                 coco_annotation_dir,
                 class_file,
                 json_file,
                 coco_dataset: COCO=None,
                 **_):
    # convert and divide
    os.makedirs(coco_image_dir, exist_ok=True)
    os.makedirs(coco_annotation_dir, exist_ok=True)

    coco_data = voc2coco(
        image_dirs=image_dirs,
        annotation_dirs=annotation_dirs,
        image_target_dir=coco_image_dir,
        class_file=class_file,
        image_type=image_type,
        data_name=data_name,
        save=False,
        coco_dataset=coco_dataset
    )
    coco_data.save(json_file)
    return coco_data


def divide_only(json_file, train, val, **_):
    print("\nDividing data into train/val/test dataset\n")

    coco_dataset = COCO(json_file)
    all_dataset = divide_coco_by_image(coco_dataset, train, val, save=False)
    for item in all_dataset:
        this_dataset = all_dataset[item]

        print("\n" + "#" * 52)
        print(item, "dataset")

        this_dataset.show_each_category_num()
        this_dataset.save(os.path.join(os.path.dirname(json_file), this_dataset.info["description"]))


def convert_and_divide(convert=True, divide=True, **kwargs):
    c = convert_only(**kwargs) if convert else None
    del c
    divide_only(**kwargs) if divide else None


def main(root_dir, dist_dir: str, train, val, image_type="jpg", convert=True, divide=False):
    """settings"""
    # VOC
    image_dirs = [os.path.join(root_dir, "image")]
    annotation_dirs = [os.path.join(root_dir, "annotation")]

    # COCO
    data_name = dist_dir.replace("\\", "/").split("/")[-1]
    coco_image_dir = os.path.join(dist_dir, "images")
    coco_annotation_dir = os.path.join(dist_dir, "annotations")
    json_file = os.path.join(coco_annotation_dir, "%s.json" % data_name)
    class_file = "labels.txt"

    coco = None
    if os.path.exists(json_file):
        try:
            coco = COCO(json_file)
        except Exception as e:
            print(e)

    ###########################################################################
    """
    do not edit the following code unless you know what are you doing
    """

    settings = {
        "image_dirs": image_dirs,
        "annotation_dirs": annotation_dirs,
        "image_type": image_type,
        "data_name": data_name,
        "coco_image_dir": coco_image_dir,
        "coco_annotation_dir": coco_annotation_dir,
        "class_file": class_file,
        "json_file": json_file,
        "train": train,
        "val": val,
        "coco_dataset": coco,
    }

    convert_and_divide(convert, divide, **settings)


if __name__ == '__main__':
    main(
        root_dir="./voc2",
        dist_dir="./GUNS2022",
        train=0.8,
        val=0.2,
        image_type="jpg",
        convert=True,
        divide=True
    )
