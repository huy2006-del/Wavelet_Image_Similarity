# Test Report

## 1. Mục đích

Tài liệu này trình bày kết quả kiểm thử hệ thống **Wavelet Image Similarity**.

Mục tiêu của kiểm thử là xác nhận các module chính hoạt động đúng khi kết hợp thành một pipeline hoàn chỉnh:

```text
Input Image Pair
      ↓
Preprocessing
      ↓
Wavelet Transform
      ↓
Wavelet Hash
      ↓
Hamming Distance
      ↓
Similarity Decision
      ↓
Evaluation
```

Các nội dung kiểm thử bao gồm:

* Kiểm tra preprocessing.
* Kiểm tra Wavelet Transform.
* Kiểm tra Wavelet Hash.
* Kiểm tra Hamming Distance.
* Kiểm tra pipeline xử lý một cặp ảnh.
* Kiểm tra xử lý dataset.
* Kiểm tra dữ liệu đầu vào không hợp lệ.
* Kiểm tra tính nhất quán của kết quả.

---

## 2. Môi trường kiểm thử

| Thành phần           | Giá trị       |
| -------------------- | ------------- |
| Ngôn ngữ             | Python 3.x    |
| Framework kiểm thử   | pytest        |
| Thư viện xử lý ảnh   | OpenCV        |
| Wavelet              | PyWavelets    |
| Numerical processing | NumPy         |
| Dataset              | `data/input/` |
| Test directory       | `tests/`      |

Phiên bản Python và các thư viện cụ thể được xác định theo môi trường thực tế của nhóm khi chạy kiểm thử.

---

## 3. Cấu trúc kiểm thử

Các test được tổ chức trong thư mục:

```text
tests/
├── test_preprocessing.py
├── test_wavelet_transform.py
├── test_wavelet_hash.py
├── test_hamming_distance.py
└── test_pipeline.py
```

Trong đó:

* `test_preprocessing.py`: kiểm tra tiền xử lý ảnh.
* `test_wavelet_transform.py`: kiểm tra Wavelet Transform.
* `test_wavelet_hash.py`: kiểm tra tạo Wavelet Hash.
* `test_hamming_distance.py`: kiểm tra Hamming Distance.
* `test_pipeline.py`: kiểm tra sự kết hợp của các module trong pipeline.

---

## 4. Phương pháp kiểm thử

Project sử dụng hai mức kiểm thử chính.

### 4.1. Unit Test

Unit Test kiểm tra từng module độc lập.

Ví dụ:

```text
Input
  ↓
Function
  ↓
Expected Output
```

Mục tiêu là phát hiện lỗi trong từng thành phần trước khi tích hợp toàn bộ hệ thống.

### 4.2. Integration Test

Integration Test kiểm tra nhiều module khi kết hợp với nhau.

Pipeline được kiểm tra theo hướng:

```text
Image
 ↓
Preprocessing
 ↓
Wavelet Transform
 ↓
Wavelet Hash
 ↓
Hamming Distance
 ↓
Similarity
```

Mục tiêu là xác nhận dữ liệu được truyền đúng giữa các module.

---

## 5. Test Cases

### TC-01: Kiểm tra preprocessing

**Mục tiêu:** xác nhận ảnh đầu vào được đọc và tiền xử lý đúng.

**Input:**

```text
data/input/similar/pair_01/image_01.jpg
```

**Expected:**

* Ảnh được đọc thành công.
* Ảnh đầu ra không rỗng.
* Kích thước ảnh sau preprocessing đúng theo cấu hình.
* Dữ liệu ảnh có kiểu dữ liệu hợp lệ.

**Status:** Chưa cập nhật.

---

### TC-02: Kiểm tra Wavelet Transform

**Mục tiêu:** xác nhận ảnh sau preprocessing có thể được biến đổi bằng Wavelet.

**Expected:**

* Wavelet Transform thực hiện thành công.
* Kết quả không rỗng.
* Các hệ số Wavelet có kích thước hợp lệ.

**Status:** Chưa cập nhật.

---

### TC-03: Kiểm tra Wavelet Hash

**Mục tiêu:** xác nhận hệ thống có thể tạo hash từ ảnh sau Wavelet Transform.

**Expected:**

* Hash được tạo thành công.
* Hash không rỗng.
* Hash có độ dài xác định.
* Hai lần xử lý cùng một ảnh phải tạo ra kết quả nhất quán.

**Status:** Chưa cập nhật.

---

### TC-04: Kiểm tra Hamming Distance

**Mục tiêu:** kiểm tra phép tính khoảng cách giữa hai hash.

**Input:**

```text
Hash A = 10101010
Hash B = 10101010
```

**Expected:**

```text
Hamming Distance = 0
```

Trường hợp hai hash khác nhau cần trả về số lượng bit khác nhau tương ứng.

**Status:** Chưa cập nhật.

---

### TC-05: Kiểm tra pipeline với cặp Similar

**Mục tiêu:** kiểm tra toàn bộ pipeline với một cặp ảnh được gán nhãn `similar`.

**Input:**

```text
data/input/similar/pair_01/
├── image_01.jpg
└── image_02.jpg
```

**Expected:**

* Hai ảnh được đọc thành công.
* Hai ảnh được preprocessing.
* Wavelet Transform thực hiện thành công.
* Hai Wavelet Hash được tạo.
* Hamming Distance được tính.
* Pipeline trả về kết quả hợp lệ.

**Status:** Chưa cập nhật.

---

### TC-06: Kiểm tra pipeline với cặp Dissimilar

