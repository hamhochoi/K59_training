# virtualization and container basic
## 1. virtualization_ sự ảo hóa
### - Sự ảo hóa là gì ?
Là tạo ra thêm phiên bản phụ ( phiên bản ảo) của các thành phần trong hệ thống máy tính như: Phần cứng, phần mềm, thiết bị lưu trữ, mạng máy tính,...
-->chạy nhiều thứ hơn trên 1 máy tính duy nhất.
### - 1 số ví dụ về ảo hóa:
- Hệ điều hành ảo( tạo máy ảo):Có thể tạo nhiều máy ảo trên 1 máy tính duy nhất, bên cạnh đó cũng có thể chạy song song cùng lúc 2 hệ điều hành.
việc chuyển đổi giữa 2 hệ điều hành này đơn giản như thao tác với 2 cửa sổ trên máy tính.
Máy thật và máy ảo có thể chia sẻ dữ liệu với nhau.
Các phần mềm chuyên dụng cho việc tạo hệ điều hành ảo này: VMware, VirtualBox, Virtual PC, VMware Fusion,...


- Ổ đĩa ảo: Khi máy tính có gắn ổ đĩa quang thì đó là ổ đĩa thật.
những khi máy tính không có ổ đĩa thật này, mà khi tải 1 số phần mềm, phim có dạng file ảnh
.ISO/.IMG. Muốn đọc những file này mà không cần ghi ra đĩa, có thể sử dụng
phần mềm đọc file hoặc cài ổ đĩa ảo.
Ví dụ phần mềm tạo ổ đĩa ảo: Alcohol, DAEMON Tools,...

- Desktop ảo:
 Giả sử khi có 1 máy chủ trung tâm tại 1 công ty, chứa đầy đủ dữ liệu, phần mềm, ...phục vụ công việc cho các nhân viên, mà không thể nào
 trang bị 1 loạt máy chủ như thế cho mỗi nhân viên, giải pháp ở đây là từ máy chủ trung tâm tạo ra nhiều desktop ảo và cung cấp cho các nhân viên.
 --> nhiều người có thể làm việc cùng lúc trên máy chủ đó.

- RAM ảo:
Các hệ thống máy chủ cũng rất hay dùng RAM ảo. RAM ảo được tao ra từ việc gộp chung tất cả RAM hiện có trong 1 trung tâm thành 1 RAM chung cho toàn hệ thống. Đối với máy tính cá nhân cũng có tạo RAM ảo, bằng cách trích 1 phần ổ cứng làm RAM ảo,
 giúp làm giảm gánh nặng xử lí ở RAM thật.

- Máy chủ ảo ( Virtual Private Server_VPS): Nhiều máy chủ ảo có thể chạy trên
một máy chủ thực. sẽ giúp tiết kiệm chi phí thuê, mua server đối với những ứng dụng đòi hỏi server không
cần quá mạnh.



### - Các công nghệ ảo hóa:

  Có thể kể đến các công nghệ ảo hóa như Hyperviser hay OS level, ...
- Hypervisor:  cung cấp các môi trường tách biệt gọi là các phân vùng_partition. Mỗi phân vùng ứng với 1 máy ảo với hệ điều hành riêng.
VD: Hyper-V, Xen,...Hypervisor có thể chia làm 2 loại: Native (Bare Metal Hypervisor) và Hosted Hypervisor

  ![anhhy](http://i.imgur.com/phbvkWK.png)

  ![anhhy1](http://i.imgur.com/Xp28nEJ.png)

Native gồm: Monolithic và Microkernelized

  ![anhhy2](http://i.imgur.com/vPr1F3a.png)

- OS level (Isolation): hay còn gọi là Containers Virtualization , là phương pháp ảo hóa mới
cho phép nhân của hệ điều hành hỗ trợ nhiều instances (còn được gọi là container) dựa trên 1 hệ điều hành có sẵn cho nhiều users khác nhau.
--> tạo, chạy nhiều máy ảo được cách ly, an toàn dùng chung 1 hệ điều hành.
Ưu điểm của công nghệ này là bảo trì nhanh chóng nên được sử dụng nhiều trong lĩnh vực hosting.
. công nghệ này chỉ tồn tại trên hệ điều hành Linux.
VD: chroot, Docker,...

## 2. virtual machine_ máy ảo

### - Máy ảo là gì?

Máy ảo là 1 chương trình đóng vai trò như 1 máy vi tính ảo.
Nó chạy trên hệ điều hành thật(hệ điều hành chủ) cung cấp phần cứng ảo tới hệ điều hành ảo (hệ điều hành khách)
Hệ điều hành khách hoạt động trên cửa sổ của hệ điều hành chủ như mọi chương trình khác trên máy tính.
Các thiết bị phần cứng ảo được cung cấp bởi máy ảo và ánh xạ đến phần cứng thực trên máy thật.
ví dụ : ổ đĩa cứng ảo được lưu trong 1 file đặt trong ổ đĩa cứng thật.

Có thể cài đặt nhiều máy ảo trên 1 máy chủ, chỉ bị hạn chế bởi dung lượng.

VD: VirtualBox, VMware Player,...



### - Các công nghệ tạo VM:

1 sô công nghệ : VMware,Xen, Hyper_V,KVM,...
trong đó:
- VMware ESX and ESXi:  là 1 nền tảng được tạo bởi VMware, chạy trên Bare Metal, với kiến trúc Monolithic.
- Hyper-V:  được tạo bởi Microsoft, cũng thuộc loại máy ảo Bare Metal, nhưng với kiến trúc Microkernelized
- Xen: xuất phát từ 1 đồ án nghiên cứu của trường đại học Cambridge, với kiến trúc Microkernelized.
- KVM(Kernel-based Virtual Machine): được phát triển bởi Redhat.công nghệ này thuộc loại Native hay Hosted còn nhiều tranh cãi xung quanh.


## 3. Docker
### - Docker là gì?
Docker là 1 công cụ tạo môi trường được đóng gói_container trên máy tính, không làm tác động đến môi trường hiện tại của máy tính.
(Docker có thể đóng gói cả hệ điều hành).



### - Docker khác máy ảo:
Điểm khác biệt chính ở đây là các containers có kernel có thể chia sẻ với các containers khác, trong khi mỗi máy ảo sẽ có ứng dụng, thư viện, hệ điều hành riêng biệt.

![anhss](http://i.imgur.com/rFzcxyj.png)


Thành phần :
- Docker Engine: thành phần chính của Docker, như 1 công cụ để đóng gói ứng dụng.
- Docker Hub: dịch vụ cloud để chia sẻ ứng dụng.

Các khái niệm:

- Docker images: giống như 1 môi trường đã được xây dựng
- Docker registries: kho chứa images. Có thể tạo ra các images của mình tải lên đây hoặc tải về các images được chia sẻ.
- Docker container: giống như 1 thư mục.chứa tất cả những thứ để ứng dụng có thể chạy được. Mỗi Docker container được tạo ra từ 1 Docker image.
- Dockerfile: file chứa tập hợp các lệnh để Docker có thể đọc , thực hiện để đóng gói 1 image.
- Orchestration: là các công cụ, dịch vụ để điều phối, quản lí nhiều containers để chúng làm việc hiệu quả nhất.

Docker là "lightweight" vì mỗi container chứa ứng dụng, thư viện riêng nhưng kernel được chia sẻ với các containers khác nên dung lượng mỗi container chiếm sẽ không lớn như mỗi máy ảo cần có.
# end.
