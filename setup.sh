#! /bin/sh

sh -c 'echo "deb-src http://archive.raspbian.org/raspbian wheezy main contrib non-free rpi" >> /etc/apt/sources.list'

apt-get update

apt-get upgrade

wget https://puredata.info/downloads/pd-extended-0-43-3-on-raspberry-pi-raspbian-wheezy-armhf/releases/1.0/Pd-0.43.3-extended-20121004.deb

dpkg -i Pd-0.43.3-extended-20121004.deb

apt-get -f install

chmod 4755 /usr/bin/pd-extended 

apt-get install python-pip vim emacs byobu ipython

cp rpi_setup/pdsend /usr/local/bin

cp rpi_setup/pdreceive /usr/local/bin

"alias pd='/usr/lib/pd-extended/bin/pd'" >> /.bashrc

modprobe snd-bcm2835

amixer cset numid=3 1

