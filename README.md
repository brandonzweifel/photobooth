# Installation

## Install PI3D

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install python-dev python-setuptools libjpeg-dev zlib1g-dev libpng12-dev libfreetype6-dev
sudo apt-get install python-pip
sudo pip install pi3d
sudo pip install Pillow
sudo raspi-config # set gpu_mem=128
```

## Install The Printer

Install CUPS and add the printer usingt his great tutorial,

http://www.howtogeek.com/169679/how-to-add-a-printer-to-your-raspberry-pi-or-other-linux-computer/

Set your printer to be the default,

```
# List printers
lpstat -p -d

# Set Default
lpoptions -d HP_Photosmart_C4400_series
```