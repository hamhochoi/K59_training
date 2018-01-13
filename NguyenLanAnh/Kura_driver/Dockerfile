FROM ubuntu
MAINTAINER Lananh
## build a image 
## sudo docker build -t [ten] .
## run a container 
## sudo docker run --name [ten_container] -p 80:80 -i -t [ten_image]

RUN apt-get update
## install software packages 
RUN apt-get install -y apt-utils unzip ethtool dos2unix telnet bind9 hostapd isc-dhcp-server iw monit wget openjdk-8-jdk  wireless-tools
## install Kura 
RUN wget http://ftp.daumkakao.com/eclipse/kura/releases/3.0.0/kura_3.0.0_raspberry-pi-2-3_installer.deb
RUN dpkg -i kura_3.0.0_raspberry-pi-2-3_installer.deb
EXPOSE 80
EXPOSE 5002
EXPOSE 1450
CMD service kura start while true