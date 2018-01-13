# Docker network and Kubernetes concept

## 1. Docker network

### Docker network là gì?

Docker network dùng để gắn địa chỉ IP cho các containers.

Phân loại Docker network

      - Default Networks
      - Users-defined Networks
### Default Network

Sau khi cài đặt Docker có 3 networks được tạo ra 1 cách tự động: brige, none, host. Có thể kiểm tra bằng câu lệnh:

      $docker network ls
- brige là loại network mà docker sẽ tự động truy cập container tới mạng này . Bridge như một phần của host's network stack( Sử dụng câu lệnh ifconfig để kiểm tra, bridge được thể hiện bằng docker0). Muốn thay đổi network mà container chạy trên đó khi run sử dụng cờ --network:

      $docker run --network=<tennetwork>
các container có thể giao tiếp với nhau qua network này qua :

      $docker run --link
- none: khi sử dụng none, container sẽ được đính kèm vào container-specific network stack.Khi mà 1 container đang chạy đính kèm vào network này thì nó có vai trò như 1 root, để xem network như thế nào trong 1 container. Container này thiếu network interface. Sử dụng câu lệnh sau để để đính kèm container vào network này:

      $docker attach <tên>
Sử dụng CTRL-p CTRL-q để detach mà container vẫn tiếp tục running.

- host: Sử dụng network này để thêm container vào host network stack.
      $docker network inspect //để lấy thông tin về network.

### User-defined networks

Tạo những networks kiểu này nhằm mục đích quản lí các containers liên kết với nhau, hoặc cho phép phân giải một cách tự động tên miền sang địa chỉ IP. Docker cung cấp drivers network để tạo những mạng này. Có thể tạo:

    -bridge network
    -overlay network
    -MACVLAN network
    -network plugin
    -remote network
- bridge network: Là lọai phổ biến nhất được sử dụng trong Docker. Tạo network bằng câu lệnh:

      $docker network create --driver bridge <ten>
      $docker run --network=<ten> //cho phép container run trong network đó.
Loại này sẽ hữu ích cho loại network nhỏ(single host), còn đối với network lớn sẽ sử dụng overlay.

- docker-gwbridge network: Là một local bridge network.Nó sẽ được tự động được tạo ra trong hai tình huống:

  -Khi tham gia một nhóm, Docker sử dụng network này cho việc giao tiếp giữa các node tại những host khác nhau.

  -Khi mà không 1 network nào của container cung cấp những truy cập ngoài mạng. Sử dụng network này để liên hệ với những network ngoài hoặc những nodes ở nhóm khác.
Nó luôn luôn xuất hiện khi sử dụng network overlay.

