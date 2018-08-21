# Rule Engine Docs
- Khi một rule được tạo ra, nó chứa các thông tin về trigger, condition và action.
- Các trigger được lưu vào 1 DB; các rule (mapping trigger-condition, event-action) đưọc lưu vào 1 DB; các action được lưu vào 1 DB; 
- Các Event Generator đọc các trigger từ Trigger DB, kiểm tra các state nhận được từ các Data Source, nếu thỏa mãn sẽ sinh ra một Event tương ứng với trigger đó, gửi event tới cho Rule Engine.
- Các Rule Engine đọc dữ liệu từ DB lưu thông tin mapping của trigger-condition-action. Khi có event tới, Rule Engine kiểm tra condition tương ứng, nếu thỏa mãn, gọi action tương ứng dựa trên việc mapping.
- Actor khi nhận được một lời gọi thực hiện action từ Rule Engine, sẽ thực hiện action thông qua phương thức execute().

