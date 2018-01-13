# Chạy Kubernetes bằng Kubeadm 


## Cài đặt Kubeadm 

Trước khi cài đặt kubeadm ta phải cài đặt `docker` Cách thức cài đặt docker trên rapsbian đã được đề cập trong bài viết trước. 

Sau đây là các bước cài đặt kubeadm:

~~~
sudo su -

curl -s https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key add -

echo "deb http://apt.kubernetes.io/ kubernetes-xenial main" > /etc/apt/sources.list.d/kubernetes.list

apt-get update && apt-get install -y kubeadm

~~~


## Các vấn đề khi chạy Kubernetes trên Raspbian 

### Vấn đề khi chạy `kubeadm init` trên Raspberry Pi 

Sau khi cài đặt xong `kubeadm` và `docker` ta sử dụng lệnh `kubeadm init --pod-network-cidr 10.244.0.0/16` để chạy thử một node master trên Pi 3. Có thể sẽ gặp lỗi sau: 

~~~
[kubeadm] WARNING: kubeadm is in beta, please do not use it for production clusters.
[init] Using Kubernetes version: v1.7.4
[init] Using Authorization modes: [Node RBAC]
[preflight] Running pre-flight checks
[preflight] The system verification failed. Printing the output from the verification:
OS: Linux
KERNEL_VERSION: 4.9.35-v7+
CONFIG_NAMESPACES: enabled
CONFIG_NET_NS: enabled
CONFIG_PID_NS: enabled
CONFIG_IPC_NS: enabled
CONFIG_UTS_NS: enabled
CONFIG_CGROUPS: enabled
CONFIG_CGROUP_CPUACCT: enabled
CONFIG_CGROUP_DEVICE: enabled
CONFIG_CGROUP_FREEZER: enabled
CONFIG_CGROUP_SCHED: enabled
CONFIG_CPUSETS: enabled
CONFIG_MEMCG: enabled
CONFIG_INET: enabled
CONFIG_EXT4_FS: enabled
CONFIG_PROC_FS: enabled
CONFIG_NETFILTER_XT_TARGET_REDIRECT: enabled (as module)
CONFIG_NETFILTER_XT_MATCH_COMMENT: enabled (as module)
CONFIG_OVERLAY_FS: enabled (as module)
CONFIG_AUFS_FS: not set - Required for aufs.
CONFIG_BLK_DEV_DM: enabled (as module)
CGROUPS_CPU: enabled
CGROUPS_CPUACCT: enabled
CGROUPS_CPUSET: missing
CGROUPS_DEVICES: enabled
CGROUPS_FREEZER: enabled
CGROUPS_MEMORY: enabled
DOCKER_VERSION: 17.05.0-ce
[preflight] WARNING: docker version is greater than the most recently validated version. Docker version: 17.05.0-ce. Max validated version: 1.12
[preflight] Some fatal errors occurred:
	missing cgroups: cpuset
[preflight] If you know what you are doing, you can skip pre-flight checks with `--skip-preflight-checks`
~~~

Lỗi này không phải do docker chúng ta ở phiên bản quá cao so với 1.12 ( bằng chứng ta khi chạy Hypriot phiên bản mới nhất cũng sử dụng docker 17.05.0-ce mà kubeadm vẫn hoạt động)  mà do `cpuset` chưa được kích hoạt trong quá trình khởi động hệ thống. Để khắc phục điều này ta truy cập vào file `/boot/cmdline.txt` thêm `cgroup_enable=cpuset` vào cuối dòng và khởi động lại Pi. 

Sau khi khởi động lại ta có thể chạy lệnh `kubeadm init --pod-network-cidr 10.244.0.0/16` thành công để tạo một node master trên Pi.

### Vấn đề đa nền tảng 

Với hệ thống đang triển khai chúng ta luôn phải đối mặt với vấn đề đa nên tảng. Nếu dựng một cụm cluster Kubernetes hoàn toàn với các Node là Rasberry thì không có vấn đề nhưng khi sử dụng một máy tính thông thường ( với kiến trúc amd ) join vào cluster hay sử dụng để làm master thì sẽ không thể triển khai được nếu chạy Kubeadm một các tự động như trên

#### Cài đặt manifest tool 

Để khắc phục vấn đề trên ta sử dụng `manifest` để có thể chạy các image thích hợp cho các nền tảng phần cứng khác nhau. 

