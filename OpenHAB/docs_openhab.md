## DOCS Cài openhab
- Tải docker image: docker pull openhab/openhab bản 2.3.0
- chạy lệnh docker run:

```
docker run \
        --name openhab \
        --net=host \
        -v /etc/localtime:/etc/localtime:ro \
        -v /etc/timezone:/etc/timezone:ro \
        -v openhab_addons:/openhab/addons \
        -v openhab_conf:/openhab/conf \
        -v openhab_userdata:/openhab/userdata \
        -d \
        --restart=always \
        openhab/openhab:2.3.0-amd64-debian
```
- Lưu ý: chạy trên pi thì phải tải docker image tương ứng là cấu trúc tập lệnh armhf thay vì amd 
- chạy lệnh sau trên terminal: 

```
sudo useradd -r -s /sbin/nologin openhab
usermod -a -G openhab <user>
mkdir /opt/openhab
mkdir /opt/openhab/conf
mkdir /opt/openhab/userdata
mkdir /opt/openhab/addons
chown -R openhab:openhab /opt/openhab
```

