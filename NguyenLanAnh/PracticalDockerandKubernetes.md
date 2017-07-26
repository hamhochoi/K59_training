# [16/07-22/07] Practical Docker and Kubernetes
### 1. cài đặt Kubernetes
B1: clone repo từ github

B2: Máy được chọn làm master chạy file master.sh

B3: Các máy workers có thể là máy vật lí/máy ảo, export địa chỉ IP của máy master, sau đó chạy file worker.sh

### 2. Triển khai MQTT broker
Cài đặt kubectl chế độ dòng lệnh để làm việc với các cụm Kubernetes dễ dàng hơn.

Trước hết cần cấu hình cho hệ thống sử dụng configmap. Cụ thể, sử dụng câu lệnh:

     kubectl create configmap [ten-configmap] --namespace=[ten-namespace] --from-file=[key]=[path]



Sau khi đã cấu hình xong,với kết quả "configmap created", có thể tạo pod, sử dụng câu lệnh:

     kubectl create -f [file yaml]

Với MQTT broker, tạo configmap cho limit-queue.conf, rồi tạo pod.

![mqtt](http://imageshack.com/a/img923/7688/fux1p0.png)

### 3. Triển khai openHab và M2M

#### openHAB
Cũng tương tự như với MQTT broker.
Tạo configmap cho 2 file openhab.1.cfg và demo.1.items, sau đó tạo pod

![openhub](http://imageshack.com/a/img924/9207/LA17Ju.png)

![openhub1](http://imageshack.com/a/img923/7999/rIDHSk.png)

#### M2M
Tạo configmap cho 2 file config.1.cfg và items.1.cfg , sau đó tạo pod.
Bên cạnh đó, sử dụng các câu lệnh:

     kubectl get nodes//thông tin về nodes
     kubectl get pod//thông tin về pod
     kubectl describe configmaps [tên-configmap]//để xem thông tin config

### end.
