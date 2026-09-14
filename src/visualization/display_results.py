```python
"""
Hiển thị kết quả so sánh ảnh.

File này phụ trách:
- Hiển thị 2 ảnh cần so sánh.
- Hiển thị thông tin kết quả so sánh.
- Hiển thị Hamming Distance và kết luận Similar / Dissimilar.

Không thực hiện:
- Preprocessing
- Wavelet Transform
- Wavelet Hash
- Tính Hamming Distance
"""

import cv2
import matplotlib.pyplot as plt


def display_images(image1, image2, title1="Ảnh 1", title2="Ảnh 2"):
    """
    Hiển thị hai ảnh cạnh nhau.

    Parameters
    ----------
    image1 : numpy.ndarray
        Ảnh thứ nhất.

    image2 : numpy.ndarray
        Ảnh thứ hai.

    title1 : str
        Tiêu đề của ảnh thứ nhất.

    title2 : str
        Tiêu đề của ảnh thứ hai.
    """

    # Tạo cửa sổ gồm 2 vùng hiển thị ảnh
    plt.figure(figsize=(10, 5))

    # Hiển thị ảnh thứ nhất
    plt.subplot(1, 2, 1)

    if len(image1.shape) == 3:
        image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)

    plt.imshow(image1)
    plt.title(title1)
    plt.axis("off")

    # Hiển thị ảnh thứ hai
    plt.subplot(1, 2, 2)

    if len(image2.shape) == 3:
        image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)

    plt.imshow(image2)
    plt.title(title2)
    plt.axis("off")

    plt.tight_layout()
    plt.show()


def display_comparison(
    image1,
    image2,
    hamming_distance,
    threshold,
    title1="Ảnh 1",
    title2="Ảnh 2"
):
    """
    Hiển thị hai ảnh cùng với kết quả so sánh.

    Parameters
    ----------
    image1 : numpy.ndarray
        Ảnh thứ nhất.

    image2 : numpy.ndarray
        Ảnh thứ hai.

    hamming_distance : int
        Khoảng cách Hamming giữa hai Wavelet Hash.

    threshold : int
        Ngưỡng dùng để phân loại ảnh.

    title1 : str
        Tiêu đề ảnh thứ nhất.

    title2 : str
        Tiêu đề ảnh thứ hai.
    """

    # Xác định kết quả dựa trên threshold
    if hamming_distance <= threshold:
        result = "Similar"
    else:
        result = "Dissimilar"

    # Tạo cửa sổ hiển thị
    plt.figure(figsize=(10, 6))

    # Ảnh thứ nhất
    plt.subplot(1, 2, 1)

    if len(image1.shape) == 3:
        image1 = cv2.cvtColor(image1, cv2.COLOR_BGR2RGB)

    plt.imshow(image1)
    plt.title(title1)
    plt.axis("off")

    # Ảnh thứ hai
    plt.subplot(1, 2, 2)

    if len(image2.shape) == 3:
        image2 = cv2.cvtColor(image2, cv2.COLOR_BGR2RGB)

    plt.imshow(image2)
    plt.title(title2)
    plt.axis("off")

    # Thêm thông tin kết quả ở phía dưới
    plt.figtext(
        0.5,
        0.03,
        f"Hamming Distance: {hamming_distance} | "
        f"Threshold: {threshold} | "
        f"Result: {result}",
        ha="center",
        fontsize=12
    )

    plt.tight_layout(rect=[0, 0.08, 1, 1])
    plt.show()


def display_similarity_result(hamming_distance, threshold):
    """
    Hiển thị riêng kết quả phân loại ảnh.

    Parameters
    ----------
    hamming_distance : int
        Khoảng cách Hamming.

    threshold : int
        Ngưỡng phân loại.
    """

    if hamming_distance <= threshold:
        result = "Similar"
    else:
        result = "Dissimilar"

    print("=== Image Similarity Result ===")
    print(f"Hamming Distance: {hamming_distance}")
    print(f"Threshold: {threshold}")
    print(f"Result: {result}")
```
