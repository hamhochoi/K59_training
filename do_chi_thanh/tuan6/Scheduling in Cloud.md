# Scheduling in cloud computing

- Bài toán mapping task trong môi trường phân tán thuộc bài toán NP khó, không có thuật toán giải trong thời gian đa thức

- Các vấn đề trong lập lịch trong Cloud Computing[2]
  1. For the set of VMs find the appropriate Physical Machine.
  2. Determine the proper provisioning scheme for the VMs.
  3. Scheduling the tasks on the VMs.


## Các tài nguyên trong Cloud
  - Storage
  - Memory
  - CPU
  - Năng lượng tiêu thụ
  - Băng thông tiêu thụ
  
  
## Các thuật toán Schedule trên tầng Cloud

- Thuật toán lập lịch để giảm tiêu thụ năng lượng
  - http://esatjournals.net/ijret/2014v03/i03/IJRET20140303071.pdf
  
- Thuật toán giảm băng thông tiêu thụ
  - http://cgi.di.uoa.gr/~ad/M155/Papers/ContentICDCS13.pdf: 
  - Tối ưu dựa trên nội dung của các VM image: Tính toán độ tương đồng của các VM trên các máy chủ vật lý với VM image cần triển khai. Tìm VM trên máy chủ vật lý có độ tương đồng cao nhất, tính toán phần sai khác và chỉ truyền đi phần sai khác tới các VM trên máy chủ vật lý. Từ đó trên máy chủ vật lý có thể tạo ra VM cần triển khai. Do đó giảm được lượng lớn băng thông truyền qua mạng.
  
- Thuật toán migrate VM để giảm cache-miss và trễ truy cập memory.
  - https://www.usenix.org/system/files/conference/hotcloud12/hotcloud12-final16.pdf
  - http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.401.8928&rep=rep1&type=pdf: 
  - Trong mỗi máy chủ vật lý có một bộ giám sát tình trạng cach-miss và hiệu năng của hệ thống. Định kỳ bộ phận giám sát sẽ gửi thông tin về cho cloud scheduler. Tùy vào tình trạng của mỗi máy chủ, cloud scheduler sẽ ra quyết định để di chuyển các VM để giảm tổng cach-miss và thời gian trễ để truy cập memory.
  
- Một phương pháp luận về cân bằng tải cho server
  - https://www.cse.iitb.ac.in/~sahoo/papers/cloud2011_mayank.pdf
  - http://www.ijcaonline.org/research/volume136/number9/chakankar-2016-ijca-908552.pdf
  - Các yêu cầu về tài nguyên (CPU, memory, network) được biểu diễn dưới dạng vector RRV
  - Tài nguyên tiêu thụ của mãy chủ vật lý được biểu diễ dưới dạng vector RUV
  - Tổng các tài nguyên của PM được biểu diễn dưới dạng vector TCV
  - Phương pháp này tập trung vào cân bằng các tài nguyên trên server nhưng chỉ đưa ra lý thuyết, không có dẫn chứng thực tế.
  
- Thuật toán dựa trên thời gian thực hiện để phân bố VM vào PM
  - Chọn ngẫu nhiên một VM
  - Phân bố nó vào PM nào có thời gian thực hiện ngắn nhất
  - https://core.ac.uk/display/36727972?source=3&algorithmId=14&similarToDoc=24348762&similarToDocKey=CORE&recSetID=46c2dd04-edb4-453c-a4f4-7ed00f8bf6e5&position=1&recommendation_type=same_repo&otherRecs=36727972,24943688,25047985,42506237,35096244
 
- Thuật toán tham lam Greedy
  - Tìm node máy chủ vật lý đầu tiên thỏa mãn yêu cầu của VM và sử dụng máy chủ đầu tiên tìm được
  - Sử dụng cạn kiệt tài nguyên của node này trước khi chuyển sang node khác
  - Điểm mạnh: Đơn giản, dễ cài đặt do đó nó đã từng được sử dụng trong một thời gian dài trước đây
  - Điểm yếu: Lãng phí tài nguyên. Trong khi các node vẫn còn thừa tài nguyên sử dụng, chỉ một node được sử dụng để cài đặt các VM đến khi hết tài nguyên
- Thuật toán Round Robin
  - Phân bố các VM trên các máy vật lý một cách lần lượt, đều nhau
  - Điểm mạnh: Sử dụng các máy chủ vật lý một cách đều nhau
  - Điểm yếu: Tiêu thụ năng lượng lớn vì các máy chủ phải bật liên tục.

 

---------------------------------------------------------------------------------------------------------


## First come first servered

- Lưu các yêu cầu vào một hàng đợi
- Xử lý các yêu cầu theo thời gian, lần lượt từ các yêu cầu đến trước được phục vụ trước.

## Thuật toán Min-Min[5]
- Công việc có thời gian tính toán ngắn nhất được thực hiện trước, công việc có thời gian tính toán lâu được thực hiện sau.
- Ưu điểm: Các công việc nhỏ không phải đơi lâu
- Nhược điểm: Các công việc lớn phải đợi lâu mới được thực hiện

## Thuật toám Max-Min[5]
- Công việc có thời gian tính toán lớn nhất được thực hiện trước, công việc có thời gian tính toán nhanh được thực hiện sau
- Ưu điểm: Các công việc lớn không phải đơi lâu
- Nhược điểm: Các công việc nhỏ phải đợi lâu mới được thực hiện

## Thuật toán most-fit[5]
- Thực hiện các công việc có thười gian thù hợp nhất trước
- Không tối ưu

## Giải thuật di truyền[3]

- Là một giải thuật tìm kiếm một solution cho một task dựa trên chiến lược lựa chọn tự nhiên (nature selection strategy)
- Tìm ra một solution có phẩm chất cao từ một miền tìm kiếm rộng lớn trong thời gian đa thức bằng việc áp dụng nguyên tắc của sự tiến hóa
- Một giải thuật di truyền bao gồm solution tốt nhất đã tìm được và các solution trong các vùng tìm kiếm mới
- Một giải thuật di truyền sẽ duy trì một số lượng các cá thể được tiến hóa theo các thế hệ
- Phẩm chất của một cá thể được xác định bởi một hàm đánh giá, hàm này chỉ ra độ tốt của một solution so với các solution khác.
- Các bước của một giải thuật di truyền
  - Bắt đầu với một tập các solution khởi tạo ngẫu nhiên
  - Tạo ra một solution dựa trên các genetic operators
  - Đánh giá các cá thể trong dân số
  - Lặp lại bước 2, 3 cho tới khi hội tụ
  

## Giải thuật bầy đàn [4]



Tài liệu tham khảo:
  1. http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.401.8928&rep=rep1&type=pdf
  2. https://www.researchgate.net/file.PostFileLoader.html?id=588b43dedc332d2885646a64&assetKey=AS%3A455125929074691%401485521885745
  3. http://gridbus.csse.unimelb.edu.au/papers/Workflow_JSP_2005.pdf
  4. http://www.scielo.edu.uy/scielo.php?script=sci_arttext&pid=S0717-50002014000100003
  5. https://www.ijsr.net/archive/v3i5/MDIwMTMxOTc0.pdf
  6. http://www.sersc.org/journals/IJGDC/vol9_no7/10.pdf
  7. http://research.ijcaonline.org/volume120/number6/pxc3903964.pdf
  8. http://www.ijeit.com/vol%202/Issue%2011/IJEIT1412201305_25.pdf
  
  
  
  
  ---------------------------------------------------

 
