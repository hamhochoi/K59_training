# Bắt đầu với Docker


## Phân biệt các lệnh

- `docker run` : cho phép tạo ra một container mới và chạy các lệnh. Đầu tiên thì tìm file trên local nếu không có sẽ tìm trên HUB và tải về để chạy nó. Docker chỉ tải lại khi mã nguồn của Image thay đổi
~~~
	docker run [OPTIONS] IMAGE [COMMAND] [ARG...]
~~~

- `docker start`: khởi động một container đã được tạo trước nhưng đang bị ngừng

~~~
	docker stats [OPTIONS] [CONTAINER...]
~~~

- `docker stop`: tạm dừng một container đang chạy 

~~~
	docker stop [OPTIONS] CONTAINER [CONTAINER...]
~~~

- `docker rm`: xóa một hay nhiều container 

~~~
	docker rm [OPTIONS] CONTAINER [CONTAINER...]
~~~

## MySQL container

### Tạo một MySQL Server Instance 

Chạy lệnh:
~~~
	sudo docker run --name test-mySql-image -e MYSQL_ROOT_PASSWORD=hihi -d mysql:latest
~~~

Trong đó: 

- `docker run`: là câu lệnh để chạy một image và tạo ra một container

- `--name test-mySql-image`: là đặt tên cho container là test-mySql-image

- `-e MYSQL_ROOT_PASSWORD=hihi`: tham số -e là thể hiện chúng ta đang set biến môi trường và ở đây là password đặt là hihi

- `-d` : cho phép container chạy backgroud và in ra container ID

- `mysql:latest`: tên image và phiên bản sẽ chạy 


Kết quả :
~~~
haiquan@myubuntu:~/Documents/testMySQL$ sudo docker run --name test-mySql-image -e MYSQL_ROOT_PASSWORD=hihi -d mysql:latest
Unable to find image 'mysql:latest' locally
latest: Pulling from library/mysql
cd0a524342ef: Pull complete 
d9c95f06c17e: Pull complete 
46b2d578f59a: Pull complete 
10fbc2bcc6e9: Pull complete 
91b1a29c3956: Pull complete 
5bf9316bd602: Pull complete 
69bd23f08b55: Pull complete 
4fb778132e94: Pull complete 
6913628d7744: Pull complete 
a477f36dc2e0: Pull complete 
c954124ae935: Pull complete 
Digest: sha256:e44b9a3ae88db013a3e8571a89998678ba44676ed4ae9f54714fd31e108f8b58
Status: Downloaded newer image for mysql:latest
4349ba97c2f53e44d09480f33f60f6275f415d33f1e94803ab89a425e0453505

~~~


Do trong máy chưa có image mysql nên docker sẽ tiến hành download image về và chạy 

### Chạy lệnh trong mysql container

Docker cho phép chúng ta truy nhập vào Mysql Command Line để thực hiện các câu lệnh SQL. Để thực hiện điều này ta sử dụng lệnh để vào bash shell trong mysql container

~~~
	sudo docker exec -it test-mySql-image bash
~~~

Sau đó sử dụng lệnh

~~~
	mysql -u root -p
~~~
 
Ở đây root chính là user bạn muốn sử dụng. Nhập password tương ứng với tài khoản ta được kết quả :

~~~
haiquan@myubuntu:~/Documents/testMySQL$ sudo docker exec -it test-mySql-image bash
root@4349ba97c2f5:/# mysql -u root -p 
Enter password: 
Welcome to the MySQL monitor.  Commands end with ; or \g.
Your MySQL connection id is 5
Server version: 5.7.18 MySQL Community Server (GPL)

Copyright (c) 2000, 2017, Oracle and/or its affiliates. All rights reserved.

Oracle is a registered trademark of Oracle Corporation and/or its
affiliates. Other names may be trademarks of their respective
owners.

Type 'help;' or '\h' for help. Type '\c' to clear the current input statement.


~~~


Từ bây giờ ta có thể sử dụng các câu lệnh SQL để thao tác

~~~

mysql> CREATE DATABASE dockerSQL;
Query OK, 1 row affected (0.05 sec)

mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| dockerSQL          |
| mysql              |
| performance_schema |
| sys                |
+--------------------+
5 rows in set (0.00 sec)


mysql> INSERT INTO Hpcc 
    -> VALUES (30,'BKHN');
Query OK, 1 row affected (0.11 sec)


mysql> SELECT * FROM Hpcc;
+---------+--------+
| SoNguoi | DiaChi |
+---------+--------+
|      30 | BKHN   |
+---------+--------+
1 row in set (0.00 sec)


~~~


### Kết nối đến MySQL Server Instance 

Đầu tiên phải lấy địa chỉ của container chạy mySQL bằng lệnh:
~~~
	sudo docker inspect test-mySql-image
~~~

Lệnh này trả về các thông tin về container. Ta tìm đến mục IPAddress và copy địa chỉ để đưa vào phần kết nối trong MySQL Workbench.





