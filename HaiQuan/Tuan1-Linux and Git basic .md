# Báo cáo tuần 1

## Phần 1: Hệ Điều Hành Linux


### 1. Filesystem Hierarchy Standard

Trong hệ điều hành Linux các tệp và các thư mục kết hợp tạo thành một cây duy nhất có thư mục gốc ký hiệu là / và được gọi là thư mục gốc

Các thư mục con thường gặp của thư mục gốc là: 


- **/bin**: chứa các chương trình thực thi có thể được sử dụng bởi tất cả người dùng. Vd: cat, ls, mkdir, ps...

- **/sbin**: lưu trữ các tiện ích dành cho admin của hệ th

- **/boot**: bao gồm tất cả những thứ cần cho tiến trình khởi động hệ thống

- **/dev**: lưu trữ các file đặc biệt hay file thiết bị 

- **/etc**: chứa các file cấu hình của hệ thống và phần mềm

- **/home**: chứa các file cá nhân của người dùng

- **/lib**: chứa các thư viện hỗ trợ cho các file thực thi trong /bin và /sbin. Các thư viện này thường bắt đầu bằng ld\* hay lib\*.so.\*

- **/media**: thư mục này chứa các thư mục con được sử dụng để làm điểm kết nối cho các thiết bị như đĩa mềm, cdrom hay đĩa zip

- **/mnt**: thư mục này để mount các file hệ thống

- **/opt**: được dành riêng để chứa các ứng dụng thêm vào từ các nhà cung cấp khác. Ứng dụng có thể được lưu trong /opt hoặc trong thư mục con của /opt

- **/root**: là thư mục home của root user

- **/srv**: chứa các dịch vụ liên quan đến máy chủ

- **tmp**: chứa các file tạm thời của hệ thống và người dùng. Các file lưu trong mục này sẽ bị xóa khi hệ thống khởi động lại

- **/usr**: chứa các chương trình của người dùng
	- **/usr/bin**: chứa các file thực thi của người 
	- **/usr/sbin**: chứa các file thực thi của hệ thống dưới quyền admin 
	- **/usr/lib**: chứa các thư viện cho các chương trình trong /usr/bin và /usr/sbin
	-  **/usr/local**: chứa các chương trình người dùng cài từ mã nguồn
	- **/usr/share**: chứa các chương trình hay package nào có dữ liệu là cố định

- **/var**: bao gồm thông tin về các biến của hệ thống

- **/proc**: chứa các thông tin của B


### 2. Bash shell

Shell là trình thông dịch lệnh của Linux thường tương tác với người dùng theo từng câu lệnh. Shell đọc lệnh từ bàn phím hoặc từ file.

Bash shell là một loại shell thông dụng trên Linux. Để thực thi 1 Shell Script ta sử dụng:

~~~
	bash đường_dẫn_tới_file
~~~

Trong Linux shell có 2 loại biến:

- Biến hệ thống: Tạo ra và được quản lý bởi Linux. Tên biến là **CHỮ HOA**

- Biến do người dùng định nghĩa: tạo ra và quản lý bởi người dùng. Tên biến là **chữ thường**. Cú pháp:
~~~
	tên_biến=giá_trị 
~~~

 Không được sử dụng dấu ?, * để đặt tên cho các biến. Để xem hoặc truy cập giá trị các biến ta sử dụng ký hiệu $TênBiến. Một biến mà không được khởi tạo sẽ có giá trị là NULL.

**Một số câu lệnh cơ bản:** 

- In kết quả ra màn hình
~~~
	echo [option] [string, variables...] 
~~~

- Thực hiện các phép toán số học
~~~
	expr biểu_thức_số_học
	
	Chú ý: các toán tử là: +, -, \*, /, % 
~~~

- Đọc dữ liệu từ đầu vào 
~~~
	read tên_biến_nhận_giá_trị 
~~~

- Câu lệnh if
~~~
	if điều_kiện
	then
		câu lệnh 1 
		....
	else
		câu lệnh 2
		.....
	fi
~~~

- Câu lệnh kiểm tra một biểu thức là đúng hay sai 
~~~
	test [biểu thức] 
	
	Chú ý: biểu thức ở đây có thể bao gồm: số nguyên, các kiểu tệp, xâu ký tự 
~~~

- Cấu trúc lặp for
~~~
	for { tên_biến } in {danh sách các phần tử }
	do
		Các câu lệnh
		.....
	done 
	
~~~

- Cấu trúc lặp While
~~~
	while [ điều kiện ]
	do
		Các câu lệnh
		.....
	done 
~~~

- Cấu trúc case
~~~
	case $tên_biến in
		pattern1) 
			Các câu lệnh
			;;
		pattern2)
			Các câu lệnh
			;;
		...
	esac 
	
~~~


### 3. Init System 

#### Init System là gì?

