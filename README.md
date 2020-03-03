# face_recognition_system_

## Work Flow
- Detect face sử dụng thư viện face_recognition 
- Đưa face vừa detect thành 1 vecto đặc trừng 128 chiều (face_recognition cũng hỗ trợ)
- So sánh vecto đó với các vecto có trong dataset
- Xét ngưỡng cho khoảng cách, nếu đạt ngưỡng thì trả về thông tin người đó, không thì unknow (ngưỡng đang chọn là 2 vecto có khoảng cách nhỏ hơn 0.4)
- Gửi thông tin về telegram bot 

## Cách để thông tin gửi về tele
- Cài đặt ứng dụng telegram
- Tìm userinfobot gửi tin nhắn bất kỳ cho nó, nó sẽ trả về Id để thay vào phần user id
- Chưa đủ, khi thay đổi user id vẫn chưa nhận được thông tin ngay, phải tìm @anonymous_face_bot rồi nhắn tin bất kỳ sau đó sẽ nhận được

## Mô tả 
- camera.py   : Mở camera usb
- check.py    : chạy demo
- extract_face: Đưa ảnh trong folder test_faiss về emb_128
- face_utils  : Các hàm xử lý, hiển thị

## Demo
run python check.py 
Nhấn phím s rồi chọn vùng cần làm việc, sau đó nhấn phím space
