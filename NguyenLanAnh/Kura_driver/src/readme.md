## Kura driver

- KuraOSGi chứa file Activator, khởi động OSGi plugin. [tạo OSGi project](https://eclipse.github.io/kura/dev/hello-example.html)
- maven chứa file Receiver, Sender là những file chính thực hiện nhiệm vụ gửi, nhận message giả lập, file pom.xml chưa những cấu hình cho libraries cần thiết. Trong đó sử dụng thư viện JMS(java message service)_cho phép gửi nhận thông tin một cách bất đồng bộ, và ActiveMQ (một message oriented middleware) quản lí message queue.

KuraOSGi project và maven project sẽ được liên kết với nhau, sử dụng Maven Tycho [OSGi+maven](http://o7planning.org/vi/10137/thiet-lap-du-an-java-osgi-voi-maven-va-tycho)

- 2 project được lên kết với nhau thông qua file cấu hình pom.xml
