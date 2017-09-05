# Linux
## Installation
### Chuẩn bị trước khi cài
- USB
- File .iso cài đặt Ubuntu
- Phần mềm USB Installer

### Cài đặt
- Boot hệ thống
- Phân chia ổ đĩa
- Cấu hình hệ thống
- Tạo tài khoản sử dụng

### Các kiểu file system
Linux cần ít nhất 2 bảng partition. Một dành cho các tệp của HĐH, bảng còn lại dùng cho vùng nhớ swap

Có khá nhiều dạng file hệ thống trong Linux như ext2, ext3, ext4,... Hiện tại trong Linux phổ biến hai kiểu hệ thống file là ext3 và ext4.

## Filesystem Hierarchy Standard
1. /root  
Thư mục gốc của toàn bộ hệ thống phân cấp.
2. /bin  
Chứa file thực thi dạng binary. Các câu lệnh được sử dụng bởi tất cả các user trong hệ thống sẽ được đặt trong đây
3. /boot  
Chứa các file boot loader , ví dụ: hạt nhân, initrd.
4. /dev  
Chứa các file device để đại diện các hardware. Ví dụ: /dev/sda
5. /etc  
Thông thường ở /etc sẽ chứa file cấu hình cho các chương trình hoạt động. Ví dụ: /etc/network dùng để quản lý dịch vụ network
6. /home  
Chứa đựng thông tin cá nhân của các user
7. /lib  
Thư viện cần thiết cho các chương trình nhị phân trong /bin/và /sbin/
8. /media  
Chứa thư mục dùng để mount cho các thiết bị removable. Ví dụ như CDROM, Floppy...
9. /mnt  
Chứa các thư mục dùng để system admin thực hiện quá trình mount
10. /opt  
Chứa đựng các gói phần mềm tùy chọn
11. /proc  
Chứa đựng thông tin về quá trình xử lý của hệ thống, thông tin về các process đang chạy, thông tin tài nguyên hệ thống
12. /root  
Thư mục home của user root
13. /run  
Thông tin về hệ thống đang chạy kể từ lần khởi động cuối
14. /sbin  
Chứa đựng các file thực thi dạng binary. Các lệnh bên trong /sbin thường được sử dụng bởi system administrator và dùng cho các mục đích là duy trì quản trị hệ thống.
15. /srv  
Chứa đựng các dịch vụ cho server, nó liên quan đến dữ liệu
16. /sys  
Chứa thông tin về các thiết bị kết nối với máy tính.
17. /tmp  
Thư mục này chứa các file được tạo ra bởi hệ thống và user.
18. /usr  
Chứa các file binary, library, tài liệu, source-code cho các chương trình
- /usr/include: Tiêu chuẩn bao gồm tệp
- /usr/lib: Thư viện cho các chương trình nhị phân trong /usr/bin/và /usr/sbin/
- /usr/src: Source code
19. /var  
Chứa đựng các file có sự thay đổi trong quá trình hoạt động của hệ điều hành

