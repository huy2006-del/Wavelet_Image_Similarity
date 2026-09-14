# Test Plan – Wavelet Image Similarity

## 1. Mục đích

Tài liệu này mô tả kế hoạch kiểm thử cho project **Wavelet Image Similarity**.

Mục tiêu của quá trình kiểm thử là kiểm tra tính đúng đắn, tính ổn định và khả năng hoạt động của toàn bộ quy trình xử lý ảnh, từ ảnh đầu vào đến kết quả đánh giá độ tương đồng.

Quá trình kiểm thử tập trung vào việc xác định hệ thống có thể xử lý đúng các cặp ảnh tương đồng và không tương đồng hay không, đồng thời kiểm tra khả năng phối hợp giữa các module trong hệ thống.

---

## 2. Phạm vi kiểm thử

Phạm vi kiểm thử bao gồm toàn bộ pipeline xử lý chính của hệ thống:

```text
Ảnh đầu vào
    ↓
Preprocessing
    ↓
Wavelet Transform
    ↓
Wavelet Hash
    ↓
Hamming Distance
    ↓
Kết quả độ tương đồng
```

Các thành phần được kiểm thử gồm:

| STT | Thành phần          | Nội dung kiểm thử                                     |
| --- | ------------------- | ----------------------------------------------------- |
| 1   | Image Preprocessing | Kiểm tra quá trình xử lý ảnh đầu vào                  |
| 2   | Wavelet Transform   | Kiểm tra quá trình biến đổi Wavelet                   |
| 3   | Wavelet Hash        | Kiểm tra quá trình tạo Hash                           |
| 4   | Hamming Distance    | Kiểm tra khoảng cách giữa hai Hash                    |
| 5   | Full Pipeline       | Kiểm tra toàn bộ quy trình từ ảnh đầu vào đến kết quả |
| 6   | Input Validation    | Kiểm tra các trường hợp dữ liệu đầu vào không hợp lệ  |

---

## 3. Mục tiêu kiểm thử

Các mục tiêu chính của quá trình kiểm thử:

1. Kiểm tra hệ thống có thể nhận và xử lý ảnh đầu vào đúng cách.

2. Kiểm tra các bước preprocessing hoạt động đúng theo thiết kế.

3. Kiểm tra Wavelet Transform tạo ra kết quả hợp lệ.

4. Kiểm tra Wavelet Hash có thể tạo ra Hash từ ảnh sau khi xử lý.

5. Kiểm tra Hamming Distance tính đúng khoảng cách giữa hai Hash.

6. Kiểm tra hệ thống có thể phân biệt ảnh tương đồng và ảnh không tương đồng.

7. Kiểm tra các module có thể kết hợp với nhau thành một pipeline hoàn chỉnh.

8. Kiểm tra hệ thống xử lý được các trường hợp đầu vào không hợp lệ mà không gây lỗi nghiêm trọng hoặc làm chương trình dừng bất thường.

9. Kiểm tra kết quả đầu ra có đúng với kết quả mong đợi hay không.

---

## 4. Đối tượng kiểm thử

Đối tượng kiểm thử chính là các module và chương trình trong project có liên quan đến quá trình xử lý và so sánh ảnh.

### 4.1. Module Preprocessing

File:

```text
src/preprocessing/image_preprocessor.py
```

Kiểm tra khả năng xử lý ảnh trước khi đưa vào Wavelet Transform.

Các nội dung cần kiểm tra:

* Ảnh có thể được đọc thành công.
* Ảnh được đưa về kích thước phù hợp.
* Ảnh được chuyển đổi sang dạng cần thiết cho các bước tiếp theo.
* Dữ liệu đầu ra có thể được sử dụng bởi Wavelet Transform.

### 4.2. Module Wavelet Transform

File:

```text
src/wavelet/wavelet_transform.py
```

Kiểm tra quá trình biến đổi ảnh bằng Wavelet.

Các nội dung cần kiểm tra:

* Module nhận được ảnh sau preprocessing.
* Wavelet Transform thực hiện thành công.
* Kết quả biến đổi không bị rỗng hoặc sai định dạng.
* Kết quả có thể được sử dụng cho bước tạo Hash.

### 4.3. Module Wavelet Hash

File:

```text
src/wavelet/wavelet_hash.py
```

Kiểm tra quá trình tạo Hash từ kết quả Wavelet.

Các nội dung cần kiểm tra:

* Hash được tạo thành công.
* Hash có định dạng hợp lệ.
* Hai ảnh giống hoặc gần giống nhau có xu hướng tạo ra Hash tương đồng.
* Hai ảnh khác nhau có thể tạo ra Hash khác nhau.

