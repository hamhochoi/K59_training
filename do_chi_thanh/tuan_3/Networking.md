# Tầng Giao vận

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
    * Đơn vị dữ liệu : byte stream
    * Giao thức hướng kết nối: Xác thực bên nhận, bên gửi trước khi gửi, nhận tin.
        --> Sử dụng giao thức bắt tay 3 bước 
    * Truyền thông hướng tin cậy: Đảm bảo xác thực bên nhận, gửi; xác nhận gói tin nhận được thông qua ACK; truyền lại gói tin bị lỗi; cơ chế timeout
    * Thứ tự gói tin nhận được được đảm bảo.
    * Một ứng dụng có thể sử dụng nhiều socket khác nhau để trao đổi dữ liệu với các tiến trình khác nhau.
    * Kiểm soát luồng: Đảm bảo không làm quá tải bên nhận
    * Kiểm soát tắc nghẽn: Đảm bảo không làm mạng quá tải
    
# Tầng mạng

## 
