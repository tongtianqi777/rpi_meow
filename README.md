# Raspberry Pi Meow
For Zoey & Jake
--TNP

## Setup
```shell
pip3 install opencv-python
sudo apt-get install libcblas-dev
sudo apt-get install libhdf5-dev
sudo apt-get install libhdf5-serial-dev
sudo apt-get install libatlas-base-dev
sudo apt-get install libjasper-dev
sudo apt-get install libqtgui4
sudo apt-get install libqt4-test
```

## Deployment
```shell
# activate the right Python env
source ~/tflite/bin/activate
python3 -m venv ~/tflite/

# run these in separate processes
python detect.py
python api.py
```