### 4.4. Module Hamming Distance

File:

```text
src/similarity/hamming_distance.py
```

Kiểm tra khả năng tính khoảng cách giữa hai Hash.

Các nội dung cần kiểm tra:

* Hai Hash giống nhau cho khoảng cách bằng 0.
* Hai Hash khác nhau cho khoảng cách lớn hơn 0.
* Kết quả tính toán đúng với trường hợp kiểm thử.

### 4.5. Full Pipeline

File kiểm thử:

```text
tests/test_pipeline.py
```

Đây là phần kiểm thử chính của TV7.

Kiểm tra toàn bộ quá trình:

```text
Input Image
    ↓
Preprocessing
    ↓
Wavelet Transform
    ↓
Wavelet Hash
    ↓
Hamming Distance
    ↓
Similarity Result
```

Mục tiêu là xác định các module có thể hoạt động liên tục với nhau và tạo ra kết quả cuối cùng hợp lệ.

---

## 5. Chiến lược kiểm thử

Quá trình kiểm thử được thực hiện theo nhiều mức độ khác nhau.

### 5.1. Unit Testing

Kiểm thử từng thành phần riêng biệt.

Ví dụ:

```text
test_preprocessing.py
test_wavelet_transform.py
test_wavelet_hash.py
test_hamming_distance.py
```

Mục tiêu là xác định từng module có hoạt động đúng trước khi kết hợp chúng thành hệ thống hoàn chỉnh.

### 5.2. Integration Testing

Kiểm tra khả năng kết hợp giữa các module.

Ví dụ:

```text
Preprocessing
      ↓
Wavelet Transform
      ↓
Wavelet Hash
      ↓
Hamming Distance
```

Mục tiêu là xác định dữ liệu đầu ra của module trước có thể được sử dụng chính xác bởi module tiếp theo.

### 5.3. System Testing

Kiểm thử toàn bộ hệ thống từ ảnh đầu vào đến kết quả cuối cùng.

File kiểm thử chính:

```text
tests/test_pipeline.py
```

System Testing được sử dụng để kiểm tra hệ thống trong điều kiện gần với quá trình sử dụng thực tế.

---

## 6. Dữ liệu kiểm thử

Dữ liệu kiểm thử được lấy từ cấu trúc dữ liệu của project:

```text
data/
└── input/
    ├── similar/
    │   ├── pair_01/
    │   ├── pair_02/
    │   └── ...
    │
    └── dissimilar/
        ├── pair_01/
        ├── pair_02/
        └── ...
```

### 6.1. Ảnh tương đồng

Các ảnh trong thư mục:

```text
data/input/similar/
```

được sử dụng để kiểm tra trường hợp hai ảnh có nội dung tương đồng.

Kết quả mong đợi là hai ảnh có khoảng cách Hamming tương đối thấp và được hệ thống đánh giá là tương đồng theo ngưỡng được sử dụng trong project.

### 6.2. Ảnh không tương đồng

Các ảnh trong thư mục:

```text
data/input/dissimilar/
```

được sử dụng để kiểm tra trường hợp hai ảnh không tương đồng.

Kết quả mong đợi là hai ảnh có khoảng cách Hamming cao hơn so với nhóm ảnh tương đồng và được hệ thống đánh giá là không tương đồng theo ngưỡng được sử dụng.

---

## 7. Các nhóm trường hợp kiểm thử

Các trường hợp kiểm thử được chia thành các nhóm sau:

### Nhóm 1 – Ảnh tương đồng

Kiểm tra các cặp ảnh được xác định là tương đồng.

Ví dụ:

```text
image_01.jpg
image_02.jpg
```

Kỳ vọng:

```text
Hash 1 ≈ Hash 2
Hamming Distance thấp
→ Similar
```

### Nhóm 2 – Ảnh không tương đồng

Kiểm tra các cặp ảnh được xác định là không tương đồng.

Kỳ vọng:

```text
Hash 1 khác Hash 2
Hamming Distance cao hơn
→ Dissimilar
```

### Nhóm 3 – Hai ảnh giống nhau

Sử dụng cùng một ảnh làm đầu vào cho cả hai phía.

Ví dụ:

```text
image_A ↔ image_A
```

Kỳ vọng:

```text
Hamming Distance = 0
```

### Nhóm 4 – Dữ liệu đầu vào không hợp lệ

Kiểm tra các trường hợp như:

