# Computation offloading trong Fog computation

- Do các thiết bị tầng Fog thường có khả năng tính toán thấp, low-power nên khi thực hiện các công việc đòi hỏi khối lượng tính toán lớn, do đó ta phải chia tải tính toán.
- Có 2 phương pháp để chia tải tính toán trong Fog computing 
    * Gửi các phần tính toán lớn lên cloud
    * Chia sẻ phần tính toán lớn cho các thiết bị Fog khác.

## Gửi thẳng lên Cloud

- Không phải gửi tất cả công việc tính toán lên cloud, chỉ gửi các tính toán khó lên cloud, trước khi gửi phải tính toán xem việc tính toán trên cloud hay local là tốt hơn.
- Tại lần chạy đầu tiên, phải tính toán thời gian chạy ở local và cloud
- Từ lần chạy thứ 2, sử dụng kết quả tính toán được ở lần chạy trước để so sánh, chọn chạy ở local hay cloud; sau mỗi lần chạy phải cập nhật lại thời gian tính toán phía cloud, local.
- Cập nhật thời gian tính toán phía cloud (Ts): Xác định độ lệch về thời gian tính toán phía server sau các lần chạy các tác vụ tính toán. Nếu độ lệch đủ nhỏ (VD 10%) thì giảm dần tần suất cập nhập giá trị Ts. Ngược lại, nếu độ lệch lớn, phải update lại Ts. ớnKhi resume update, các kết quả Ts trước không được sử dụng nữa. 

## Chia sẻ tác vụ tính toán lớn với các thiết bị Fog khác.




## Tài liệu tham khảo:
1. http://wcl.cs.rpi.edu/theses/imaishigeru-master.pdf
2. http://networking.khu.ac.kr/layouts/net/publications/data/KCC2016/%ED%8A%B8%EB%A6%AC.pdf
3. 
