# ThingsBoard
```
address: 192.168.0.198:8080
email: tenant@thingsboard.org
password: tenant
```
Thingsboard quản lý device theo user. Hiện tại đã có user HPCC. Khi tạo device mới thì gán device đó vào user. Từ đó sẽ gọi API của Thingsboard lấy tất cả các device thuộc user đó.

Thingsboard tự có mqtt broker của chính nó nên không cần phải chạy mqtt ngoài nữa. Thingsboard tự quy định topic của nó, gồm:
- `v1/devices/me/attributes`: subscribe các thuộc tính của device.
- `v1/devices/me/telemetry`: subscribe các giá trị của device.
- `v1/devices/me/rpc/request/+`: subscribe các request từ thiết bị khác.
- `v1/devices/me/rpc/response/$request_id`: subscribe response của ThingsBoard. ($request_id là một số)
- v.v. Xem thêm ở [https://thingsboard.io/docs/reference/mqtt-api/]()

Các device phân biệt nhau bởi 1 Access token. Mỗi device sẽ có một Access token riêng (mình có thể đặt tên được).

Address Api của ThingsBoard: `192.168.0.198:8080/swagger-ui.html`. Phải có 1 Jwt mới có thể sử dụng Api, trong Driver cũng cần phải có Jwt. Lệnh để get Jwt:
```
curl -X POST --header 'Content-Type: application/json' --header 'Accept: application/json' -d '{"username":"tenant@thingsboard.org", "password":"tenant"}' 'http://192.168.60.198:8080/api/auth/login'
```

Dashboard hiện tại có bảng điều khiển 3 đèn.