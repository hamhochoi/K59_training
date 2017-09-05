# **report 2: init Systemd**
## cách tìm các file cấu hình của 1 service
- Tìm trong thư mục etc/ nơi chứa các tập tin cấu hình của hệ thống.

## chọn service Postgresql
- cài đặt:
           apt-get update//update apt-get repository
           sudo apt-get install postgresql postgresql-contrib
- các file cấu hình của service:

lưu trong etc/postgres/9.6/main

           postgresql.conf
           pg_hba.conf
           start.conf

  - enable/disable service:(tạm thời)
           sudo service postgresql start
          sudo service postgresql stop

- enable/disable (automatically), qua systemd
           sudo systemctl enable <tên app>.service
           sudo systemctl disable <tên app>.service
