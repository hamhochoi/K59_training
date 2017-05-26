#Scheduling in cloud computing

1. For the set of VMs find the appropriate Physical
Machine.
2. Determine the proper provisioning scheme for the
VMs.
3. Scheduling the tasks on the VMs.

## Thuật toán tham lam Greedy

- Tìm node máy chủ vật lý đầu tiên thỏa mãn yêu cầu của VM và sử dụng máy chủ đầu tiên tìm được
- Sử dụng cạn kiệt tài nguyên của node này trước khi chuyển sang node khác
- Điểm mạnh: Đơn giản, dễ cài đặt do đó nó đã từng được sử dụng trong một thời gian dài trước đây
- Điểm yếu: Lãng phí tài nguyên. Trong khi các node vẫn còn thừa tài nguyên sử dụng, chỉ một node được sử dụng để cài đặt các VM đến khi hết tài nguyên


## Thuật toán Round Robin
- Phân bố các VM trên các máy vật lý một cách lần lượt, đều nhau
- Điểm mạnh: Sử dụng các máy chủ vật lý một cách đều nhau
- Điểm yếu: Tiêu thụ năng lượng lớn vì các máy chủ phải bật liên tục.

## Giải thuật di truyền

- Dựa trên chiến lược lựa chọn tự nhiên (nature selection strategy)
- Bắt đầu với một tập các 


Tài liệu tham khảo:
  1. http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.401.8928&rep=rep1&type=pdf
