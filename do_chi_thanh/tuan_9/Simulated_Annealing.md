# Simulated Annealing (SA) là gì?
- SA là thuật toán tìm kiếm lời giải tối ưu dựa trên quá trình vật lý thực tế là luyện kim. 
- Trong vật lý, quá trình luyện kim là đưa kim loại đến nhiệt độ cao để kim loại nóng chảy; sau đó từ từ làm nguội kim loại lỏng để tăng kích thước tinh thể, làm giảm khiếm khuyết của chúng. Nếu quá trình làm lạnh không diễn ra từ từ, kim loại sẽ đạt trạng thái không ổn định (tối ưu địa phương)
# So sánh Simulated Annealing và Hill Climbing
- Hill Climbing chỉ đạt được các cực tiểu địa phương. Để vượt qua vấn đề này, chúng ta có thể dùng một số cách:
  - Thử chạy thuật toán ở nhiều điểm bắt đầu khác nhau.
  - Tăng kích thước không gian tìm kiếm
- Không giống Hill Climbing, SA lựa chọn các 'neighbourhood' một cách random. Nếu việc chuyển từ trạng thái hiện tại sang trạng thái mới đưa ra một kết quả tốt hơn, ta sẽ chấp nhận giải pháp đó; ngược lại, ta sẽ chấp nhận giải pháp tồi hơn **với một xác suất**.
## Tiêu chuẩn chấp nhận một giải pháp 
- Gọi trạng thái hiện tại là s, trạng thái tiếp theo là s'; e = E(s), e' = E(s') lần lượt làm mức năng lượng của từng trạng thái.
T là nhiệt độ của trạng thái s.
- Xác suất để thuật toán SA chọn đi từ trạng thái s tới s' có năng lượng e'>e (tức là đạt trạng thái **tồi hơn** trạng thái hiện tại) là **P = exp( (e-e')/kT)** với k là hằng số Bolzmann. Để ý thấy xác suất P luôn nằm trong [0,1].
- Nếu năng lượng giảm, thuật toán luôn luôn đi tới trạng thái mới; nếu năng lượng tăng, thuật toán đi tới trạng thái mới với xác suất như trên. Đặt r là một số ngẫu nhiên trong [0,1]. Nếu P > r, thuật toán sẽ đi tới trạng thái mới có mức năng lượng cao hơn.
## Thay đổi nhiệt độ T như thế nào? (Cooling Schedule)
- Cooling Schedule bao gồm 4 thành phần:
  - Nhiệt độ khởi tạo
  - Nhiệt độ kết thúc
  - Giảm nhiệt độ như thế nào?
  - Số vòng lặp tại mỗi nhiệt độ.
### Nhiệt độ khởi tạo
- Nhiệt độ ban đầu phải đủ lớn để xác suất P đủ lớn để cho phép chuyển trạng thái sang bất kỳ một trạng thái kế tiếp nào. Nếu điều này không thỏa mãn, trạng thái cuối cùng sẽ như trạng thái ban đầu (hoặc chênh lệch ít), như vậy, chúng ta chỉ đơn thuần thực hiện thuật toán Hill Climbing.
- Nếu nhiệt độ quá lớn, SA có thể chuyển trạng thái đến bất kỳ trạng thái kế tiếp nào khác, như vậy sẽ là tìm kiếm ngẫu nhiên, không thể thực hiện trong không gian bài toán quá lớn.
- Để hiệu quả, chúng ta sẽ tìm kiếm ngẫu nhiên lúc đầu, sau khi nhiệt độ đã đủ nhỏ, chúng ta mới áp dụng thuật toán SA.
- Một số giải pháp để khởi tạo nhiệt độ ban đầu:
  - Nếu chúng ta biết được độ chênh lệch tối đa giữa các mức năng lượng (hàm đánh giá), chúng ta có thể chọn T phù hợp.
  - Cách khác: bắt đầu T lớn, sau đó giảm nhiệt độ nhanh chóng đến khi 60% các trạng thái tồi hơn được chấp nhận; sau đó mới thực hiện giảm từ từ nhiệt độ.
  - Cách khác: Tăng nhanh nhiệt độ tới khi một tỷ lệ nhất định các trạng thái tồi hơn được chấp nhận, lúc đó giảm từ từ nhiệt độ.
  
### Nhiệt độ kết thúc
- Thường là khi T = 0
- Trong thực tế, có thể dừng khi nhiệt độ thấp chấp nhận được, hoặc khi từ trạng thái này không đi tới các trạng thái khác nữa.

### Giảm nhiệt độ
- Công thức: T = T*alpha với alpha là một hàng số nằm trong khoảng (0.8; 0.99)

### Số vòng lặp tại mỗi mức nhiệt độ
- Lựa chọn một số lượng vòng lặp nhất định tại mỗi mức T
- Thực hiện 1 vòng lặp tại mỗi mức T nhưng T giảm rất chậm. T = T/(1+beta*T) với beta nhỏ thích hợp
- Số vòng lặp lớn khi T nhỏ, lặp ít khi T lớn.

# Nâng cao hiệu năng
## Khởi tạo giá trị
- Bình thường, SA sẽ khởi tạo một trạng thái ban đầu là random. Tuy nhiên, ta có thể làm tốt hơn. VD: cho trạng thái ban đầu là kết quả tối ưu khi dùng Greedy search.
## Kết hợp với các giải thuật khác
## Hàm tiêu chuẩn chấp nhận
- Việc tính giá trị của P như trên tại mỗi vòng lặp tại mỗi mức T rất tốn kém, khoảng 1/3 chi phí thời gian, do đó một số cách tăng hiệu năng:
1. P = 1 - delta/T
2. Xây dựng một bảng các giá trị P có thể có tương ứng với delta/T. Sau đó, tại mỗi lần tính, ta chỉ tính delta/T và làm tròn tới số nguyên gần nhất; khi đó ta tra trong bảng mà không phải tính lại giá trị của P.







# Tài liệu tham khảo: 
1. http://www.cs.nott.ac.uk/~pszgxk/aim/notes/simulatedannealing.doc
2. https://vuonghienuit.wordpress.com/2012/05/13/simulated-annealing-thuat-toan-mo-phong-luyen-kim/