```text
File không tồn tại
Đường dẫn không hợp lệ
File ảnh không thể đọc
Định dạng ảnh không được hỗ trợ
```

Kỳ vọng hệ thống xử lý lỗi phù hợp và không bị dừng bất thường.

### Nhóm 5 – Full Pipeline

Kiểm tra toàn bộ pipeline với dữ liệu thực tế.

Kỳ vọng:

```text
Input
 ↓
Preprocessing
 ↓
Wavelet
 ↓
Hash
 ↓
Hamming Distance
 ↓
Result
```

Tất cả các bước phải thực hiện thành công.

---

## 8. Môi trường kiểm thử

Môi trường kiểm thử dự kiến sử dụng:

| Thành phần        | Môi trường                                        |
| ----------------- | ------------------------------------------------- |
| Ngôn ngữ          | Python                                            |
| Hệ điều hành      | Windows                                           |
| IDE               | Visual Studio Code / môi trường phát triển Python |
| Testing Framework | pytest                                            |
| Dữ liệu           | Dataset ảnh trong thư mục `data/input/`           |
| Source Code       | Project Wavelet_Image_Similarity                  |

Các thư viện cần thiết được cài đặt theo file:

```text
requirements.txt
```

---

## 9. Tiêu chí Pass / Fail

Một test case được xác định là **PASS** khi:

* Chương trình thực hiện đúng thao tác được yêu cầu.
* Không xảy ra lỗi ngoài dự kiến.
* Kết quả thực tế phù hợp với kết quả mong đợi.
* Dữ liệu đầu ra có định dạng hợp lệ.

Một test case được xác định là **FAIL** khi:

* Chương trình bị lỗi hoặc dừng bất thường.
* Không tạo được kết quả.
* Kết quả thực tế khác với kết quả mong đợi.
* Dữ liệu đầu ra không hợp lệ.
* Pipeline không thể hoàn thành toàn bộ quy trình.

---

## 10. Kết quả kiểm thử

Kết quả kiểm thử được ghi nhận trong file:

```text
docs/05_testing/test_report.md
```

Mỗi trường hợp kiểm thử cần ghi nhận tối thiểu:

| Thông tin       | Nội dung               |
| --------------- | ---------------------- |
| Test Case ID    | Mã trường hợp kiểm thử |
| Input           | Dữ liệu đầu vào        |
| Expected Result | Kết quả mong đợi       |
| Actual Result   | Kết quả thực tế        |
| Status          | PASS / FAIL            |
| Note            | Ghi chú nếu có lỗi     |

---

## 11. Tiêu chí hoàn thành kiểm thử

Quá trình kiểm thử được xem là hoàn thành khi:

1. Các test case quan trọng đã được thực hiện.

2. Các module chính đều được kiểm tra.

3. Full Pipeline được kiểm thử thành công.

4. Các lỗi phát hiện trong quá trình kiểm thử được ghi nhận.

5. Kết quả kiểm thử được tổng hợp trong `test_report.md`.

6. Các trường hợp FAIL được kiểm tra và xử lý hoặc ghi nhận rõ nguyên nhân.

---

## 12. Phân công kiểm thử

Phần kiểm thử của project do **Thành viên 7 (TV7)** phụ trách.

Các nhiệm vụ chính:

| STT | Công việc                                     | Người phụ trách            |
| --- | --------------------------------------------- | -------------------------- |
| 1   | Xây dựng Test Plan                            | TV7                        |
| 2   | Xây dựng Test Cases                           | TV7                        |
| 3   | Viết `test_pipeline.py`                       | TV7                        |
| 4   | Chạy kiểm thử toàn bộ pipeline                | TV7                        |
| 5   | Ghi nhận kết quả kiểm thử                     | TV7                        |
| 6   | Tổng hợp Test Report                          | TV7                        |
| 7   | Phối hợp với các thành viên khi phát hiện lỗi | TV7 + thành viên liên quan |

---

## 13. Kết luận

Test Plan được xây dựng nhằm đảm bảo project **Wavelet Image Similarity** được kiểm tra một cách có hệ thống.

Việc kiểm thử tập trung vào từng module riêng biệt và toàn bộ pipeline, từ quá trình tiền xử lý ảnh, Wavelet Transform, tạo Wavelet Hash đến tính Hamming Distance và đưa ra kết quả tương đồng.

Các kết quả kiểm thử sẽ được sử dụng làm cơ sở để đánh giá độ ổn định của hệ thống và phục vụ cho việc hoàn thiện project cũng như báo cáo cuối cùng.
