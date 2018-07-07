# Sơ đồ hệ thống Rule Engine

![Sơ đồ hệ thống Rule engine](https://raw.githubusercontent.com/hamhochoi/K59_training/master/Cloud/Monitor/diagram_rule_new.png "rule engine")

# Luồng hoạt
- Driver đọc dữ liệu từ IOT platform rồi chuyển dữ liệu cho Filter.
- Filter có nhiệm vụ lọc, chuyển tiếp dữ liệu cho Forwarder (hiện tại chưa có chức năng lọc dữ liệu). 
- Forwarder có chức năng chuyển tiếp dữ liệu đến các microservices khác nhau trong hệ thống. Cụ thể hệ thống hiện tại là chuyển tiếp dữ liệu cho Collectoer
- Collector thu thập dữ liệu của toàn bộ các IOT platform. Khi lấy được trạng thái các item trong hệ thống, Collector gửi dữ liệu cho Rule Engine để theo dõi hệ thống
- Rule API có chức năng cung cấp cho người sử dụng thông qua giao diện UI thực hiện các thao tác thêm, sửa, xóa các rule của hệ thống. Các rule này sẽ được lưu vào CSDL để load lại mỗi khi người sử dụng vào giao diện UI để thêm, sửa, xóa rule.
- Rule Engine sẽ đọc các rule được enable trong hệ thống, đồng thời nhận dữ liệu của các thiết bị trong hệ thống từ Collector để thực hiện giám sát các thiết bị trong hệ thống. Khi các rule được thỏa mãn, tùy vào các action mà người dùng lựa chọn (trong tập các action mà Rule Engine cho phép), hệ thống có thể sinh ra Alert, thay đổi trạng thái của các thiết bị dưới tầng IOT platform thông qua API set state,...

# Chi tiết một số module quan trọng

## Rule Engine

- Nhận thông tin về trạng thái của các thiết bị từ Collector sử dụng RabbitMQ broker (MQTT). 
  - Queue: monitor.request.collector
- Nhận thông tin về các rule được enable trong hệ thống từ RuleAPI qua HTTP request.
  - Địa chỉ: http://127.0.0.1:5000/rule
  - Mỗi rule được định dạng theo một json format (xem trong file [rule_example.json](https://github.com/hamhochoi/K59_training/blob/master/Cloud/Monitor/rule_example.json)
- Khi nhận được message từ Collector, tạo một **subprocess** để giám sát các item trong hệ thống
  - Hàm **monitor** : lấy list các rule, với mỗi rule, kiểm tra điều kiện bằng cách duyệt qua tất cả các item trong hệ thống và so sánh với điều kiện của rule đó.  
  - Trong khi check điều kiện của các rule, do chương trình cần biết trạng thái của các item trong hệ thống trước đó một khoảng thời gian (ứng với trường rule_condition -> "timer" trong json format), một request sé được gửi tới DBreader để lấy dữ liệu trong quá khứ được lưu trong CSDL. 
  - Thực hiện các action Alert hoặc set state cho các item dưới tầng IOT platform tùy thuộc vào kiểu action mà người dùng lựa chọn (tương ứng với trường action_name trong json format)
  
## Rule API

- Có các chức năng thêm, sửa, xóa, lưu trữ các rule mà người dùng định nghĩa ra.
- Với các trường được thêm mới/sửa, các rule được lưu trong CSDL với trường rule_status là "enable".
- Với các rule được xóa đi, các rule đó vẫn được lưu trong CSDL nhưng với trường rule_status là "disable". 


