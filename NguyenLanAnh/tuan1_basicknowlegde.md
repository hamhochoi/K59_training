# **Report 1**
# LINUX
Đây là một hệ điều hành nhân Linux mã nguồn mở, do Linus Torvalds tạo ra. Linux kiểu như 1 hệ điều hành Unix đã được modun hóa. Sau một khoảng thời gian ngắn phát triển, từ phiên bản Linux đầu tiên, hiện tại đã có nhiều  phiên bản Linux (Distro)mà phổ biến nhất có thể nhắc tới là : Ubuntu, Fedora,Debien, Linux Mint,...
## Tổng quan, cài đặt Linux
Có nhiều lí do để nhiều người chọn Linux trở thành hệ điều hành chính trên máy tính của mình, và đặc biệt là những lập trình viên, có thể kể đến những lí do cơ bản sau:
- Về vấn đề bản quyền, chi phí: Linux thuộc phần mềm mã nguồn mở nên người sử dụng không cần phải lo lắng nhiều về vấn đề bản quyền, đồng thời chi phí cho những phần mềm kiểu này là ít hoặc free.
- Linux là một hệ điều hành linh hoạt, uyển chuyển, bởi nó là 1 hệ điều hành mã nguồn mở nên bản thân người dùng có thể tùy chỉnh, thay đổi, sửa chữa theo ý mình nếu có đủ khả năng. Tính linh hoạt, uyển chuyển của hệ điều hành còn thể hiện ở chỗ nó tương thích với nhiều môi trường: Môi trường máy chủ, desktop, nhúng vào các thiết bị điều khiển,...
- Linux mang tính an toàn, bảo mật cao: Linux có một cơ cấu phân quyền người sử dụng hết sức chặt chẽ: Chỉ có những root mới có quyền can thiệp vào hệ thống để cài đặt và thay đổi. Bên cạnh đó Linux cũng có chế độ cho phép một người dùng bình thường có khả năng sử dụng quyền của root trong một khoảng thời gian cho một số hành động. Cơ chế phân quyền như này giúp tránh khỏi những sai sót, đổ vỡ trong hệ thống.
Tính chất mở một lần nữa thể hiện điểm mạnh của mình, khi nó giúp Linux tăng sự an toàn hệ thống, khi một lỗ hổng bị phát hiện, thì nó sẽ được cả cộng đồng mã nguồn mở tham gia sửa chữa, trong 1 thời gian ngắn, lỗ hổng đó sẽ được fix. Bên cạnh đó, vì người quản trị cũng nhìn thấy được từng ngõ ngách của hệ thống nên cũng phần nào đảm bảo được sự an toàn.
- Thích hợp cho việc quản trị mạng: Bởi vì ngay từ đầu được tạo ra cho chế độ đa người dùng, nên Linux được coi là hệ điều hành mạng rất có giá trị: Tính bảo mật cao, chạy ổn định.
- Chạy thống nhất trên các hệ thống phần cứng: Mặc dù có rất nhiều phiên bản Linux khác nhau do các nhà phân phối khác nhau ban hành nhưng nhìn chung chúng đều chạy khá ổn định trên các thiết bị phần cứng.
## Tiêu chuẩn phân cấp hệ thống file
Cấu trúc tập tin trong Linux được tổ chức theo một hệ thống phân bậc tương tự cấu trúc của 1 cây phân cấp, với bậc cao nhất là thư mục gốc, kí hiệu "/". Tất cả các tập tin, thư mục đều nằm dưới thư mục gốc.
Nằm dưới thư mục gốc (/)có một loạt các thư mục quan trọng của hệ thống tập tin:
![cây thư mục](http://i.imgur.com/vCKSmWt.png)
trong đó
- /(root): thư mục gốc, chỉ có root user mới có quyền viết dưới thư mục này.
- /bin: chứa các chương trình thực thi. chương trình chung của Linux cho tất cả người dùng được lưu ở đây, VD: ls, ping, ps, cp,...
- /sbin: cũng chứa các chương trình thực thi, nhưng đó là những chương trình dành cho admin, cho việc bảo trì hệ thống, VD: reboot, ifconfig,...
- /etc: chứa các tập tin cấu hình hệ thống, đống thời còn chứa các shell script dùng để khởi động hoặc tắt các chương trình khác. VD:/etc/resolv.conf, ...
- /proc: chứa thông tin về các tiến trình đang chạy dưới dạng 1 hệ thống file thư mục mô phỏng. VD: thư mục con /proc/{pid}chứa các thông tin về tiến trình có id là pid. bên cạnh đó đây cũng là nơi lưu thông tin về các tài nguyên đang được sử dụng của hệ thống.
- /usr: chương trình của người dùng. chứa các file thư viện,file thực thi, tài liệu hướng dẫn.
  1. /usr/bin: chứa các file thực thi của người dùng như : at,awk,cc,less,...
  2. /usr/sbin: chứa các file thực thi của hệ thống dưới quyền admin: atd, cron,.
  3. /usr/lib: chứa các thư viện cho các chương trình trong /usr/bin, /usr/sbin
  4. /usr/local: chứa các chương trình của người dùng được cài từ mã nguồn
- /home: thư mục chính lưu trữ các tập tin cá nhân của tất cả user
- /boot: chứa các tập tin cấu hình cho quá trình khởi động hệ thống.
- /dev: Các file thiết bị. Các phân vùng ổ cứng, thiết bị ngoai vi như USB, ổ đĩa cắm ngoài, bất kì thiết bị gắn kèm vào hệ thống đều được lưu ở đây.
- /tmp: chứa các file tạm thời được tạo bởi hệ thống và người dùng. các file lưu trong thư mục này sẽ bị xóa khi hệ thống khởi động lại
- /var: thông tin về các biến của hệ thống được lưu tại đây. như thông tin về log file: /var/log, các gói và cơ sở dữ liệu /var/lib
- /lib: thư viện hệ thống, thư viện hỗ trợ cho các file thực thi trong /bin, /sbin
- /opt: Các ứng dụng phụ tùy chọn. chứa các ứng dụng thêm vào từ các nhà cung cấp độc lập khác. chúng có thể được cài ở /opt hoặc thư mục con của /opt
- /mnt: thư mục để mount. thư mục tạm để mount các file hệ thống
- /media: các thiết bị gắn có thể gỡ bỏ. thư mục tam này chứa các thiết bị như CdRom/media/cdrom hay các phân vùng đĩa cứng /media/Data (D:/Data trong window)
- /srv: dữ liệu của các dịch vụ khác. chứa dữ liệu liên quan đến các dịch vụ máy chủ như /srv/svs, chứa các dữ liệu liên quan đến CVS.
![vd](http://i.imgur.com/AawXaw6.png)
## bash shell
- shell là 1 chương trình đặc biệt, chấp nhận các câu lệnh và chuyển đến kernel để xử lí, sau đó trả lại kết quả cho người dùng, thông dịch các lệnh của người dùng nhập vào hoặc từ các file. thực tế, shell không phải một phần của hạt nhân hệ thống, nó chỉ dùng hạt nhân để thực thi các chương trình, tạo ra các tập tin.
các shell script: bash, csh, ksh, tcsh,...
sử dụng câu lệnh : "echo $SHELL" để biết hệ thống đang chạy shell gì.
1 số câu lệnh thiết lập quyền, thực thi chương trình shell:
"chmod o+x tên file"//câu lệnh thiết lập quyền
"bash tên file"//các câu lệnh thực thi
"sh tên file"// thực thi file
"./tên file"// thực thi file

1.Biến trong shell
- Biến hệ thống: biến được tạo ra và quản lí bởi Linux, tên biến viết hoa.
- Biến do người dùng định nghĩa: Biến được tạo ra và quản lí bởi người dùng, tên biến viết thường.
- $tên biến
  VD: echo $bien // để hiển thị gt biến
- định nghĩa các biến người dùng:
      tên biến = giá trị
VD: n = 9
- bên cạnh đó cũng có các quy tắc đặt tên biến: tên biến phải bắt đầu bằng kí tự, không được để dấu cách 2 bên toán tử bằng, phân biệt chữ hoa chữ thường, khi biến không được khởi tạo sẽ có giá trị mặc định là NULL, không có các kí tự "?" hay " * " trong tên biến.

2.Các phép toán
- thực hiện các phép tính số học cần dùng câu lệnh: expr
trong đó có các toán tử: +, -, \*, /,%
              VD: expr 5\*8
- Đối với cặp dấu '' sẽ yêu cầu thực hiện lệnh
              VD: echo 'expr8+9'
ngược lại đối với dấu "", tất cả các kí tự trong cặp dấu này sẽ ko có ý nghĩa tính toán, trừ những kí tự \ hoặc $

3.Các cấu trúc rẽ nhánh
- Câu lệnh if...then
          if điều kiện
          then
                câu lệnh
          fi
Tương tự với câu lệnh if...then...else

4.Các phép toán kiểm tra
- Các phép toán kiểm tra
![toán kiểm tra](http://i.imgur.com/pfp8y1a.png)
- Các phép so sánh xâu
![so sánh xâu](http://i.imgur.com/wIKu3gO.png)
- Phép kiểm tra file, thư mục
![kiểm tra file, thư mục](http://i.imgur.com/Si8Z7Lv.png)
- Các phép toán logic
      not: !biểu thức
      and: -a
      or: -r

5.Các cấu trúc lặp
- lặp for
           for<tên biến>in<danh sách>
           do<các câu lệnh>
           done

hoặc:

          for(gt1;gt2;gt3)
          do<các câu lệnh>
          done

         VD:
          for i in 1 2 3 4
          do
          echo "Hello World"
          done

- lặp while
         while < điều kiện>
         do < các câu lệnh>
         done

- Cấu trúc case:
        case $tên_biến in
        pattern2)câu lệnh;;
        * ) câu lệnh;;
        esac
## init System
- init process là tiến trình được khởi động đầu tiên trong hệ thống. nhiệm vụ của init là start, stop các process services. Nó là tiến trình được khởi động lên đầu tiên trong hệ thống nên init process luôn có PID(Process ID)là 1
- có 3 kiểu triển khai init trong hệ thống Linux là:

        System V (cũ)
        Upstart
        Systemd
init Systemd không chỉ dừng lại ở việc start/stop các services nó còn có thể mount filesystems, quản lí network sockets,...quản lí các công việc như thế, Systemd phân chia ra các đơn vị units:
         Service units(.service)để start và stop các unit
         Mount units(.mount) để quản lí các mount point
         Target unit(.target)để điều khiển các runlevels(sử dụng trong sysV init)
trong khi ở SysV init System có các runlevels:
               0 - halt
               1 - single-user
               2 - multi-user
               3 - multi-user with networking
               4 - user defined
               5 - multi-user with display manager(graphical login)
               6 - reboot

Thì Systemd khái niệm runlevels được thay thế bằng các targets để boot vào như:
     poweroff.target - shutdown system
     rescue.target - single user mode
     multi-user.target - multiuser with networking
     graphical.target - multiuser with networking and GUI
     reboot.target - restart

# Git
## cơ bản về Git
- Git là một phần mềm quản lí mã nguồn phân tán, ban đầu dành cho việc phát triển nhân Linux. Hiện nay, nó trở thành một trong các phần mềm quản lí mã nguồn phổ biến nhất.
- Các khái niệm cơ bản trong git:
     **repository**:(repo)đây là nơi chứa tất cả thông tin cần thiết để duy trì và quản lí các sửa đổi và quản lí dự án. repo có 2 cấu trúc dữ liệu chính là object store và index. tất cả dữ liệu của repo đều được chứa trong thư mục đang làm việc dưới dạng folder ẩn có tên là .git.
     **object store**: là trái tim của git, nó chứa những dữ liệu gốc, các file log ghi chép quá trình sửa đổi, tên người tạo file, ngày tháng,....Git có 4 loại objects: blobs, trees, commits, tags
     blobs: file nhị phân có thể chứa mọi loại dữ liệu bất kể là dữ liệu của chương trình gì
     trees: lớp đại diện cho thông tin thư mục như thông tin định danh của blob, đường dẫn , metadata chứa thông tin cấu trúc và các thư mục nhỏ chứa trong thư mục đó.
     commits: chứa metadata có thông tin về mọi thứ như tên tác giả, người tải lên, ngày tải, thông tin log,...
     tags: đánh dấu
     **index**: file nhị phân động tạm thời miêu tả cấu trúc thư mục của toàn bộ repo và trạng thái của dự án được thể hiện thông qua commits và trees tại 1 thời điểm nào đó trong lịch sử phát triển. index không chứa nội dung file mà chỉ dùng để truy tìm những thứ mà bạn muốn commits
- Một số website, phần mềm cho phép lưu trữ Git:
             GitHub
             GitLab
             GNU Savannah
             ...
- Cơ chế lưu trữ phiên bản của Git là nó sẽ tạo ra 1 snapshot trên mỗi tập tin và thư mục sau khi commit, từ đó cho phép bạn tái sử dụng lại 1 ảnh chụp nào đó mà có thể hiểu đó như là 1 phiên bản.

## Cài đặt Git
- cài đặt Git trên Ubuntu

sử dụng lệnh sau để cài đặt Git:
         sudo apt-get install git
Thiết lập chứng thực cá nhân:
         git config --global user.name "tên"
         git config --global user.email "tên mail"

- Tạo repository:

có 2 loại repo: local và remote, với  kho chứa trên máy cá nhân và kho chứa trên máy chủ từ xa.
         Tạo local: git init tên_file
         Tạo remote: trên Github
Sau khi tạo xong 1 repo trên Github sẽ có 1 đường dẫn đến repo này, và khi muốn clone kho về máy, sử dụng câu lệnh:
          git clone <địa chỉ>
sau khi clone về máy, ta có thể thay đổi tùy ý và sau đó có thể đẩy lên Github bằng câu lệnh:
           git push origin master

## SVN
Bên cạnh Git - 1 version control còn có SVN (subversion). Đây cũng là 1 version control được sử dụng phổ biến hiện nay. kho plugin WordPress cũng đang sử dụng SVN   

Nó làm việc với 1 máy chủ trung tâm kho mã nguồn, những kho đó được chia vào 3 key chính là : Trunk,Branches,Tags, trong đó:

- TRunk:

là nơi lưu trữ mã nguồn gốc, như khu vực trung tâm nới bất cứ ai làm việc trong dự án sẽ lấy các cập nhật tại đây. khi làm việc với 1 tính năng mới bạn sẽ branches mã nguồn từ trunk, sau khi tính năng đó được hoàn thành, nó sẽ được đưa vào trunk.

- Branches:

Sử dụng khi tạo ra tính năng mới, vì vậy sẽ branch mã nguồn từ trunk. Điều này có nghĩa là sẽ lấy được ra bản sao chép trunk và đặt trong 1 folder mới bên trong khu vực branch, và tạo những thay đổi trên folder đó. sau khi hoàn thành sẽ đưa những thay đổi đó vào trunk.

- Tags:

Nó cũng là 1 phương án tạo mã nguồn. Sự khác nhau ở đây là tag sẽ không bao giờ sử dụng cho phát triển mã nguồn, chúng chỉ là phương án dễ dàng cho việc lấy lại mã nguồn. thời điểm sử dụng tag là cho việc triển khai mã nguồn, khi hoàn thành những mã nguồn mới, merge vào trunk và đánh dấu tính năng mới đó. lợi ích làm việc này là nếu bản phát hành mới đổ vỡ, có thể lấy lại mã nguồn quay trở lại thời điểm tag trước đó.

Mỗi loại version control này có những đặc điểm , lợi ích riêng nên tùy từng yêu cầu, sở thích từng người để chọn cho mình những loại quản lí phiên bản phù hợp.

# end
