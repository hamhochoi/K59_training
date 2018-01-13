# Framework driver/ wrapper
### 1. Heapster, InfluxDB, Grafana

- Heapster: Thu thập các số liệu trong cụm như CPU, không gian đĩa, sự sử dụng bộ nhớ,...

- InfuxDB: Cơ sở dữ liệu time series.

- Grafana: Một giải pháp cho dashboard

### 2. Làm việc với InfluxDB

Sau khi đã chạy file influxdb_deployment.yaml, influxdb_service.yaml.
Sử dụng câu lệnh:

     kubectl get services --namespace=kube-system

Để thấy các service đang được sử dụng, và đồng thời ghi nhớ địa chỉ IP của monitoring-influxdb,
sử dụng vào câu lệnh:

     influx -host YOUR_INFLUX_SERVICE_IP -port 8086

Để vào database shell, tại đây có thể thao tác với database.
### 3. Làm việc với giao diện Grafana

Sau khi đã chạy file grafana_deployment.yaml, grafana_service.yaml. Sử dụng câu lệnh
sau để lấy thông tin về service Grafana.

     kubectl describe service monitoring-grafana --namespace=kube-system

Sẽ xuất hiện 1 loạt thông tin vể service, trong đó sẽ bao gồm 1 thông tin về
endpoint.

VD: Endpoints:   10.1.31.2:3000

Nhập địa chỉ này trên trình duyệt web sẽ vào được, và sử dụng Grafana.
