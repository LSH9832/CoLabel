import image_server
from multiprocessing import Process, freeze_support


freeze_support()


def back_run(user="admin", password="admin", root_path="./images", **kwargs):
    image_server.ROOTPATH.set(root_path)
    image_server.UserPwd.set(user, password)
    image_server.app.run(**kwargs)


def back_process(user="admin", password="admin", host="0.0.0.0", port=12345, root_path="./images", **kwargs):
    data = {
        "host": host,
        "port": port
    }
    for key in kwargs:
        data[key] = kwargs[key]
    return Process(target=back_run, args=(user, password, root_path), kwargs=data)


if __name__ == '__main__':
    import time
    process = back_process(user="admin01", port=13579)

    process.start()
    time.sleep(30)
    process.terminate()

