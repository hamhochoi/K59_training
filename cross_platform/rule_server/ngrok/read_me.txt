https://viblo.asia/p/tooling-gioi-thieu-ngrok-mang-demo-du-an-web-len-internet-khong-can-deploy-naQZR7eqlvx

1. Trước tiên. Các bạn tải và cài đặt ngrok tại địa chỉ https://ngrok.com/download
   unzip /path/to/ngrok.zip
   ./ngrok authtoken <YOUR_AUTH_TOKEN>      (token lay tu tai khoan ngrok - dang ky bang gmai, vao phan Auth, lay auth_token)
  
2. mkdir ngrok && cd ngrok
   echo "<h1> Hello Ngrok </h1>" > index.html

3. install php : sudo apt install php7.0-cli
   php -S localhost:1111

4. Vao thu muc chua file unzip ngrok
   ./ngrok http 1111
