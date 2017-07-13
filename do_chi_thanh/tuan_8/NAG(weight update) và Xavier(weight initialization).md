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



# Tham khảo:
1. cs231n.github.io/neural-networks-2/
2. http://cs231n.github.io/neural-networks-2/
3. http://proceedings.mlr.press/v9/glorot10a/glorot10a.pdf
4. 