Quá trình khởi động của máy tính bắt đầu khi có tín hiệu bật máy, BIOS được thực hiện. Chương trình này kiểm tra các thiết bị phần cứng cơ bản của hệ thống. Nếu lỗi thì sẽ báo cho người sử dụng, hoặc tắt máy nếu không thể khắc phục. Nếu không hệ thống sẽ thực hiện khởi động theo chế độ mặc định, tìm kiểm một thiết bị lưu trữ để có thể tải nhân HĐH . Để có thể tải hệ điều hành các hệ thống thường sử dụng sector đầu tiên trên các thiết bị lưu trữ (Master Boot Record). Trong sector này sẽ chứa một chương trình con sẽ khởi động toàn bộ quá trình tải nhân hệ điều hành. Chương trình này sẽ tìm ra các phân vùng tích cực ( chứa hệ điều hành ) (chương trình con có thể là GRUB, LILO...) để tải hệ điều hành 

Trong những năm gần đấy BIOS và MBR đang dần được thay thế bằng UEFI và GPT

So sánh MBR và GPT :

|MBR|GPT|
|-------|--------|
|Hỗ trợ ổ cứng tối đa 2.2TB|Hỗ trợ ổ cứng tối đa 9.4ZB|
|Hỗ trợ tối đa 4 phân vùng trên mỗi ổ đĩa|Hỗ trợ tối đa 128 phân vùng ổ đĩa|
|Có thể sử dụng trên cả máy dùng BOIS hay UEFI| Chỉ dùng trên các máy tính có UEFI|

So sánh BOIS và UEFI :

|BOIS|UEFI|
|------|------|
|Không hỗ trợ GPT|Hỗ trợ cả MBR và GPT|
|Tốc độ khởi động trung bình|Tốc độ khởi động nhanh|


Init System là tiến trình đầu tiên chạy khi mà nhân Linux được kích hoạt. Process ID của Init System luôn là 1. Nó phải khởi động tất cả các tiến trình, dịch vụ cần thiết để hệ điều hành hoạt động.

Sau quá trình khởi động, Init System vẫn chạy. Nó có thể được sử dụng để quản lý các tiến trình đã được kích hoạt và đồng ý kích hoạt, hủy bỏ hay khởi chạy lại tiến trình khi hệ điều hành đang hoạt động


#### Điều khiển hệ thống với systemd 

Systemd là một kiểu của Init System được phát triển để thay thế các phiên bản Init System cũ. Nó được phân chia thành các phần gọi là "unit" để quản lý hệ thống dễ dàng hơn. Có nhiều kiểu Unit nhưng phổ biến nhất là 2 kiểu: *service units* và *target units*

- *Service Units* : chức năng chỉnh để kích hoạt và giám sát các service. Các thao tác này được thực hiện bằng câu lệnh:

~~~

	sudo systemctl [tùy_chọn] tên_service.service 
	
Tùy chọn thường dùng:
- start: kích hoạt một service 
- stop: dừng một service
- status: cung cấp thông tin về service
- restart: khởi động lại service 
- enable: kích hoạt service khi khởi động hệ thống
- disable: vô hiệu hóa service khi khởi động hệ thống
- cat: hiển thị unit file mà systemd nạp vào hệ thống 
- mask: ngăn chặn việc khởi động service 
- unmask: cho phép có thể khởi động service 
- edit: thay đổi nội dung unit file 
~~~

- *Target Units*: được sử dụng để liên kết tới các units khác với mục diễn tả trạng thái của hệ thống. Có các kiểu target như:

	- poweroff.target: tắt hệ thống
	
	- rescue.target: chế độ một người sử dụng
	
	- multi-user.target: chế độ nhiều người sử dụng có kết nối mạng
	
	- graphical.target: chế độ nhiều người sử dụng có kết nối mạng và giao diện đồ họa 
	
	- reboot.target: khởi động lại
	
	Ngoài ra người dùng có thể tự định nghĩa các `target` mới 


## Phần 2. Git

### 1. History of Version control system

Quản lý phiên bản( Version control system - VSC ) là một hệ thống lưu trữ các thay đổi của một tập tin ( file ) hoặc một tập hợp các tập tin theo thời gian, do đó nó có thể giúp bạn quay lại một phiên bản xác định nào đó trong quá khứ. Một VSC có thể cho phép bạn khôi phục lại phiên bản cũ của các file, hay toàn bộ dự án, xem lại các thay đổi đã được thực hiện theo thời gian, xem ai là người thực hiện thay đổi gây ra sự cố...

Quá trình phát triển:

