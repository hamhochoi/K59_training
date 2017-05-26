#Scheduling in cloud computing

- Bài toán mapping task trong môi trường phân tán thuộc bài toán NP khó, không có thuật toán giải trong thời gian đa thức

- Các vấn đề trong lập lịch trong Cloud Computing[2]
  1. For the set of VMs find the appropriate Physical Machine.
  2. Determine the proper provisioning scheme for the VMs.
  3. Scheduling the tasks on the VMs.

## Thuật toán tham lam Greedy

- Tìm node máy chủ vật lý đầu tiên thỏa mãn yêu cầu của VM và sử dụng máy chủ đầu tiên tìm được
- Sử dụng cạn kiệt tài nguyên của node này trước khi chuyển sang node khác
- Điểm mạnh: Đơn giản, dễ cài đặt do đó nó đã từng được sử dụng trong một thời gian dài trước đây
- Điểm yếu: Lãng phí tài nguyên. Trong khi các node vẫn còn thừa tài nguyên sử dụng, chỉ một node được sử dụng để cài đặt các VM đến khi hết tài nguyên

## First come first servered

- Lưu các yêu cầu vào một hàng đợi
- Xử lý các yêu cầu theo thời gian, lần lượt từ các yêu cầu đến trước được phục vụ trước.





## Thuật toán Round Robin
- Phân bố các VM trên các máy vật lý một cách lần lượt, đều nhau
- Điểm mạnh: Sử dụng các máy chủ vật lý một cách đều nhau
- Điểm yếu: Tiêu thụ năng lượng lớn vì các máy chủ phải bật liên tục.

## Giải thuật di truyền[3]

- Là một giải thuật tìm kiếm một solution cho một task dựa trên chiến lược lựa chọn tự nhiên (nature selection strategy)
- Tìm ra một solution có phẩm chất cao từ một miền tìm kiếm rộng lớn trong thời gian đa thức bằng việc áp dụng nguyên tắc của sự phát triển
- Một giải thuật di truyền bao gồm solution tốt nhất đã tìm được và các solution trong các vùng tìm kiếm mới
- Một giải thuật di truyền sẽ duy trì một số lượng các cá thể được tiến hóa theo các thế hệ
- Phẩm chất của một cá thể được xác định bởi một hàm đánh giá, hàm này chỉ ra độ tốt của một solution so với các solution khác.
- Các bước của một giải thuật di truyền
  - Bắt đầu với một tập các solution khởi tạo ngẫu nhiên
  - Tạo ra một solution dựa trên các genetic operators
  - Đánh giá các cá thể trong dân số
  - Lặp lại bước 2, 3 cho tới khi hội tụ
  

##





Tài liệu tham khảo:
  1. http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.401.8928&rep=rep1&type=pdf
  2. http://ijcsit.com/docs/Volume%207/vol7issue3/ijcsit2016070309.pdf
  3. http://gridbus.csse.unimelb.edu.au/papers/Workflow_JSP_2005.pdf
  
  
  
  
  
  
  
