# Tầng Giao vận : Điều khiển việc truyền dữ liệu giữa các tiến trình trên tầng ứng dụng

## Giao thức UDP (User Diagram Protocol)

* Các đặc điểm: 
    * Đơn vị dữ liệu : diagram
    * Giao thức hướng không kết nối: Không xác thực bên nhận trước khi gửi
        --> Truyền thông không tin cậy, đối với các ứng dụng cần đảm bảo tính tin cậy, ứng dụng sẽ phải cài đặt cơ chế kiểm soát độ tin cậy, do đó sẽ phức tạp hơn
    * Không có quản lý tắc nghẽn: Dữ liệu được gửi đi nhanh nhất và nhiều nhất có thể
        --> Làm mạng quá tải
    * Phát hiện lỗi 1 bit bằng checksum
    * Mỗi tiến trình sử dụng một socket duy nhất để trao đổi dữ liệu với tiến trình khác.
    * Thứ tự nhận gói tin không được đảm bảo
## Giao thức TCP (Tranmission Control Protocol)
* Các đặc điểm:
    * Đơn vị dữ liệu : byte stream
    * Giao thức hướng kết nối: Xác thực bên nhận, bên gửi trước khi gửi, nhận tin.
        --> Sử dụng giao thức bắt tay 3 bước 
    * Truyền thông hướng tin cậy: Đảm bảo xác thực bên nhận, gửi; xác nhận gói tin nhận được thông qua ACK; truyền lại gói tin bị lỗi; cơ chế timeout
    * Thứ tự gói tin nhận được được đảm bảo.
    * Một ứng dụng có thể sử dụng nhiều socket khác nhau để trao đổi dữ liệu với các tiến trình khác nhau.
    * Kiểm soát luồng: Đảm bảo không làm quá tải bên nhận
    * Kiểm soát tắc nghẽn: Đảm bảo không làm mạng quá tải
    
# Tầng mạng: Điều khiển việc truyền dữ liệu giữa các nút mạng qua môi trường liên mạng

## Tổng quan
* Các đặc điểm: 
     * Truyền dữ liệu host - host
     * Cài đặt trên mọi hệ thống cuối và bộ định tuyến
     * Đơn vị truyền: diagram 
     * Bên gửi: nhận dữ liệu từ tầng giao vận, đóng gói
     * Bên nhận: mở gói, chuyển phần dữ liệu trong payload cho tầng giao vận
     * Bộ định tuyến: Định tuyến và truyền tiếp
     
 * Các chức năng chính: 
     * Định tuyến: Tìm đường đi qua các nút trung gian để tìm tới đích
         * Giao thức định tuyến giúp xác định đường đi ngắn nhất tới đích.
     * Chuyển tiếp: Chuyển gói tin trên cổng vào tới cổng ra theo tuyến đường
         * Bảng định tuyến giúp chuyển tiếp gói tin tới cổng ra trên bộ định tuyến để truyền gói tin tới đích
     * Định địa chỉ: Định danh cho các nút mạng
     * Đóng gói dữ liệu : Nhận dữ liệu từ giao thức tầng trên, thêm tiêu đề mang thông tin điều khiển quá trình truyền dữ liệu tới nút đích
     * Đảm bảo chất lượng dịch vụ: đảm bảo các thông số phù hợp với đường truyền theo từng dịch vụ
     
 ## Giao thức IP (Internet Protocol)

  * Đặc điểm: 
      * Giao thức không tin cậy: 
            * Truyền dữ liệu theo kiểu best-effort
            * Không có cơ chế phục hồi lỗi
            * Khi cần đảm bảo tính tin cậy, sẽ sử dụng dịch vụ tầng trên (TCP).
      * Giao thức hướng không liên kết 
      * Các gói tin được xử lý độc lập
      
  * Chức năng cơ bản của IP:
      * Định địa chỉ IP
      * Đóng gói dữ liệu
      * Chuyển tiếp theo địa chỉ IP
      * Đảm bảo chất lượng dịch vụ
  * Định địa chỉ IP
      * Địa chỉ IP dùng để định danh các thiết bị trong mạng
      * Mỗi thiết bị có duy nhất một IP
      * Địa chỉ IP có tính duy nhất trong mạng
      * Địa chỉ IP gồm có 2 phần NetworkID(địa chỉ mạng) và HostID (Địa chỉ máy trạm)
      * Có 2 cách phân địa chỉ IP: Phân lớp và không phân lớp
           * Phân lớp địa chỉ IP: Các bit trong địa chỉ IP được chia cố định thành các phần
               --> Làm hạn chế việc sử dụng không gian mạng IP do số lượng nhỏ, gây lãng phí
           * Không phân lớp: Sử dụng mặt nạ mạng đính kèm với IP để xác định số bit phần networkID
   * Đóng gói dữ liệu: 
      * Đường truyền có một giá trị tối đa kích thước của một gói tin có thể truyền qua (MTU)
      * Các gói tin có kích thước lớn hơn MTU được chia ra thành các gói tin nhỏ hơn, và sẽ được tập hợp lại tại bên nhận
      
   * Chuyển tiếp gói tin: 
      * Mỗi nút mạng sử dụng một bảng forwarding table (một phần của bảng định tuyến)
      * Các thông tin trên bảng : nút đến , cổng ra.
      
# Tầng liên kết: Hỗ trợ việc truyền thông cho các thành phần kế tiếp trên cùng một mạng

* Các chức năng chính: 
   * Đóng gói dữ liệu: Đơn vị khung tin dữ liệu
   * Địa chỉ hóa : Sử dụng địa chỉ MAC
   * Điều khiển truy nhập đường truyền
   * Kiểm soát luồng: Đảm bảo bên nhận không quá tải
   * Kiểm soát lỗi: Phát hiện và sửa lỗi bit trên các khung tin: Sử dụng chủ yếu mã vòng CRC
   
* Các đặc điểm chính: 
   * Điều khiển truyền dữ liệu trên liên kết vật lý giữa 2 nút mạng kế tiếp
   * Triển khai trên mọi nút mạng, trên cạc mạng hoặc chip tích hợp
   
* Định địa chỉ MAC:
   * Địa chỉ MAC gồm 48 bit, được quản lý bởi IEEE
   * Mỗi cổng mạng được gán một địa chỉ MAC
   * Địa chỉ MAC của một thiết bị là không đổi
         --> Không thể thay đổi địa chỉ vật lý
   * ARP : Tầng mạng sử dụng địa chỉ IP, tầng liên kết sử dụng địa chỉ MAC, do đó cần sử dụng một bảng để ánh xạ tương ứng địa chỉ IP và địa chỉ MAC của thiết bị.
  
* Điều khiển truy nhập đường truyền
   * Các dạng liên kết đường truyền : Điểm - điểm và điểm - đa điểm
   * Các phương pháp điều khiển truy nhập
      * Phân tài nguyên sử dụng kỹ thuật chia kênh
      * Truy cập ngẫu nhiên
      * Lần lượt
      
* Chuyển tiếp dữ liệu trong mạng LAN
    * Sử dụng địa chỉ MAC
    * Cơ chế tự học
      
  
