# CoLabel  Version0.1.0
## Quick Start

- for Windows
```bash
################################################
# full label tool
################################################
pip install -r requirements.txt
python colabel.py


################################################
# provide service only
################################################
pip install flask requests lxml
# params                   host   |  port  |    user    | password | dataset root path 
# default                0.0.0.0  | 12345  |   admin    |   admin  |    ./images
python image_server.py -ip 0.0.0.0 -p 12345 -u username -k password -r ./images
```

- for Linux
```bash
################################################
# full label tool
################################################
pip3 install -r requirements.txt
python3 colabel.py


################################################
# provide service only
################################################
pip3 install flask requests lxml
python3 image_server.py -ip 0.0.0.0 -p 12345 -u username -k password -r ./images
```
