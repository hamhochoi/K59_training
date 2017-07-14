# Xaview initialization
- Là phương pháp khởi tạo trọng số cho các liên kết trong mạng neural 
- Giả sử X là tập input của layer thứ j có kích cỡ là n.
- Tại 1 neural, W là tập các trọng số ngẫu nhiên ứng với các input
- Đầu ra của neural được tính bởi Y = W1*X1 + W2*X2 + ... + Wn*Xn
- Var(X): phương sai của biến ngẫu nhiên X
- Tại mỗi neural, mong muốn duy trì được phương sai của trọng số đầu vào với đầu ra. Tức là **Var(Y) = Var(Xi)**
- Để có Var(Y) = Var(Xi) thì nVar(Wi) = 1 (Xem chứng minh [1])
- Nếu tính cả backpropagate thì mVar(Wi) = 1 với m là kích thước layer thứ j+1.  
  Do đó Var(Wi) = 2/(n+m)
- Ta có thể sử dụng phân phối chuẩn Gaussian với E(X) = 0 và Var(X) = 1.
  Khi W theo phân phối chuẩn gausian, var(x) = 1 
  Để có được Var(Wi) = 1/n --> Wi = X.sqrt(n)
- Như vậy, để khởi tạo trọng số theo phương pháp Xavier, ta khởi tạo các giá trị random rồi nhân các giá trị đó với sqrt(n).
  vd trong numpy: w = np.random.randn(n)/sqrt(n) [2]
- Trong [3], tác giả đề xuất dùng var(Wi) = 2/(n+m) tuy nhiên, trong thực tế ta sử dụng [2].
- Khi sử dụng ReLu neural, [3] đề xuất dùng w = np.random.randn(n)*sqrt(2.0/n)

# Nesterov's Accelerate Gradient Descent (NAG)[4]
- Là một thuật toán cập nhật trọng số W. Để hiểu rõ hơn, ta phải tìm hiểu trước tiên và momentum.
- **Đọc [4] để hiểu rõ hơn và dễ hiểu hơn**
## Momentum:
- Khi nghiệm của Gradient Descent rơi vào local minimum, ta cần đà (momentum) để có thể (không phải luôn luôn) thoát ra khỏi nghiệm local minimum đó. 
- Momentum dựa trên hiện tượng vật lý, giống như thả một viên bi xuống local minimum, nếu có đà đủ mạnh, viên bi đó có thể thoát khỏi vị trí local minimum và có thể tới được global minimum.
- Giải thích một số ký hiệu trong [4]: 
  - v(t): là độ thay đổi giá trị của W (trong [4] là *theta*) tại thời điểm t.
  - Khi không có momentum, v(t) = *learning_rate* * *đạo hàm của hàm cost*
  - Khi có thêm momentum, v(t) = *learning_rate* * *đạo hàm của hàm cost* + *gamma* * *v(t-1)*
  - Ở trên, *gamma* * *v(t-1)* chính là momentum để vượt qua local minimum, *gamma* thường lấy là 0.9
## Thuật toán NAG
- Momentum giúp vượt qua local minimum, tuy nhiên, khi gần đến global minimum, mất nhiều thời gian để hội tụ (dừng lại).
- Thuật toán NAG được dùng để giúp hội tụ nhanh hơn.
- Ý tưởng: dự đoán vị trí tiếp theo (giá trị tiếp theo của J(W) với J() là cost function).
  - Một cách gần đúng, vị trí tiếp theo là *theta* = *theta* - *momentum* * *v(t-1)* (bỏ phần gradient)
  - Công thức cập nhật trọng số: 
     *theta* = *theta* - *gamma* * *v(t-1)* - *learning_rate* * *đạo hàm của J(*theta* - *gamma* * *v(t-1)*)*
     với *theta* - *gamma* * *v(t-1)* là vị trí tiếp theo. 
  - Khi đó, giá trị cập nhật sẽ gần với điểm cực tiểu hơn vì luôn đi ngược hướng với đạo hàm tại điểm tiếp theo nên sẽ tiến về gần đích hơn.

# Tham khảo:
1. cs231n.github.io/neural-networks-2/
2. http://cs231n.github.io/neural-networks-2/
3. http://proceedings.mlr.press/v9/glorot10a/glorot10a.pdf
4. https://machinelearningcoban.com/2017/01/16/gradientdescent2/#-nesterov-accelerated-gradient-nag
