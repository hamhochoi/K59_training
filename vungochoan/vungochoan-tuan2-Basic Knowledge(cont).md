# Apache2
1. File cấu hình của service
- apache2.conf: File cấu hình mặc định của apache2, chứa các thông số như timeout, log,...
- ports.conf: Chứa thông tin cổng mà apache2 lắng nghe
- Thư mục conf-available, conf-enabled: Chứa các file cấu hình như security.conf, charset.conf,...

    Tất cả đều nằm trong thư mục /etc/apache2

2. File cấu hình systemd unit của service
- /run/systemd/generator.late/apache2.service
- /lib/systemd/system/apache2.service.d/apache2-systemd.conf

3. Lệnh Enable/disable
- Enable: `systemctl start apache2`
- Disable: `systemctl stop apache2`
- Restart: `systemctl restart apache2`
