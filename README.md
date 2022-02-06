# Raspberry Pi Meow
For Zoey & Jake
--TNP

## Python Env
```shell
# you should do these before you do anything
# activate the right Python env
source ~/tflite/bin/activate
python3 -m venv ~/tflite/
```

## Setup
```shell
# Install Redis as in-mem cache
wget http://download.redis.io/releases/redis-6.0.6.tar.gz
tar xzf redis-6.0.6.tar.gz
cd redis-6.0.6
make

cd src
./redis-server
```

```shell
# Python packages
pip install redis
pip install opencv-python
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
# run these in separate processes
python detect.py
python api.py
```
