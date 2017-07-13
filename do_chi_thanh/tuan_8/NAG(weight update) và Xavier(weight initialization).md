# Xaview initialization
- Là phương pháp khởi tạo trọng số cho các liên kết trong mạng neural 
- Giả sử X là tập input có n thành phần
- Tại 1 neural, W là tập các trọng số ngẫu nhiên ứng với các input
- Đầu ra của neural được tính bởi Y = W1*X1 + W2*X2 + ... + Wn*Xn
- Var(X): phương sai của biến ngẫu nhiên X
- Để có Var(Y) = Var(Xi) thì nVar(Wi) = 1 (Xem chứng minh [1])
- Nếu tính cả backpropagate thìmnVar(Wi) = 1
  Do đó 




# Tham khảo:
1. cs231n.github.io/neural-networks-2/
2. 
