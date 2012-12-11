#! /bin/sh

sudo sh -c 'echo "deb-src http://archive.raspbian.org/raspbian wheezy main contrib non-free rpi" >> /etc/apt/sources.list'

sudo apt-get update

sudo apt-get upgrade

wget https://puredata.info/downloads/pd-extended-0-43-3-on-raspberry-pi-raspbian-wheezy-armhf/releases/1.0/Pd-0.43.3-extended-20121004.deb

sudo dpkg -i Pd-0.43.3-extended-20121004.deb

sudo apt-get -f install

sudo chmod 4755 /usr/bin/pd-extended 

sudo apt-get install python-pip vim emacs byobu ipython

sudo cp rpi_setup/pdsend /usr/local/bin

sudo cp rpi_setup/pdreceive /usr/local/bin

echo "alias pd='/usr/lib/pd-extended/bin/pd'" >> /.bashrc

sudo modprobe snd-bcm2835

sudo amixer cset numid=3 1

