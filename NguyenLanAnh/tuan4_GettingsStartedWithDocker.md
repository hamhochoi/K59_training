# Gettings started with Docker
## 1. Cài đăt Docker CE
Cài đặt Docker CE cho Ubuntu Xenial 16.04:
- Bước 1:
$ sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    software-properties-common
- Bước 2:
$ curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
$ sudo apt-key fingerprint 0EBFCD88
- Bước 3:
$ sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
- Bước 4:
$ sudo apt-get update
- Bước 5:
$ sudo apt-get install docker-ce





## 2. Phân biệt các lệnh
- docker run: Lệnh khởi động và đồng thời tạo mới 1 container
- docker start: Lệnh khởi động lại một container đã tồn tại
- docker stop: Lệnh dừng một container đang hoạt động
- docker rm: Lệnh xóa container đã dừng
- docker rmi: Lệnh xóa image

## 3. Demo với mysql
### Kéo image về:

        $ docker pull mysql // kéo image từ Docker hub về
        Hoặc:
        $ docker run // vừa kéo image còn thiếu về đồng thời tạo luôn container mới.

### Tạo container mysql server mới:

        $ docker run -it -d --name demo1 -v ~/data/mysql/:/var/lib/mysql -e MYSQL_ROOT_PASSWORD=password mysql:latest
         trong đó:
         -i : truy cập vào terminal
         -t : hiển thị kết quả lệnh
         -d : giữ container chạy
         --name: tên container
         -e: biến môi trường
demo:
![anh1](http://i.imgur.com/4JkiSb1.png)

### Truy cập vào mysql server container:

        $ docker exec -it demo1 mysql -uroot -p

![anh2](http://i.imgur.com/FjZqnGz.png)

Tạo DB ở container:

![anh21](http://i.imgur.com/JeBSgg3.png)

### Cài đặt mysql client:

        $ sudo apt-get install mysql-client //cài đặt client
        $ mysql -uroot -p student -h 172.17.0.2 -P 3306
        //trong đó 172.17.0.2 là địa chỉ IP của container và được xác định bằng câu lệnh docker inspect ID_container



![hinh3](http://i.imgur.com/q9dwois.png)

![hinh4](http://i.imgur.com/REr6Fiv.png)

end
