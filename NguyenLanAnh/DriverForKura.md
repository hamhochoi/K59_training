# Driver reading data from sensor for Kura
## 1. Kura
Kura thực tế là một cái dự án opensource nhằm cung cấp container dựa trên OSGi cho những ứng dụng M2M
chạy ở những thiết bị gateways như Raspberry Pi.

OSGi-The Open Services Gateway Initiative : sẽ định nghĩa lên kiến trúc
cho việc phát triển hay triển khai những cái ứng dụng hay thư viện theo hướng modun.

Về cơ bản, Kura sẽ cung cấp platform tại gateways nằm giữa "private device network" với "local network"/"public network"/ "cellular network", quản lí những ứng dụng đang hoạt động thu thập dữ liệu local hay quản lí
chuyển giao dữ liệu một cách đáng tin cậy tới cloud.

Dưới đây là hình ảnh khái quát cho những chức năng của Kura:


![kura1](http://imageshack.com/a/img922/6189/MDRlrZ.png)

## 2. Thiết lập môi trường phát triển

Môi trường để phát triển Kura, cần những thành phần:
- JVM (Java JDK SE 8 or Open JDK 8)
- Eclipse IDE
- Kura Workspace setup

Việc cài đặt những thành phần trên có đầy đủ tại: https://eclipse.github.io/kura/dev/kura-setup.html

Đồng thời, cũng cài đặt plugin mToolkit,và import Kura User Workspace. Hướng dẫn chi tiết cũng đã có tại link trên.

## 3. driver đọc dữ liệu từ sensor cho Kura.

Sensor nối với Arduino:

![arduinoandsensor](http://imageshack.com/a/img923/7159/B3GlmA.png)

Arduino(bộ vi điều khiển) sẽ nhận được những tín hiệu tương tự, đọc và lưu giữ gía trị nhận được từ sensor.
Arduino được kết nối với Raspberry Pi qua dây cáp:

![rasp](http://imageshack.com/a/img923/9484/H9jMdd.png)

Raspberry Pi này sẽ được cài đặt Kura để quản lí những dữ liệu nhận được. Kura cần có 1 driver đọc dữ liệu từ Arduino đó.
Eclipse hỗ trợ nhiều thư viện I/O này như : Pi4j hay Device I/O. Hiện tại sẽ sử dụng thư viện Pi4j.Cụ thể là gói serial cho việc đọc dữ liệu thông qua dây nối.

End.