Cơ chế quản lý phiên bản 1 cách thô sở nhất đó là copy các file sang một thư mục khác. Đây là 1 phương pháp phổ biến vì nó đơn giản nhưng hay gây ra lỗi và nhầm lẫn. Để giải quyết vấn đề này thì người ta cho ra đời các phiên bản VCS cục bộ có chứa 1 database đơn giản để lưu trữ tất cả những sự thay đổi của file. Vấn đề gặp phải đó chính là khi cần cộng tác với các lập trình viên khác trong hệ thống
=>> Hệ Thống Quản Lý Phiên Bản Tập Trung ra đời. Lợi thế của mô hình này là rất lớn so với quản lý cục bộ tuy nhiên vẫn còn một số nhược điểm là nếu máy chủ trung tâm bị lỗi thì trong khoảng thời gian đó không thể truy xuất dữ liệu và làm việc cùng nhau, có thể mất hết toàn bộ dữ liệu nếu lỗi nghiêm trọng
=>> Hệ Thống Quản Lý Phiên Bản Phân Tán ra đời đã khắc phục được các nhược điểm trên 

### 2. Basic Git command and workflow

Mỗi tệp tin trong Git được quản lý dựa trên ba trạng thái: committed, modified, và staged. Committed có nghĩa là dữ liệu đã được lưu trữ một cách an toàn trong cơ sở dữ liệu. Modified có nghĩa là bạn đã thay đổi tệp tin nhưng chưa commit vào cơ sở dữ liệu. Và staged là bạn đã đánh dấu sẽ commit phiên bản hiện tại của một tập tin đã chỉnh sửa trong lần commit sắp tới. Điều này tạo ra ba phần riêng biệt của một dự án sử dụng Git: thư mục Git (git directory), thư mục làm việc(working directory), và khu vực tổ chức (staging area).

![](https://git-scm.com/figures/18333fig0106-tn.png) 


Tệp tin trong `working directory` có thể có 2 trạng thái: `tracked` hoặc `untracked`. Tệp tin `tracked` là tệp tin đã có mặt trong `snapshot` trước, chúng có thể là `unmodified`, `modified`, hoặc `staged`. Tệp tin `untracked` là các tập tin chưa có trong một `snapshot` trước hay trong `staging area`. Ban đầu khi tạo ra `clone` một repository thì tất cả các tệp tin sẽ ở trạng thái `tracked` và `unmodified` vì bạn mới tải chúng về và chưa thực hiện bất kỳ thay đổi nào. Khi bạn chỉnh sửa các tệp tin này thì bạn phải `stage` các tệp tin này và `commit` lại chúng 

![](https://git-scm.com/figures/18333fig0201-tn.png) 

**Tiến trình công việc (workflow)**:

- Thay đổi các tệp tin trong thư mục làm việc
- Tổ chức các tệp tin, đẩy vào Staging Area
- Commit để đẩy dữ thông tin từ Staging Area vào thư mục git để lưu trữ
- Đẩy dữ liệu lên remote repository 


**Các câu lệnh cơ bản:**

- Khởi tạo một Git Repository
~~~
	git init 
~~~

- Sao chép (clone) một repository
~~~
	git clone đường_dẫn_đến_repository 
~~~

- Kiểm tra trạng thái của tệp tin
~~~
	git status 
	
	Chú ý: có 4 trạng thái có thể trả về là: untracked, unmodified, modified, staged 
~~~

- Theo dõi tệp tin
~~~
	git add tên_tệp_tin 
	
hoặc: 

	git add * (để theo dõi tất cả file) 
~~~

- Commit thay đổi
~~~
	git commit -m "Thêm ghi chú"
~~~
- Kết nối để Remote Repository 
~~~
	git remote add <tên-máy-chủ> <url > 
	
~~~

- Đẩy dữ liệu lên Remote Repository
~~~
	git push <tên máy chủ> <tên nhánh> 
~~~
- Xem lịch sử Commit
~~~
	git log 
~~~

- Loại bỏ tệp tin trong Staging Area
~~~
	git reset HEAD <file> 
~~~

- Tạo một nhánh (branch) 
~~~
	git branch <tên_nhánh> 
~~~
- Xóa một nhánh 
~~~
	git branch -d <tên_nhánh> 
~~~
- Truy cập vào một nhánh 
~~~
	git checkout <tên_nhánh> 
~~~
- Hiển thị danh sách các nhánh (branch)
~~~
	git branch 
~~~
- Gộp nhánh vào nhánh hiện tại
~~~
	git merge <tên_nhánh_cần_gộp> 
~~~


### 3. Compare to SVN,...

Sự khác nhau cơ bản giữa Git và các VCS khác là: 

- Phần lớn các hệ thống khác lưu trữ thông tin dưới dạng danh sách các tệp tin được thay đổi. Các hệ thống này coi thông tin lưu trữ là một tập các tệp tin và thay đổi được thực hiện trên mỗi tập tin theo thời gian

- Git coi dữ liệu của nó giống như tập hợp của các "snapshot" của một hệ thống tập tin nhỏ. Mỗi khi bạn "commit" nó sẽ lưu lại một "snapshot" ghi lại nội dung của tất cả các tệp tin tại thời điểm đó. Để hiệu quả hơn thì nếu ko có sự thay đổi nào nó sẽ tạo một liên kết tới tập tin đã tồn tại trước đó



		