Bản chất để thao tác với manifest của docker thì ta sử dụng [HTTP API ](https://docs.docker.com/registry/spec/api/) của docker nhưng để đơn giản ta có thể sử dụng tool đã được cung cấp sẵn tại https://github.com/estesp/manifest-tool


Để có thể build được `manifest tool` ta cần cài đặt `go`:

- `sudo apt-get install golang-go`

- Tạo thư mục để lưu trữ code: `mkdir -p go/src/github.com/estesp`

- Đặt đường dẫn đến thư mục lưu trữ code của go: truy cập vào file `.profile` thêm vào cuối file `export GOPATH=$HOME/go` 

- Truy cập vào thư mục `go/src/github.com/estesp` vừa tạo ở trên download code: `git clone https://github.com/estesp/manifest-tool`

- Truy cập vào thư mục vừa tải vào build manifest tool: `cd manifest-tool && make binary`

#### Tạo một image đa nền tảng 

Ta pull 2 image của flannel kiến trúc amd và arm về máy 

~~~

docker pull quay.io/coreos/flannel:v0.7.1-arm

docker pull quay.io/coreos/flannel:v0.7.1-amd64

~~~

Đổi tag của các image để push lên repository của mình: 

~~~

docker tag quay.io/coreos/flannel:v0.7.1-amd64 haiquan5396/flannel:v0.7.1-amd64

docker tag quay.io/coreos/flannel:v0.7.1-arm haiquan5396/flannel:v0.7.1-arm

docker push haiquan5396/flannel:v0.7.1-amd64

docker push haiquan5396/flannel:v0.7.1-arm

~~~

Tạo một file `flannel.yaml` để lưu trữ các thông tin về kiến trúc và các image sẽ tải về tương ứng 

~~~

image: haiquan5396/flannel:latest
manifests:
  -
    image: haiquan5396/flannel:v0.7.1-arm
    platform:
      architecture: arm
      os: linux
  -
    image: haiquan5396/flannel:v0.7.1-amd64
    platform:
      architecture: amd64
      os: linux

~~~


Chạy lệnh :  `./manifest-tool push from-spec ~/flannel.yaml` 

- **chú ý:**  ~/flannel.yaml là địa chỉ của file yaml vừa tạo và lệnh được chạy trong thư mục build manifest-tool 

Vậy là ta đã có một image có thể chạy trên cả adm và arm. Khi sử dụng lệnh `docker pull haiquan5396/flannel` bạn sẽ có được image phù hợp với kiến trúc máy hiện tại. 


#### Demo dựng cluster Kubernetes 

Demo sau đây sử dụng một máy tính kiến trúc amd làm máy master và một raspberry kiến trúc arm làm minion

Đầu tiên ta cài đặt kubeadm, docker trên cả hai máy

Trên máy master ta chạy `sudo kubeadm init --pod-network-cidr 10.244.0.0/16` . Quá trình này lần đầu có thể diễn ra khá lâu do phải download các image. Kiểm tra log của quá trình và ghi lại câu lệnh sử dụng để join các node vào cluster ví dụ như: `kubeadm join --token 47404e.b4b1266dd8581106 192.168.0.124:6443`. Sau khi hoàn thành ta chạy các lệnh sau để có thể sử dụng `kubectcl`:

~~~

mkdir -p $HOME/.kube

sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config

sudo chown $(id -u):$(id -g) $HOME/.kube/config

~~~

Sửa đổi image chạy kube-proxy bằng lệnh: `kubectl -n kube-system set image daemonset/kube-proxy kube-proxy=luxas/kube-proxy:v1.7.3`. Do kube-proxy chạy bằng một daemonset nên phải sửa thành image đa nền tảng. `luxas/kube-proxy:v1.7.3` là một image đa nền tảng có thể sử dụng hoặc có thể tự tạo bằng cách đã hướng dẫn ở trên. 

Download 2 file chạy flannel về để chỉnh sửa cho phù hợp khi chạy đa nền tảng:

~~~

	wget https://rawgit.com/coreos/flannel/v0.7.1/Documentation/kube-flannel-rbac.yml

	wget https://rawgit.com/coreos/flannel/v0.7.1/Documentation/kube-flannel.yml

~~~

Trong file `kube-flannel.yaml` ta sử các image `quay.io/coreos/flannel:v0.7.1-amd64` thành image: `haiquan5396/flannel` ( vừa tạo ở trên ) và bỏ phần: 
~~~

      nodeSelector:
        beta.kubernetes.io/arch: amd64
        
~~~

Giờ ta chạy flannel bằng các lệnh: 

~~~

	kubectl create -f kube-flannel.yml

	kubectl create -f kube-flannel-rbac.yml
	
~~~

Kiểm tra các pod đã chạy chưa: 

~~~

master@masternode:~$ kubectl get pods --all-namespaces

NAMESPACE     NAME                                 READY     STATUS    RESTARTS   AGE
kube-system   etcd-masternode                      1/1       Running   0          11m
kube-system   kube-apiserver-masternode            1/1       Running   0          11m
kube-system   kube-controller-manager-masternode   1/1       Running   0          11m
kube-system   kube-dns-2425271678-dtlsr            3/3       Running   0          11m
kube-system   kube-flannel-ds-d2808                2/2       Running   1          2m
kube-system   kube-proxy-s6rqh                     1/1       Running   0          3m
kube-system   kube-scheduler-masternode            1/1       Running   0          11m


~~~

Giờ ta join Pi vào cluster sử dụng lệnh join được cung cấp khi chạy lệnh `kubeadm init` lúc đầu: `sudo kubeadm join --token 47404e.b4b1266dd8581106 192.168.0.124:6443`

Đợi quá trình hoàn tất ta sử dụng lệnh `kubectl get pods --all-namespaces` hoặc `kubectl get nodes` trên master để kiểm tra. Nếu quá trình thành công ta sẽ được: 

~~~

master@masternode:~$ kubectl get nodes 
NAME          STATUS    AGE       VERSION
masternode    Ready     17m       v1.7.4
raspberrypi   Ready     1m        v1.7.4

~~~


# Tạo một Registry Server

Đầu tiên ta tạo một `self-signed certificates`:

~~~

mkdir -p certs
	
openssl req \
  -newkey rsa:4096 -nodes -sha256 -keyout certs/domain.key \
  -x509 -days 365 -out certs/domain.crt
  
~~~

Khi chạy lệnh openssl bạn có thể phải nhập một số thông tin. Ta có thể bỏ qua và chỉ nhập `Common Name ` là tên server mà bạn muốn đặt. Ở đây mình chọn là `hpcchub.com`:

~~~

Country Name (2 letter code) [AU]:
State or Province Name (full name) [Some-State]:
Locality Name (eg, city) []:
Organization Name (eg, company) [Internet Widgits Pty Ltd]:
Organizational Unit Name (eg, section) []:
Common Name (e.g. server FQDN or YOUR name) []:hpcchub.com
Email Address []:

~~~

Ta sẽ thấy trong thư mục `certs` vừa tạo có 2 file `domain.key` và `domain.crt`

Trên mọi node mà bạn muốn truy cập vào registry, bạn truy cập vào file `/etc/hosts` thêm dòng địa chỉ và tên server sẽ truy cập để máy có thể phân giải địa chỉ. Sau đây là file `/etc/hosts` sau khi thêm dòng `192.168.0.124   hpcchub.com`:

~~~

127.0.0.1       localhost
127.0.1.1       masternode
192.168.0.124   hpcchub.com

# The following lines are desirable for IPv6 capable hosts
::1     localhost ip6-localhost ip6-loopback
ff02::1 ip6-allnodes
ff02::2 ip6-allrouters
~~~

Tiếp đến ta copy file `domain.crt` vào đường dẫn `/etc/docker/certs.d/hpcchub.com:5000/ca.crt` trên mọi node muốn truy cập. 

Bây giờ ta chạy lệnh: 

~~~

docker run -d \
  --name registry \
  -v /home/master/certs:/certs \
  -e REGISTRY_HTTP_TLS_CERTIFICATE=/certs/domain.crt \
  -e REGISTRY_HTTP_TLS_KEY=/certs/domain.key \
  -v /home/master/registry:/var/lib/registry \
  -p 5000:5000 \
  registry:2
  
~~~

Kiểm tra xem registry có hoạt động không: 

- tải một image về máy: `docker pull ubuntu:16.04`

- Đổi tag của image: `docker tag ubuntu:16.04 hpcchub.com:5000/my-ubuntu`

- push lên registry vừa tạo: `docker push hpcchub.com:5000/my-ubuntu`

- Xóa các image `hpcchub.com:5000/my-ubuntu` và `ubuntu:16.04`

- Thử pull lại image `hpcchub.com:5000/my-ubuntu` xem có thành công không. 


# Tài liệu tham khảo

- https://integratedcode.us/2016/04/22/a-step-towards-multi-platform-docker-images/

- https://blog.hypriot.com/post/setup-kubernetes-raspberry-pi-cluster/

- https://github.com/estesp/manifest-tool

- https://github.com/luxas/kubeadm-workshop

- https://docs.docker.com/registry/deploying/

- https://docs.docker.com/registry/insecure/