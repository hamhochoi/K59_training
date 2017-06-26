# Predicting resource utilization 

- Sử dụng neural network để dự đoán sử dụng tài nguyên trong tầng cloud: Sử dụng các dữ liệu đã có về lượng tài nguyên đã sử dụng của từng loại task để dự đoán tài nguyên sẽ sử dụng trong tương lai của loại task đó.

    - Với mỗi loại task T với đầu vào là một vector (a, b, c,...) sẽ dự đoán một đầu ra vector R(R1, R2,..., Rn) với Ri là các tài nguyên cần dự đoán.
    - Để đánh giá độ chính xác của kết quả dự đoán vector R so với tài nguyên sử dụng thực sự R', ta sử dụng công thức root-mean-square-deviation:[1] 
        





# Tài liệu tham khảo:
1. http://www.infosys.tuwien.ac.at/staff/mborkowski/pub/UCC2016.pdf
