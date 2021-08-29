# CuGo
## cameraまわりのinstall  
```shell
sudo apt-get install ros-melodic-uvc-camera  
sudo apt-get install ros-melodic-image-*  
```
## joystickまわりのinstall  
```shell
sudo apt-get install joystick
```
# 実行方法
ラズパイにリモート接続
```bash
ssh ubuntu@raspi.local  
```
```  
source ~/.bashrc  
roslaunch cubase cubase.launch  
```