- overlay networks in swarm mode: network này sẽ có trên những nodes trong swarm mà không cần tới external key-value.
overlay networks without swarm mode: Nếu không ở chế độ swarm mode thì overlay network yêu cầu phải có một key-value store service.

   ![anh1](http://i.imgur.com/IN4HXZL.png)

  Mỗi host trong network phải run một Docker Engine instance. Cách dễ dàng nhất để tạo ra các host là sử dụng Docker Machine.

- custom network plugins: Sử dụng plugin của Docker để viết lên những network driver plugin. Nó sẽ chạy như 1 tiến trình tách biệt trên máy chủ. Những plugin này sẽ có những quy tắc, vòng đời: cài đặt, bắt đầu, hoạt động, dừng.
      $ docker network create --driver weave mynet
Embedded DNS server: Cung cấp hoạt động phân giải tên miền giữa các containers.

## 2. Calico, Flannel, Weave

Có 4 giải pháp khác nhau cho network: Calico, Flannel, Weave, Docker Overlay Network.


## 3. Kubernetes

### Kubernetes?

Kubernetes là 1 project opensource được phát triển bởi Google. Kubernetes phục vụ cho việc deploy, scale và operator các application container trên các cụm máy chủ dùng container app làm trung tâm.

Với Kubernetes:

- Deploy app một cách nhanh nhất.
- Hỗ trợ tự động scale app.
- Liên tục tích hợp các tính năng mới.
- Tối ưu hóa phần cứng (cho phép người dùng lựa chọn resource mà người đó cần).

### Kubernetes components:
Cơ bản, sẽ gồm có 2 thành phần chính cấu thành lên 1 kubernete là: Master components và node components. Và mỗi thành phần này cũng bao gồm nhiều thành phần nhỏ khác.
#### Master components
Thành phần master giữ nhiệm vụ điều khiển hoạt động của cả cụm, cụm này là các node được kết nối với nhau.
- kube-apiserver: Cung cấp Kubernetes API.
- etcd: Tất cả dữ liệu về cụm nodes được lưu trữ tại đây, như thông tin cài đặt các nodes,để khi mỗi node được đặt vào. trong pod nó sẽ được cấu hình theo dữ liệu trong etcd.
- kube-controller-manager: Điều phối các nhiệm vụ của cluster.
- cloud-controller-manager: Điều khiển tương tác với cloud.
- kube-scheduler: Lên kế hoạch tạo những pod mới, và xem xét để xếp những nodes thuộc những pod đó.
- addons: Là những thành phần được thêm vào để làm rõ hơn đặc tính của các cụm. Như: DNS.

#### Node components
- kubelet: Khởi động và duy trì pods.
- kube-proxy: Duy trì 1 cơ chế (role) để truy cập vào các nodes.
- docker: run các containers.
- rkt: run các containers thay thế cho docker(thí nghiệm).
- supervisord: Có chức năng duy trì kubelet và docker chạy.
- fluentd:


Dưới đây là hình ảnh về một vài thành phần cơ bản trong Kubernetes:

![anh2](http://i.imgur.com/6ijC4pg.png)

Trong đó:

- Pod: tập hợp các container lại, các container đã được schedule.
- Kuberlet: Khởi động, duy trì pod.
- Label: dạng key-value, định nghĩa đơn giản nhiệm vụ của các Pod.
- Proxy: cơ chế truy cập tới node.
- Master: nhận những thay đổi về cài đặt và triển khai.
- API server: cung cấp Kubernetes API. Đặt Pod vào node, đồng bộ hóa thông tin của Pod bằng REST API.
- etcd: lưu trữ liên kết cài đặt với node.

### Kubernetes resources
#### Compute resources:

Có 2 loại compute resource là CPU và memory.
Loại tài nguyên này đều có đơn vị cơ sở, như CPU có đơn vị cơ sở là core , memory có đơn vị cơ sơ là byte.

Loại tài nguyên này có thể đo đạt bằng các đơn vị cơ sở như trên, có thể được xác định hay yêu cầu cho phù hợp.

Và mỗi container sẽ có các resoures này. Các resoures này sẽ phải kèm theo 2 yếu tố là request và limit. Request sẽ giúp scheduler xác định node nào mới phú hợp để đặt pod vào. Còn limit giữ vai trò là một giới hạn dừng để chắc chắn các container không đòi hỏi tài nguyên quá lớn. Khi tài nguyên đã tăng lên quá giới hạn container có thể bị dừng.

#### API resources:
Nguồn tài nguyên chỉ có thể đọc và thay đổi thông qua API Kubernetes server.

Nguồn tài nguyên này sẽ đảm bảo cho các components giao tiếp được với nhau. Và chính loại resource này lại bị quản lí bởi API server.

Gồm:  

              API versioning
              API group
Bên cạnh đó còn có Opaque integer resource, xuất hiện tại Kubernetes version 1.5.












## 4. IOT platform
### IOT platform?
IOT platform như một middleware, cái sẽ có nhiệm vụ kết nối các phần như phần cứng, điểm thu, data network với các ứng dụng đầu cuối phía người dùng. Cụ thể, nó sẽ quản lí và ảo hóa dữ liệu rồi dữ liệu sau đó mới được trả về thiết bị người dùng.-> Giải quyết các vấn đề: Kết nối thiết bị, trích xuất dữ liệu từ lượng lớn các thiết bị thu nhận dữ liệu.
### Lợi ích có được từ 1 nền tảng IOT:
#### Có thể mở rộng:
Về số lượng thiết bị có thể nhận dữ liệu, về hiệu suất cân bằng tải.
#### Dễ sử dụng
#### Hợp tác với bên thứ 3
Bên thứ 3 này có thể là phần cứng hay phần mềm nhằm tăng tốc truyền tải hay kiểm tra sự chính xác của hệ thống.
#### Có những lựa chọn triển khai

#### An toàn dữ liệu
### 1 số IOT Platforms
IOT platform rất đa dạng. Có thể chia ra nhiều loại platform: Nền tảng cho các ngành công nghiệp, nền tảng tập trung vào các thiết bị,...
Có thể kể đến 1 số platform nổi trội:
- Microsoft Azure IoT
- IBM Watson
- Cisco IoT Cloud Connect
- Amazon web services IoT
- Google Cloud
