# Virtualization 

**Virtualization** hiểu là tạo ra một phiên bản ảo chứ không phải thực của một các gì đó, bao gồm: ảo hóa nền tảng phần cứng, thiết bị lưu trữ và tài nguyên mạng

Ảo hóa bắt đầu từ năm 1960 giống như một các thức để phần chia các tài nguyên của hệ thống được cung cấp bởi các máy tính lớn cho các ứng dụng khác nhau. Từ đó thuật ngữ này được mở rộng


## Các công nghệ virtualization 
### Hardware virtualization

`Hardware Virtualization` hay `Platform Virtualization` là việc tạo ra các máy ảo giống như một máy tinh thực tế với một hệ điều hành. Phầm mềm chạy trên máy ảo sẽ được tác bệnh với phần cứng bên dưới. Ví dụ, một máy tính chạy Windows có thể lưu trữ một máy ảo giống như một máy tính thực sự đang chạy hệ điều hành Ubuntu.

Trong `hardware virtualization`, khái niệm `host machine` chỉ máy mà trên đó có thực hiện ảo hóa, còn `guest machine` là các máy ảo chạy trên `host machine`. Phần mềm hay firmware để tạo một máy ảo gọi là `hypervisor` hay `Virtual Machine Manager`

Có các kiểu `hardware virtualization` là: 

- `Full virtualization`: mô phỏng hầu như hoàn toàn phần cứng thực tế cho phép chạy phần mềm, hay hệ điều hành mà không cần phải sửa đổi. Full virtualization yêu cầu mọi tính năng nổi bật của phần cứng phải được phản ánh vào máy ảo - bao gồm : tập các lệnh, điều khiển vào ra, ngắt, truy cập bộ nhớ và nhiều thành phần khác cần thiết để các phần mềm chạy trên máy ảo có thể thực hiện. Do vậy tất cả các phần mềm có khả năng chạy trên phần cứng đều có thể chạy trên máy ảo.

- `Paravirtualization`: môi trường phần cứng không được mô phỏng; tuy nhiên, `guest programs` được chạy trên một miền độc lập như thể là chúng đang chạy trên một hệ thống riêng biệt. `Guest programs` cần được sửa đổi để chạy trong môi trường này 

Khác nhau : 

- Full virtualization: guest operating system không biết rằng nó đang trong môi trường ảo hóa nó sẽ nghĩ là phần cứng được ảo hóa chính là phần cứng thực sự nên nó sẽ sử dụng các lệnh với phần cứng như là phần cứng thực sự

- Paravirtualization: guest operating system biết gằng nó là guest machine và đang trong môi trường ảo hóa, có dirver điều khiển (hypervisor) do đó nó không ra lệnh cho phần cứng mà ra lệnh đến host OS

#### Hypervisor 

`Hypervisor` hay `virtual machine monitor` (VMM) là một phần mềm, firmware để dùng để tạo, chạy máy ảo. Có 2 kiểu `hypervisor`:

- `Type-1, native or bare-metal hypervisor` : hypervisors chạy trực tiếp trên phần cứng, nó điều khiển phần cứng và quản lý các `guest machine`. 
- `Type-2, hosted hypervisor`: hypervisor chạy trên một hệ điều hành giống như các chương trình máy tính khác và các `guest machine` sẽ được tạo trên `hypervisor`


