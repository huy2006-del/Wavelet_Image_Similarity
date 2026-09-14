```python
"""
Lưu các kết quả trực quan của project.

File này phụ trách:
- Lưu hình ảnh kết quả.
- Tự động tạo thư mục nếu thư mục chưa tồn tại.
- Lưu hình ảnh vào thư mục results/figures/.

Không thực hiện:
- Preprocessing
- Wavelet Transform
- Wavelet Hash
- Hamming Distance
- Evaluation
"""

from pathlib import Path

import cv2
import matplotlib.pyplot as plt


# Thư mục mặc định để lưu hình kết quả
DEFAULT_OUTPUT_DIR = Path("results/figures")


def save_image(image, filename, output_dir=DEFAULT_OUTPUT_DIR):
    """
    Lưu một ảnh vào thư mục kết quả.

    Parameters
    ----------
    image : numpy.ndarray
        Ảnh cần lưu.

    filename : str
        Tên file ảnh, ví dụ: "comparison.png".

    output_dir : Path or str
        Thư mục lưu ảnh.
    """

    # Chuyển đường dẫn thành Path
    output_dir = Path(output_dir)

    # Tạo thư mục nếu chưa tồn tại
    output_dir.mkdir(parents=True, exist_ok=True)

    # Đường dẫn đầy đủ của file
    output_path = output_dir / filename

    # Lưu ảnh
    success = cv2.imwrite(str(output_path), image)

    if not success:
        raise ValueError(f"Không thể lưu ảnh: {output_path}")

    print(f"Đã lưu ảnh: {output_path}")

    return output_path


def save_figure(filename, output_dir=DEFAULT_OUTPUT_DIR, dpi=300):
    """
    Lưu figure hiện tại của Matplotlib.

    Parameters
    ----------
    filename : str
        Tên file, ví dụ: "similarity.png".

    output_dir : Path or str
        Thư mục lưu figure.

    dpi : int
        Độ phân giải của hình ảnh.
    """

    # Chuyển đường dẫn thành Path
    output_dir = Path(output_dir)

    # Tạo thư mục nếu chưa tồn tại
    output_dir.mkdir(parents=True, exist_ok=True)

    # Đường dẫn đầy đủ
    output_path = output_dir / filename

    # Lưu figure hiện tại
    plt.savefig(
        output_path,
        dpi=dpi,
        bbox_inches="tight"
    )

    print(f"Đã lưu figure: {output_path}")

    return output_path
```
