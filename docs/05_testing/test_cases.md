# Test Cases – Wavelet Image Similarity

## 1. Mục đích

Tài liệu này liệt kê các trường hợp kiểm thử chính của project **Wavelet Image Similarity**.

Mục tiêu là kiểm tra từng thành phần quan trọng và toàn bộ pipeline xử lý ảnh, đồng thời đảm bảo hệ thống cho kết quả phù hợp đối với ảnh tương đồng, ảnh không tương đồng và dữ liệu đầu vào không hợp lệ.

---

## 2. Danh sách Test Case

| ID   | Thành phần        | Trường hợp kiểm thử           | Input                        | Kết quả mong đợi                                     |
| ---- | ----------------- | ----------------------------- | ---------------------------- | ---------------------------------------------------- |
| TC01 | Preprocessing     | Đọc ảnh hợp lệ                | File ảnh hợp lệ              | Ảnh được đọc thành công                              |
| TC02 | Preprocessing     | Xử lý ảnh hợp lệ              | Ảnh màu                      | Ảnh được preprocessing thành công                    |
| TC03 | Preprocessing     | File không tồn tại            | Đường dẫn sai                | Hệ thống báo lỗi phù hợp                             |
| TC04 | Preprocessing     | File ảnh không hợp lệ         | File không phải ảnh          | Hệ thống xử lý lỗi, không crash                      |
| TC05 | Wavelet Transform | Biến đổi ảnh                  | Ảnh sau preprocessing        | Wavelet Transform thực hiện thành công               |
| TC06 | Wavelet Transform | Ảnh kích thước nhỏ            | Ảnh kích thước nhỏ           | Không xảy ra lỗi ngoài dự kiến                       |
| TC07 | Wavelet Hash      | Tạo Hash                      | Kết quả Wavelet              | Hash được tạo thành công                             |
| TC08 | Wavelet Hash      | Hai ảnh giống nhau            | Ảnh A ↔ Ảnh A                | Hai Hash giống nhau                                  |
| TC09 | Hamming Distance  | Hai Hash giống nhau           | Hash A ↔ Hash A              | Distance = 0                                         |
| TC10 | Hamming Distance  | Hai Hash khác nhau            | Hash A ↔ Hash B              | Distance > 0                                         |
| TC11 | Similarity        | Hai ảnh tương đồng            | `similar/pair_*`             | Distance thấp, kết luận Similar theo threshold       |
| TC12 | Similarity        | Hai ảnh không tương đồng      | `dissimilar/pair_*`          | Distance cao hơn, kết luận Dissimilar theo threshold |
| TC13 | Pipeline          | Chạy toàn bộ pipeline         | Một cặp ảnh tương đồng       | Pipeline chạy thành công và trả kết quả              |
| TC14 | Pipeline          | Chạy với ảnh không tương đồng | Một cặp ảnh không tương đồng | Pipeline chạy thành công và trả kết quả              |
| TC15 | Pipeline          | Nhiều cặp ảnh                 | Dataset test                 | Các cặp ảnh được xử lý đúng                          |
| TC16 | Pipeline          | Input không hợp lệ            | File không tồn tại / lỗi     | Pipeline xử lý lỗi phù hợp                           |

---

## 3. Chi tiết các Test Case quan trọng

### TC01 – Đọc ảnh hợp lệ

**Mục tiêu:** Kiểm tra hệ thống có thể đọc ảnh đầu vào.

**Input:** Một file ảnh hợp lệ trong dataset.

**Thao tác:**

```text
Chọn ảnh
→ Đọc ảnh
→ Kiểm tra dữ liệu ảnh
```

**Kết quả mong đợi:** Ảnh được đọc thành công và dữ liệu ảnh hợp lệ.

**Status:** PASS / FAIL

---

### TC03 – File không tồn tại

**Mục tiêu:** Kiểm tra khả năng xử lý đường dẫn không hợp lệ.

**Input:**

```text
data/input/not_found.jpg
```

**Kết quả mong đợi:** Hệ thống thông báo lỗi phù hợp và không bị crash bất thường.

**Status:** PASS / FAIL

---

### TC05 – Wavelet Transform

**Mục tiêu:** Kiểm tra quá trình biến đổi Wavelet.

**Input:** Ảnh đã được preprocessing.

**Thao tác:**

```text
Ảnh
→ Wavelet Transform
```

**Kết quả mong đợi:** Tạo được kết quả Wavelet hợp lệ để sử dụng cho bước tiếp theo.

**Status:** PASS / FAIL

---

### TC07 – Tạo Wavelet Hash

**Mục tiêu:** Kiểm tra khả năng tạo Hash từ ảnh đã qua Wavelet Transform.

**Input:** Kết quả Wavelet hợp lệ.

**Kết quả mong đợi:** Tạo được Hash với định dạng hợp lệ.

