## Driver reading data for Kura
-  Sử dụng thư viện JMS(java message service), cho phép gửi nhận thông tin một cách bất đồng bộ.

- Test với message queue. Sử dụng ActiveMQ (một message oriented middleware_MOM) để quản lí message queue này.

- Cụ thể tạo 1 pulisher làm nhiệm vụ gửi message, 1 receiver nhận, đọc dữ liệu từ message queue.

- Tạo dự án OSGi project plugin cho việc phát triển ứng dụng Kura.
[tạo OSGi project](https://eclipse.github.io/kura/dev/hello-example.html)

Sử dụng Maven để quản lí các libraries được thêm vào dự án, một cách dễ dàng hơn. Tạo Maven project, và liên kết 2 project với nhau, sử dụng Maven Tycho,[sử dụng Maven cho project](http://o7planning.org/vi/10137/thiet-lap-du-an-java-osgi-voi-maven-va-tycho)

## Dockerfile

Sử dụng để build 1 image.

    docker build -t [ten] . //build image

## Deploy trên k8s

- file kura-rasp.deploy.yaml, deploy cho ứng dụng.
- file kura-rasp.service.yaml, tạo service cho ứng dụng.
- Sử dụng: kubectl create -f [ten]

### End.