**Mục tiêu:** kiểm tra pipeline với một cặp ảnh được gán nhãn `dissimilar`.

**Input:**

```text
data/input/dissimilar/pair_01/
├── image_01.jpg
└── image_02.jpg
```

**Expected:**

* Hai ảnh được xử lý thành công.
* Hash được tạo cho cả hai ảnh.
* Hamming Distance được tính.
* Kết quả similarity được tạo thành công.

**Status:** Chưa cập nhật.

---

### TC-07: Kiểm tra ảnh không tồn tại

**Mục tiêu:** xác nhận hệ thống xử lý lỗi khi đường dẫn ảnh không hợp lệ.

**Input:**

```text
data/input/not_found.jpg
```

**Expected:**

* Hệ thống phát hiện file không tồn tại.
* Không tiếp tục xử lý dữ liệu rỗng.
* Trả về lỗi hoặc thông báo phù hợp.

**Status:** Chưa cập nhật.

---

### TC-08: Kiểm tra hash có cùng độ dài

**Mục tiêu:** đảm bảo Hamming Distance chỉ được tính giữa hai hash hợp lệ.

**Expected:**

Nếu hai hash có độ dài khác nhau, hệ thống phải báo lỗi thay vì trả về kết quả sai.

**Status:** Chưa cập nhật.

---

### TC-09: Kiểm tra tính nhất quán

**Mục tiêu:** đảm bảo cùng một input tạo ra cùng một kết quả.

**Procedure:**

1. Chạy pipeline với cùng một cặp ảnh.
2. Chạy pipeline lần thứ hai.
3. So sánh Wavelet Hash và Hamming Distance.

**Expected:**

```text
Hash lần 1 == Hash lần 2
Distance lần 1 == Distance lần 2
```

**Status:** Chưa cập nhật.

---

## 6. Chạy Test

Từ thư mục gốc của project:

```powershell
pytest
```

Chạy riêng integration test:

```powershell
pytest tests/test_pipeline.py -v
```

Chạy toàn bộ test với thông tin chi tiết:

```powershell
pytest -v
```

---

## 7. Kết quả kiểm thử

Bảng dưới đây được cập nhật sau khi nhóm thực sự chạy test.

| Test File                   | Tổng Test | Passed | Failed | Skipped | Status    |
| --------------------------- | --------: | -----: | -----: | ------: | --------- |
| `test_preprocessing.py`     |         - |      - |      - |       - | Chưa chạy |
| `test_wavelet_transform.py` |         - |      - |      - |       - | Chưa chạy |
| `test_wavelet_hash.py`      |         - |      - |      - |       - | Chưa chạy |
| `test_hamming_distance.py`  |         - |      - |      - |       - | Chưa chạy |
| `test_pipeline.py`          |         - |      - |      - |       - | Chưa chạy |

> Không điền số liệu kiểm thử khi chưa thực sự chạy `pytest`.

---

## 8. Integration Test

Integration Test tập trung kiểm tra luồng xử lý:

```text
Image
 ↓
Preprocessing
 ↓
Wavelet Transform
 ↓
Wavelet Hash
 ↓
Hamming Distance
 ↓
Similarity
```

Các điều kiện cần đảm bảo:

1. Ảnh đầu vào được đọc thành công.
2. Preprocessing trả về dữ liệu hợp lệ.
3. Wavelet Transform nhận đúng dữ liệu đầu vào.
4. Wavelet Hash nhận được kết quả Wavelet hợp lệ.
5. Hai hash có thể được so sánh.
6. Hamming Distance trả về giá trị hợp lệ.
7. Pipeline không bị lỗi trong quá trình truyền dữ liệu giữa các module.

---

## 9. Các lỗi cần theo dõi

Trong quá trình kiểm thử, cần chú ý các lỗi:

### Input Error

* File ảnh không tồn tại.
* Đường dẫn không hợp lệ.
* File không phải ảnh.
* Ảnh bị lỗi.

### Processing Error

* Ảnh có kích thước không phù hợp.
* Wavelet không được hỗ trợ.
* Hệ số Wavelet không hợp lệ.
* Hash rỗng.

### Similarity Error

* Hai hash có độ dài khác nhau.
* Hamming Distance không hợp lệ.
* Threshold không hợp lệ.

### Pipeline Error

* Module không import được.
* Sai kiểu dữ liệu giữa các module.
* Kết quả của module trước không phù hợp với module sau.

---

## 10. Tiêu chí Pass/Fail

Một test được xem là **PASS** khi output thực tế phù hợp với expected output đã định nghĩa.

Một test được xem là **FAIL** khi:

* Function phát sinh exception ngoài dự kiến.
* Output sai định dạng.
* Output khác expected result.
* Dữ liệu truyền giữa các module không hợp lệ.

Một test có thể được đánh dấu **SKIP** khi chức năng phụ thuộc vào module chưa được triển khai hoặc điều kiện môi trường chưa đáp ứng.

---

## 11. Kết luận kiểm thử

Test Report được sử dụng để ghi nhận trạng thái kiểm thử thực tế của project.

Việc hoàn thành test report cần dựa trên kết quả chạy:

```powershell
pytest -v
```

Sau khi chạy test, nhóm cập nhật:

* Số test đã chạy.
* Số test Passed.
* Số test Failed.
* Số test Skipped.
* Các lỗi phát hiện được.
* Nguyên nhân và cách khắc phục.

Không sử dụng số liệu giả trong báo cáo kiểm thử.