## Bash shell (basic)
- Biến: `ten_bien=gia_tri`  
In gía trị của biến: `echo $ten_bien`
- Phép tính toán số học: `expr bieu_thuc_so_hoc`  
Ví dụ: `expr 1 + 1`
- Dấu ngoặc kép ""  
Tất cả các ký tự trong dấu ngoặc kép đều không có ý nghĩa tính toán, trừ những ký tự sau \ hoặc $
- Mảng
    - Khai báo mảng: array=(value1 value2 ...)
    - Lấy toàn bộ phần tử trong mảng: ${a[*]}, ${a[@]}
    - Số phần tử của mảng: ${#a[*]}, ${#a[@]}
    - Độ dài của phần tử trong mảng: ${#a[index]}
    - Thêm phần tử vào mảng: array+=(value3 value4 ...)
- Cấu trúc rẽ nhánh if...else  
    Cú pháp:  
    ```
    if [ dieu_kien ]  
    then  
        cau_lenh_1  
        ...  
    else 
        cau_lenh_2  
    fi
    ```

    Ví dụ:
    ```
    echo "Nhap ten file:"  
    read filename  
    if [ -e $filename ]; then  
        ls -al  
    else  
        echo "Does not exist"  
    fi  
    ```

- Cấu trúc lặp for
    Cú pháp:
    ```
    for((expr1; expr2; expr3))  
    do  
        Cac_cau_lenh  
    done  
    ```

    Ví dụ:
    ```
    sum=0  
    echo "Nhap n:"  
    read n  
    for((i=0; i <= $n; i++)) 
    do  
        sum=$(($sum+$i))  
    done  
    echo "Tong tu 1 -> $n la: $sum"  
    ```

- Vòng lặp while
    Cú pháp:
    ```
    while [ condition ]  
    do  
        command1  
        command2 
        ...  
    done
    ```

    Ví dụ:
    ```
    i=10  
    while [ $i -gt 0 ]  
    do  
        echo $i  
        let i=i-1  
    done
    ```

- Hàm trong bash shell
    ```
    function A() {  
        echo "function A" 
    }  
    function B() {  
        echo $1  
    }  
    A  
    B "function B"
    ```

## Init system(i.e. systemd)
Init process là một tiến trình được khởi động lên đầu tiên trong hệ thống Linux. Tức là sau khi chọn hệ điều hành trong menu của Boot Loader. Hệ điều hành bắt đầu được khởi động và tiến trình đầu tiên khởi động lên là init. Nhiệm vụ của init là start và stop các process, services… cần thiết khác.

Vì init là tiến trình được khởi động đầu tiên của hệ thống Linux nên:  
- Init process luôn có PID (Process ID) là 1.
- Tiến trình init là tiến trình cha của các tiến trình khác.

Có ba kiểu triển khai init system chính trong hệ thống Linux là:
- System V: là phiên bản truyền thống của init system trên nhiều hệ thống Linux.
- Upstart: Được phát triển bởi Canonical vào khoảng năm 2009 và sử dụng trong các phiên bản Ubuntu cũ hơn bản 15.04.
- Systemd: Là một init system được phát triển khoảng năm 2010 và được nhiều Linux distributions sử dụng để thay thế các init system cũ. Ubuntu từ phiên bản 15.04 và Centos từ phiên bản 7 đã sử dụng systemd làm init system mặc định.

### Purpose
- Thay thế các hệ thống init cũ
- Quản lý dịch vụ cho Linux

### Basic usage
#### Cài đặt
- Để cài đặt hệ thống chạy lệnh:  
    ```
    apt-get update  
    apt-get install systemd
    ```

    Cài đặt này sẽ cài đặt gói systemd nhưng sẽ không cấu hình systemd lên hệ thống init.

- Cấu hình để kiểm tra
    Để kiểm tra systemd trước khi chuyển sang mặc định, bạn có thể thêm tham số khởi động sau vào kernel:
    ```
    Init = / bin / systemd
    ```

    Nếu PID 1 là systemd thì hệ thống đang chạy với systemd.

- Cấu hình mặc định
Để sử dụng systemd nên cài đặt systemd-sysv  
`apt-get install systemd-sysv`
Để khởi động hệ thống mới được cài đặt, chạy lệnh  
`reboot`

#### Quản lý dịch vụ với systemd
Systemctl là công cụ chính dùng để kiểm soát trạng thái của hệ thống "systemd" và quản lý dịch vụ

*Một số ví dụ về sử dụng cơ bản*

- Liệt kê tất cả các dịch vụ đang chạy:  
`systemctl`

- Kích hoạt dịch vụ "example1" ngay lập tức:  
`systemctl start example1`

- Hủy kích hoạt dịch vụ "example1" ngay lập tức:  
`systemctl stop example1`

- Khởi động lại dịch vụ "example1" ngay lập tức:  
`systemctl restart example1`

- Hiển thị tình trạng của dịch vụ "example1":  
`systemctl status example1`

- Cho phép "example1" khởi động khi khởi động:  
`systemctl enable example1`

- Tắt "example1" để không bật trong quá trình khởi động:  
`systemctl disable example1`

# Git
Version control system là một hệ thống lưu trữ các thay đổi của một tập tin (file) hoặc tập hợp các tập tin theo thời gian, do đó nó giúp bạn có thể quay lại một phiên bản xác định nào đó sau này. Nó cho phép bạn: khôi phục lại phiên bản cũ của các file, khôi phục lại phiên bản cũ của toàn bộ dự án, xem lại các thay đổi đã được thực hiện theo thời gian, xem ai là người thực hiện thay đổi cuối cùng có thể gây ra sự cố,...


## History of Version control system
- stand-alone and file-focused
    - SCCS: 1972, Unix only
    - RCS: 1982, cross-platform, text only
- centralized
    - CVS: 1986, first central repository, file-focused
    - perforce: 1995, still the biggest repository inside Google
    - subversion: 2000, non-text files, track directory structure, transaction unit = directory
    - Microsoft Team Foundtion Server: 2010, comes with MSDN subcription, tight Visual Studio integration
- Distributed
    - Git: 2005, created by Linus Torvalds after BitKeeper went commercial only. Broadly used in conjunction with GitHub, which offer free hosting for open-source projects
    - Mercurial: 2005, also created in response to BitKeeper change

## Basic Git command and workflow
### Basic Git command
- git init: Tạo một repository mới

    Lệnh: `git init`

- git clone: Sao chép một repository

    Lệnh: `git clone đường_dẫn_repository`

- git branch: Kiểm tra nhánh hiện tại

    Lệnh: `git branch` 

        ```
        Tạo nhánh mới: `git branch tên_nhánh`  
        Xóa nhánh: `git branch -d tên_nhánh`
        ```

- git checkout: Chuyển nhánh

    Lệnh: `git checkout tên_nhánh`

- git add: Cập nhật tình trạng các file(thêm, sửa, xóa) trong projects

    Lệnh: `git add tên_file`

- git commit: Xác nhận và lưu những thay đổi của project

    Lệnh: `git commit -m "ghi_chú"`

- git push: Đẩy project lên phía server

    Lệnh: `git push origin tên_nhánh`

- git fetch: Lấy source mới nhất trên server về đè lên source trên máy local

    Lệnh: `git fetch tên_nhánh`

- git pull: Lấy source mới nhất trên server về và tiến hành trộn

    Lệnh: `git pull tên_nhánh`

- git tag: Gán nhãn

    Lệnh: `git tag -a tên_tag -m "ghi_chú"`

### Workflow
**Create a branch**

Khi bạn tạo một branch trong project của mình, bạn đang tạo ra một môi trường mới. Những thay đổi bạn thực hiện trên branch không ảnh hưởng đến master branch

**Add commit**

Khi branch của bạn đã được tạo,  bạn có thể bắt đầu thực hiện thay đổi. Bất cứ khi nào bạn thêm, chỉnh sửa, hoặc xóa một tập tin, bạn đang thực hiện một commit, và thêm chúng vào branch của bạn

Commit cũng tạo ra một lịch sử về công việc của bạn mà người khác có thể làm theo để hiểu bạn đã làm gì và tại sao. Mỗi commit có một thông điệp liên quan, mô tả giải thích tại sao một thay đổi cụ thể đã được thực hiện

**Open a pull request**

Pull request bắt đầu thảo luận về commit của bạn. Bất kỳ ai cũng có thể thấy chính xác những thay đổi nào sẽ được gộp nếu họ chấp nhận yêu cầu của bạn.

**Discuss and review your code**

Khi Pull request đã được mở ra, người hoặc nhóm xem xét các thay đổi của bạn và có thể có câu hỏi hoặc nhận xét. Nếu có nhận xét rằng bạn đã quên làm điều gì đó hoặc nếu có lỗi trong code, bạn có thể sửa nó trong bracnch của bạn và đẩy những thay đổi lên

**Deploy**

Khi Pull request của bạn đã được chấp nhận, bạn có thể triển khai các thay đổi.

**Merge**

Sau khi merge, Pull request yêu cầu giữ lại bản ghi về lịch sử thay đổi đối với code của bạn. Nó cho phép bất kỳ ai quay trở lại để hiểu tại sao và làm thế nào lại làm như vậy.

### Compare to SVN
Với Subversion, có một vấn đề: Kho SVN có thể ở một vị trí không thể kết nối(không có internet), bạn không thể commit. Nếu bạn muốn tạo một bản sao code của mình, bạn phải sao chép / dán nó theo nghĩa đen.

Với Git thì không có vấn đề trên. Bản sao cục bộ của bạn là kho lưu trữ, và bạn có thể commit. Khi có kết nối với kho chính, bạn có thể commit lại.

Git phức tạp, khó học hơn SVN

Git nhanh hơn so với SVN

Git kiểm soát tốt hơn việc phân chia và hợp nhất

Các branch của git nhẹ và hợp nhất dễ dàng
