# Rule Engine Docs
- Khi một rule được tạo ra, nó chứa các thông tin về condition và action.
- Các condition đưọc lưu vào 1 DB; các action được lưu vào 1 DB; và 1 DB lưu mapping giữa condition và action.
- Các Event Generator đọc các condition từ Condition DB, kiểm tra các state nhận được từ các Data Source, nếu thỏa mãn sẽ sinh ra một Event tương ứng với condition đó, gửi event tới cho Rule Engine.
- Các Rule Engine đọc dữ liệu từ DB lưu thông tin mapping của condition và action. Khi có event tới, Rule Engine kiểm tra nếu có action tương ứng với event đến, sẽ gọi một action đến các Actor để thực hiện action tương ứng. Ngoài ra, Rule Engine cũng có thể kiểm tra thêm một số các otherCondition.
- Actor khi nhận được một lời gọi thực hiện action từ Rule Engine, sẽ thực hiện action thông qua phương thức execute().
 