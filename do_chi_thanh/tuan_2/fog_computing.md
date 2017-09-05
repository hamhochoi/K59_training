# Fog Computing

* Khái niệm: Fog Computing là một kiến trúc nối dài của Cloud Computing ra mạng biên
* Trong Fog computing, dữ liệu được sinh ra từ sensors sẽ được xử lý local chứ không truyền thẳng lên Cloud.
* Các quá trình phân tích, xử lý dữ liệu; quản lý các thiết bị đều được xử lý tại local; 
* Dữ liệu sinh ra sẽ được gửi đến Fog, được tính toán real-time, lưu trữ tạm thời và định kỳ được tổng hợp lại và gửi lên Cloud.
* Lý do xuất hiện Fog Computing: Do Cloud Computing không đáp ứng được một số ứng dụng đòi hỏi độ trễ về mạng nhỏ, nên cần đưa ra một mô hình giải quyết được vấn đề trên

* Các ưu điểm của Fog Computing so với Cloud Computing: 
    * Do xử lý cục bộ nên độ trễ mạng nhỏ, có thể dự đoán được, phù hợp với các ứng dụng xử lý thời gian thực.
    * Độ an toàn cao hơn Cloud computing do các dữ liệu được gửi giữa Fog và Cloud được mã hóa
    * Tiêu thụ lượng băng thông ít hơn
    * Loại bỏ được hiện tượng thắt cổ chai bottle-neck do dữ liệu không cần truyền tới chỉ một kho dữ liệu
    * Loại bỏ được single point of failure (một thành phần quan trọng mà khi nó bị lỗi ảnh hưởng tới hoạt động của cả hệ thống).
 
* Nhược điểm của Fog Computing: 
    * Do việc xử lý dữ liệu được thực hiện local nên cần thiết bị phần cứng để xử lý, dẫn đến việc dư thừa tài nguyên so với tính chất pay-as-you-go trong cloud computing
    * Yêu cầu nhiều người để cài đặt, duy trì hơn cloud computing.
 
* Các vấn đề trong Fog Computing
    * Fog Network: Quản lý mạng fog, duy trì kết nối, cung cấp dịch vụ.
    * Quality of Service: Đảm bảo chất lượng dịch vụ dựa trên 4 tiêu chí: 
        * Tính kết nối
        * Tính sẵn dùng
        * Khả năng
        * Độ trễ
    * Interfacing and programming model: Thống nhất mô hình liên kết và lập trình
    * Computation offloading: Giảm tải công việc tính toán cho fog node: Do Fog Node là các thiết bị có khả năng hạn chế về mặt tính toán, xử lý dữ liệu, do đó, một phần công việc tính toán nặng nhọc phải được gửi lên cloud để thực hiện. Vấn đề là phải xác định được khi nào thì gửi yêu cầu lên cloud.
    * Accouting, billing, monitoring: Giám sát, thanh toán chi phí dịch vụ.
    * Provisioning and resource managerment: Cung cấp và quản lý tài nguyên.
    * Security and Privacy: An toàn và bảo mật. 
         * Trust Model: Người dùng phải chọn nhà cung cấp cho dịch vụ của mình, do đó cần một mô hình xác định các nhà cung cấp tin cậy. Các nhà cung cấp dịch vụ fog computing có thể là:
               1. Nhà cung cấp dịch vụ internet
               2. Nhà cung cấp dịch vụ Cloud Computing
               3. Người dùng sở hữu các private cloud, muốn chuyển đổi sang fog và cho thuê các tài nguyên dư thừa.
         * Rogue Fog Node: Các phát hiện một fog node giả mạo
         * Authentication: Vấn đề xác thực: Các thiết bị gửi dữ liệu lên fog node cần xác thực fog node đó đúng là fog node đích, fog node cần xác thực các thiết bị gửi dữ liệu lên không bị giả mạo; xác thực trong quá trình gửi dữ liệu giữa fog node và cloud.
         * Network security: Vấn đề an toàn mạng không dây trong fog network.
         * Secure data storage: Đảm bảo an toàn kho dữ liệu
         * Secure and Private data computation: Đảm bảo an toàn, bảo mật cho dữ liệu tính toán.
         * Privacy
         * Access Control: Do các mô hình điều khiển truy nhập sẵn có không phù hợp với mô hình của fog nên cần đưa ra các mô hình điều khiển truy nhập mới phù hợp hơn.
         * Intrust detection: Phát hiện truy cập trái phép
 

* Tham khảo: 
    1. https://www.quora.com/What-are-the-drawbacks-of-fog-computing-in-IoT
    2. https://www.quora.com/Are-there-any-draw-backs-dis-advantages-of-using-fog-computing-in-Internet-of-Things-IoT
    3. http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.702.7773&rep=rep1&type=pdf
    4. http://www.cs.wm.edu/~zhengrui/papers/wasa15-fog.pdf