![https://en.wikipedia.org/wiki/Hypervisor#/media/File:Hyperviseur.png](https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/Hyperviseur.png/400px-Hyperviseur.png) 



#### Snapshots

Môt `snapshot` là một trạng thái của máy ảo. Nó cho phép khôi phục một trạng thái nào đó của máy ảo tại một thời điểm tạo snapshot

#### Migration 

`Snapshot` được mô tả ở trên có thể được di chuyển đến một `host machine` khác . Khi máy ảo tạm dừng, được snapshot, di chuyển sau đó tiếp tục trên một host khác thì được gọi là `migration`

#### Failover 

Giống như cơ chế của `migration`, `failover` cho phép VM tiếp hoạt động nếu host bị lỗi. Tuy nhiên trong trường hợp này, VM sẽ tiếp tục trạng thái mà nó lưu giữ mới nhất chứ không phải là trạng thái hiện tại 

#### Reasons for hardware virtualization

- Trong trường hợp server tập trung, các server nhỏ sẽ được thay thế bởi một server lớn hơn để tăng khả năng sử dụng các tài nguyên. Thay vì mỗi OS chạy trên một máy vật ý riêng biệt thì giờ đây sẽ chuyển thành mỗi OS riêng biệt chạy trên một máy ảo. Vì nếu mỗi OS chạy trên một máy vật lý riêng biệt thì sẽ bị hạn chế tài nguyên còn nếu mỗi OS chạy trên một máy ảo và được quản lý bởi `hypersivor` thì sẽ linh hoạt hơn.

- Một máy ảo dễ dàng kiểm soát và kiểm tra hơn là một thiết bị vật lý, bên cạnh đó cấu hình của nó cũng linh hoạt hơn.

- Một máy ảo có thể được cung cấp phần cứng khi cần thiết 
- Một máy ảo có thể dễ dàng để di chuyển từ máy vật lý này sang máy vật lý khác khi cần. Điều này cũng khiến việc khôi phục hệ thống dễ dàng hơn 




### Desktop virtualization

`Desktop Virtualization` là khái niệm chỉ sự tách biệt giữa desktop với máy vật lý 

Một kiểu của `desktop virtualization` là `virtual desktop infratructure` (VDI), có thể coi là một kiểu tiên tiến hơn là `hardware virtualization`. Thay vì tương tác trực tiếp với `host computer` thông qua bàn phím, chuột và màn hình thì bây giờ người sử dụng sẽ tương tác với `host computer` thông qua một kết nối mạng sử dụng desktop khác hoặc một thiết bị di động. Thêm vào đó, `host computer` trong trường hợp này trở thành một server có khả năng làm máy chủ của nhiều máy ảo trong cùng một thời điểm cho nhiều người dùng 


### Software virtualization 

- `Operating system-level virtualization` : cho phép lưu trữ nhiều môi trường ảo hóa trong mỗi hệ điều hành. Kernel của OS cho phép sự tồn tại của nhiều `user-space` cô lập thay vì chỉ một. `OS-level virtualization` đòi hỏi ít hoặc rất ít chi phí vì chương trình trong các phân vùng ảo sử dụng các lời gọi hệ thống thông thường của hệ điều hành và không cần mô phỏng hay chạy một máy ảo trung gian. 

- `Application virtualization` và `workspace virtualization`: lưu trữ các ứng dụng vào môi trường tách biệt với hệ điều hành bên dưới. `Application virtualization` gắn liền với khái niệm `portable application`.

- `Service virtualization`: mô phỏng các thành phần mà hệ thống cần để chạy một chương trình với mục định phát triển hay testing.


### Memory virtualization 

`Memory virtualization`: tập hợp tài nguyên RAM của toàn hệ thống vào một nơi là `memory pool`. `Memory pool` có thể được truy cập bởi hệ điều hành hay các ứng dụng. Với khả năng có thể kết nối mạng, các ứng dụng có thể tận dụng được rất nhiều memory để tăng hiệu suất và khả năng của ứng dụng không còn bị hạn chế. 


### Network virtualization 

Network virtualization là quá trình kết hợp các phần cứng, phần mềm mạng và chức năng của mạng vào một thực thể duy nhất, một `virtual network`. Nó được chia làm hai loại `external virtualization` và `internal virtualization`

- External virtualization: kết hợp nhiều mạng hay thành phần của mạng vào trong một đơn vị ảo hóa. 
- Internal virtualization: cung cấp một chức năng giống như mạng đến các software container trên một hệ thống 


## Container 

`LXC ` (Linux Containers) là một phương pháp ảo hóa tầng hệ điều hành ( operating system level virtualization) cho phép chạy nhiều hệ thống Linux riêng biệt (containers) trên một `control host` sử dụng Linux kernel. Linux kernel cung cấp `cgroups` cho phép giới hạn và ưu tiên các tài nguyên hệ thống ( CPU, memory, block I/O, network, etc ) mà không cần phải chạy bất kỳ `virtual machine` nào, ngoài ra chức năng `namespace isolation` cũng cho phép cô lập hoàn toàn một khung nhìn của ứng dụng trong môi trường hoạt động, bao gồm cây tiến trình, mạng, user IDs và mounted file systems. `LXC` kết hợp cgroups của nhân Linux và hỗ trợ cô lập namespace để cung cấp một môi trường cô lập cho ứng dụng. 

Một `container` gồm một tập các tiến trình được cô lập với phần còn lại của hệ thống được chạy từ một `image` cung cấp tất cả các file cần thiết cho quá trình hoạt động của tiến trình. Bằng cách cung cấp một `image` bao gồm tất cả những gì ứng dụng cần nên nó là `portable` và `consistent` khi di chuyển từ sang các môi trường khác nhau ( lập trình, kiểm thử... ) 

![http://electronicdesign.com/site-files/electronicdesign.com/files/uploads/2015/02/0716_CTE_WTDcontainers_F1WEB.gif](http://electronicdesign.com/site-files/electronicdesign.com/files/uploads/2015/02/0716_CTE_WTDcontainers_F1WEB.gif  "Virtual Machine vs Container")

`Container` không chạy một OS hoàn chỉnh giống như `virtual machine`, các `container` chạy trên `namespace` của chúng nhưng sử dụng chung một kernel vì thế mà nó sẽ tiêu tốn ít tài nguyên hơn (lightweight) điều này cho phép ta có thể chạy nhiều ứng dụng cô lập hơn là khi sử dụng `virtual machine`. Tuy nhiên khái niệm cô lập sử dụng `namespace` của `container` không thực sự mạnh bằng `virtual machine`, với `virtual machine` thì các `guest OS` không thể có toàn quyền truy cập vào `host OS` hay các guest khác 


`Docker` là một công cụ để tạo, quản lý và giám sát các `container`.  `Docker` đã đưa ra một số thay đổi đáng kể đối với `LXC` để làm cho container trở nên linh hoạt và dễ sử dụng hơn. Sử dụng `Docker container` bạn có thể deploy, replicate, move, và back up một công việc nhanh hơn cả khi bạn sử dụng virtual machine.