**Status:** PASS / FAIL

---

### TC08 – Hai ảnh giống nhau

**Mục tiêu:** Kiểm tra tính ổn định của Wavelet Hash.

**Input:**

```text
image_A ↔ image_A
```

**Kết quả mong đợi:**

```text
Hash A = Hash A
```

**Status:** PASS / FAIL

---

### TC09 – Hai Hash giống nhau

**Mục tiêu:** Kiểm tra Hamming Distance.

**Input:**

```text
Hash A ↔ Hash A
```

**Kết quả mong đợi:**

```text
Hamming Distance = 0
```

**Status:** PASS / FAIL

---

### TC10 – Hai Hash khác nhau

**Mục tiêu:** Kiểm tra Hamming Distance với hai Hash khác nhau.

**Input:**

```text
Hash A ↔ Hash B
```

**Kết quả mong đợi:**

```text
Hamming Distance > 0
```

**Status:** PASS / FAIL

---

### TC11 – Hai ảnh tương đồng

**Mục tiêu:** Kiểm tra khả năng nhận diện ảnh tương đồng.

**Input:**

```text
data/input/similar/pair_*/
```

**Kết quả mong đợi:**

```text
Ảnh 1
 ↓
Wavelet Hash 1

Ảnh 2
 ↓
Wavelet Hash 2

        ↓

Hamming Distance thấp
        ↓
Similar
```

Kết luận cuối cùng phải tuân theo **threshold đang được sử dụng trong project**.

**Status:** PASS / FAIL

---

### TC12 – Hai ảnh không tương đồng

**Mục tiêu:** Kiểm tra khả năng phân biệt ảnh không tương đồng.

**Input:**

```text
data/input/dissimilar/pair_*/
```

**Kết quả mong đợi:**

```text
Hamming Distance cao hơn
        ↓
Dissimilar
```

Kết luận cuối cùng phải tuân theo **threshold đang được sử dụng trong project**.

**Status:** PASS / FAIL

---

### TC13 – Full Pipeline với ảnh tương đồng

**Mục tiêu:** Kiểm tra toàn bộ pipeline.

**Input:** Một cặp ảnh trong `similar`.

**Quy trình:**

```text
Input Images
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

**Kết quả mong đợi:**

* Tất cả các bước thực hiện thành công.
* Không xảy ra lỗi.
* Kết quả cuối cùng phù hợp với loại dữ liệu đầu vào.

**Status:** PASS / FAIL

---

### TC14 – Full Pipeline với ảnh không tương đồng

**Mục tiêu:** Kiểm tra toàn bộ pipeline với dữ liệu không tương đồng.

**Input:** Một cặp ảnh trong `dissimilar`.

**Kết quả mong đợi:**

* Pipeline chạy hoàn chỉnh.
* Tạo được Hash cho cả hai ảnh.
* Tính được Hamming Distance.
* Kết quả phân loại phù hợp với dữ liệu kiểm thử.

**Status:** PASS / FAIL

---

### TC15 – Kiểm thử nhiều cặp ảnh

**Mục tiêu:** Kiểm tra khả năng xử lý nhiều dữ liệu liên tiếp.

**Input:**

```text
similar/
dissimilar/
```

**Kết quả mong đợi:**

* Các cặp ảnh được xử lý đầy đủ.
* Không xảy ra lỗi bất thường giữa các lần chạy.
* Kết quả của từng cặp được ghi nhận.

**Status:** PASS / FAIL

---

### TC16 – Input không hợp lệ trong Full Pipeline

**Mục tiêu:** Kiểm tra khả năng xử lý lỗi khi pipeline nhận dữ liệu không hợp lệ.

**Input:**

```text
File không tồn tại
hoặc
File ảnh bị lỗi
```

**Kết quả mong đợi:**

* Hệ thống phát hiện lỗi.
* Hiển thị hoặc trả về thông báo lỗi phù hợp.
* Không làm chương trình dừng bất thường.

**Status:** PASS / FAIL

---

## 4. Tiêu chí đánh giá

Test Case được đánh giá **PASS** khi kết quả thực tế phù hợp với kết quả mong đợi.

Test Case được đánh giá **FAIL** khi xảy ra lỗi hoặc kết quả thực tế không phù hợp với kết quả mong đợi.

Đối với việc xác định **Similar / Dissimilar**, sử dụng threshold được định nghĩa trong code hoặc cấu hình thực tế của project, không cố định một giá trị threshold trong tài liệu này.

---

## 5. Ghi nhận kết quả

Sau khi chạy kiểm thử, kết quả của từng Test Case được cập nhật:

```text
PASS
FAIL
```

Các trường hợp FAIL cần ghi rõ nguyên nhân và được tổng hợp trong:

```text
docs/05_testing/test_report.md
```
