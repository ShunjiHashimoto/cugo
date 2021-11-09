# 収穫サポートロボット
CuGo V3を使って収穫サポートロボットTANGを作る

## 必要な開発環境
- Rapberry Pi 4
- Ubuntu18.04が入ったPC
- Webカメラ
- CuGo V3 など

## 必要なパッケージ
### Ubuntu serverをダウンロードし、SDカードに書き込む
Ubuntu serverをダウンロード
```bash
wget http://cdimage.ubuntu.com/releases/bionic/release/ubuntu-18.04.5-preinstalled-server-arm64+raspi3.img.xz
```
ファイルを解凍
```bash
hashimoto@hashimoto:~/Downloads$ xz -dv ubuntu-18.04.5-preinstalled-server-arm64+raspi3.img.xz 
```
Raspberry Pi Imagerを使って書き込む
書き込むimgファイルは先程選択したファイルを選択後、書き込む
![Screenshot from 2021-10-08 07-17-44](https://user-images.githubusercontent.com/63869336/136469821-0b4fd0a0-74e5-464a-93dd-b196089ea772.png)


### Ubuntu
```bash
sudo apt update
sudo apt upgrade
sudo apt install xubuntu-desktop
```

### ROS
```bash
sudo sh -c 'echo "deb http://packages.ros.org/ros/ubuntu $(lsb_release -sc) main" > /etc/apt/sources.list.d/ros-latest.list'
sudo apt install curl # if you haven't already installed curl
curl -s https://raw.githubusercontent.com/ros/rosdistro/master/ros.asc | sudo apt-key add -
sudo apt update
sudo apt install ros-melodic-desktop-full
echo "source /opt/ros/melodic/setup.bash" >> ~/.bashrc
source ~/.bashrc
source /opt/ros/melodic/setup.bash
sudo apt install python-rosdep python-rosinstall python-rosinstall-generator python-wstool build-essential
sudo apt install python-rosdep
sudo rosdep init
rosdep update
```
参考：http://wiki.ros.org/melodic/Installation/Ubuntu

### camera
```bash
sudo apt-get install ros-melodic-uvc-camera  
sudo apt-get install ros-melodic-image-*  
```
### joystick
```bash
sudo apt-get install ros-melodic-joy
```
### Raspberry Pi 4
```bash
sudo apt-get install python-rpi.gpio
```

## 実行
### 収穫サポートを開始する
- ssh "ユーザ名"@"IPアドレス"   
例) ssh ubuntu@172.28.***.**  
- パスワード入力   
- source ~/.bashrc  
- roslaunch cugo_bringup cugo_bringup.launch  

### 赤色検出を行う
- ssh "ユーザ名"@"IPアドレス"  
例) ssh ubuntu@172.28.×××.××  
- パスワード入力  
- source ~/.bashrc  
- roslaunch cugo_detection cugo_detection

## License

本パッケージはApache License, Version 2.0に基づき公開されています。  
ライセンスの全文は[https://www.apache.org/licenses/LICENSE-2.0](https://www.apache.org/licenses/LICENSE-2.0)から確認できます。
