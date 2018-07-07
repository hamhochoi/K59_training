# Sơ đồ hệ thống Rule Engine

![Sơ đồ hệ thống Rule engine](https://raw.githubusercontent.com/hamhochoi/K59_training/master/Cloud/Monitor/diagram_rule_new.png "rule engine")

# Luồng hoạt
- Driver đọc dữ liệu từ IOT platform rồi chuyển dữ liệu cho Filter.
- Filter có nhiệm vụ lọc, chuyển tiếp dữ liệu cho Forwarder (hiện tại chưa có chức năng lọc dữ liệu). 
- Forwarder có chức năng chuyển tiếp dữ liệu đến các microservices khác nhau trong hệ thống. Cụ thể hệ thống hiện tại là chuyển tiếp dữ liệu cho Collectoer
- Collector thu thập dữ liệu của toàn bộ các IOT platform. Khi lấy được trạng thái các item trong hệ thống, Collector gửi dữ liệu cho Rule Engine để theo dõi hệ thống
- Rule API có chức năng cung cấp cho người sử dụng thông qua giao diện UI thực hiện các thao tác thêm, sửa, xóa các rule của hệ thống. Các rule này sẽ được lưu vào CSDL của 


