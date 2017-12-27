# Concept
## Things
  - Là các thực thể có thể thêm vào hệ thống một cách vật lý và có khả năng cung cấp các chức năng
  - Không nhất thiêt phải là các device, mà có thể là một webservice, hoặc bất kỳ nguồn thông tin, chức năng nào có thể quản lý được.
  - Things cung cấp các chức năng qua các Channels.
## Channel
  - Đại diện cho các chức năng khác nhau mà Thing cung cấp.
  - Mỗi Channel là một chức năng khác nhau.
  - Là passive, và có thể được xem là một khai báo của 1 Thing
  - Các Channels được sử dụng thông qua các Items
## Items
  - Là đại diện cho các chức năng được sử dụng bới các ứng dụng (users interface, automation logic)
  - Mỗi Item có một trạng thái, và có thể nhận các lệnh.
## Links
  - Là liên kết giữa Things và Items; thể hiện sự liên kết giữa tầng virtual và tầng physical.
  - Là sự kết hợp, liên kết của ĐÚNG MỘT ThingChannel và một Item.
  - Nếu 1 Thing liên kết với một Item, ta gọi đó là "enabled", tức là chức năng mà Item đó đại diện được xử lý thông qua Channel tương ứng.
  - Khi một Link được thiết lập, một Thing sẽ phản ứng lại các sự kiện gửi tới một Item được liên kết với Channel tương ứng. Ngược lại, nó (Thing) cũng chủ động gửi các sự kiện cho các Items mà Link với các Channels của nó.
  - Một Channel có thể được Link vào nhiều Items; một Item có thể được Link vào nhiều Channels.
## Nhận xét
  - Có thể coi Things là một vật (vd: ô tô, điện thoại, hay một cái hộp trên trung tâm HPCC); Các Items là các cảm biến, bóng đèn, ...; Các Channels là các chức năng của Thing đó; Links là các liên kết giữa Things và các Items.
  - OpenHAB sẽ quản lý các Things, mỗi Thing sẽ có một địa chỉ IP và cần setup và configure trước khi sử dụng.
![alt text](https://docs.openhab.org/concepts/images/thing-devices-1.png)

## Bridges
  - Là một dạng đặc biệt của Things.
  - Là các Things cần thiết phải thêm vào hệ thống để đạt được mục đích là truy cập tới các Things khác. VD: IP gateway cho hệ thống nhà tự động hoặc webservice authentication configure cho các webservice.

## Discovery
  - Là một cơ chế tự động discovery các Things.
  
## Things Status
![alt text](https://github.com/hamhochoi/K59_training/blob/master/Things_status.png?raw=true)
  
## Thing Status API
```
Collection<Thing> things = thingRegistry.getAll();
for (Thing thing : things) {
    ThingStatusInfo statusInfo = thing.getStatusInfo();
    switch (statusInfo.getStatus()) {
        case ONLINE:
            System.out.println("Thing is online");
            break;
        case OFFLINE:
            System.out.println("Thing is offline");
            break;
        default:
            System.out.println("Thing is in state " + statusInfo.getStatus());
            break;
    }
    System.out.println("Thing status detail: " + statusInfo.getStatusDetail());
    System.out.println("Thing status description: " + statusInfo.getDescription());
}
```
## Item
  - Item types: 
![](https://github.com/hamhochoi/K59_training/blob/master/Item%20types.png?raw=true)

## Binding
  - Trước khi kết nối 1 Thing tới OpenHAB, ta phải xác định loại của Thing đó. Việc xác định này được gọi là binding.
  - Có thể hiểu Binding là xác định kiểu điều khiển Items.
  - Danh sách các kiểu Items: https://docs.openhab.org/configuration/items.html#type
## Installation 
  - Nên cài đặt sử dụng Docker
  
## Configure   
  - vào localhost:8080
  - Chọn cài đặt Standard
  - Chọn Paper UI (cho admin)
  - Làm theo hướng dẫn (sử dụng giao diện để định nghĩa một Thing): https://docs.openhab.org/tutorials/beginner/configuration.html
  - Khi sử dụng giao diện Paper UI/discovery để định nghĩa 1 Thing, dữ liệu sẽ được lưu trong một internal database nhưng không được lưu trong file configure.
  - Cũng có thể định nghĩa một Thing sử dụng file text congigure. Khi thực hiện định nghĩa sử dụng file text, các cấu hình sẽ được lưu vào file configure, có thể được backup, restore.
  - Định nghĩa một Thing theo file text: https://docs.openhab.org/configuration/things.html
  

## Reference
  - https://docs.openhab.org/concepts/things.html#thing-status
