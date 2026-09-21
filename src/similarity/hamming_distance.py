"""
Hamming Distance cho Wavelet Hash.

Module của TV4 có nhiệm vụ:
- Kiểm tra hai hash đầu vào.
- Tính Hamming Distance (số bit khác nhau).
- Tính Hamming Distance chuẩn hóa và độ tương đồng.
- Phân loại Similar / Dissimilar theo threshold.

Module không thực hiện preprocessing, Wavelet Transform hay tạo Wavelet Hash.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable, Sequence, Union

import numpy as np

HashInput = Union[str, Sequence[int], np.ndarray]


def _to_bit_string(hash_value: HashInput) -> str:
    """Chuẩn hóa hash về chuỗi bit chỉ gồm '0' và '1'.

    Hỗ trợ:
    - Chuỗi bit, ví dụ ``"101010"``.
    - list/tuple số 0, 1.
    - numpy.ndarray chứa 0, 1 hoặc bool.

    Raises
    ------
    TypeError
        Nếu kiểu dữ liệu không được hỗ trợ.
    ValueError
        Nếu hash rỗng hoặc chứa giá trị khác 0/1.
    """
    if isinstance(hash_value, str):
        bits = hash_value.strip().replace(" ", "")
        if not bits:
            raise ValueError("Hash không được rỗng.")
        if any(bit not in {"0", "1"} for bit in bits):
            raise ValueError("Hash dạng chuỗi chỉ được chứa ký tự 0 và 1.")
        return bits

    if isinstance(hash_value, np.ndarray):
        values = hash_value.reshape(-1).tolist()
    elif isinstance(hash_value, Sequence) and not isinstance(hash_value, (bytes, bytearray)):
        values = list(hash_value)
    else:
        raise TypeError(
            "Hash phải là chuỗi bit, list/tuple bit hoặc numpy.ndarray."
        )

    if len(values) == 0:
        raise ValueError("Hash không được rỗng.")

    bits = []
    for value in values:
        # bool là hợp lệ vì tương ứng 0/1.
        if isinstance(value, (bool, np.bool_)):
            bits.append("1" if bool(value) else "0")
            continue

        # Chấp nhận các kiểu số nguyên của Python/Numpy nếu đúng 0 hoặc 1.
        if isinstance(value, (int, np.integer)) and int(value) in (0, 1):
            bits.append(str(int(value)))
            continue

        raise ValueError("Hash chỉ được chứa các giá trị nhị phân 0 hoặc 1.")

    return "".join(bits)


@dataclass(frozen=True)
class ComparisonResult:
    """Kết quả so sánh hai hash."""

    distance: int
    normalized_distance: float
    similarity: float
    is_similar: bool

    @property
    def label(self) -> str:
        return "Similar" if self.is_similar else "Dissimilar"


class HammingDistance:
    """Tính khoảng cách Hamming và độ tương đồng giữa hai Wavelet Hash.

    Parameters
    ----------
    threshold : float, optional
        Ngưỡng chuẩn hóa trong khoảng [0, 1]. Hai ảnh được xem là Similar khi
        normalized_distance <= threshold. Giá trị mặc định 0.25 chỉ dùng làm
        ngưỡng thử nghiệm ban đầu; ngưỡng cuối cùng nên được TV5 chọn dựa trên
        ROC/validation dataset.
    """

    def __init__(self, threshold: float = 0.25) -> None:
        if not 0.0 <= threshold <= 1.0:
            raise ValueError("threshold phải nằm trong khoảng [0, 1].")
        self.threshold = float(threshold)

    @staticmethod
    def _validate_pair(hash_1: HashInput, hash_2: HashInput) -> tuple[str, str]:
        bits_1 = _to_bit_string(hash_1)
        bits_2 = _to_bit_string(hash_2)

        if len(bits_1) != len(bits_2):
            raise ValueError(
                "Hai hash phải có cùng độ dài để tính Hamming Distance "
                f"(nhận được {len(bits_1)} và {len(bits_2)})."
            )
        return bits_1, bits_2

    def calculate(self, hash_1: HashInput, hash_2: HashInput) -> int:
        """Trả về số vị trí bit khác nhau giữa hai hash."""
        bits_1, bits_2 = self._validate_pair(hash_1, hash_2)
        return sum(bit_1 != bit_2 for bit_1, bit_2 in zip(bits_1, bits_2))

    def normalized(self, hash_1: HashInput, hash_2: HashInput) -> float:
        """Trả về Hamming Distance chuẩn hóa trong khoảng [0, 1]."""
        bits_1, bits_2 = self._validate_pair(hash_1, hash_2)
        distance = sum(bit_1 != bit_2 for bit_1, bit_2 in zip(bits_1, bits_2))
        return distance / len(bits_1)

    def similarity(self, hash_1: HashInput, hash_2: HashInput) -> float:
        """Trả về độ tương đồng trong khoảng [0, 1].

        Công thức: similarity = 1 - normalized_hamming_distance.
        """
        return 1.0 - self.normalized(hash_1, hash_2)

    def compare(
        self,
        hash_1: HashInput,
        hash_2: HashInput,
        threshold: float | None = None,
    ) -> ComparisonResult:
        """Tính đầy đủ distance, similarity và nhãn phân loại.

        Parameters
        ----------
        threshold : float, optional
            Cho phép ghi đè ngưỡng chuẩn hóa của object trong lần so sánh này.
        """
        active_threshold = self.threshold if threshold is None else float(threshold)
        if not 0.0 <= active_threshold <= 1.0:
            raise ValueError("threshold phải nằm trong khoảng [0, 1].")

        bits_1, bits_2 = self._validate_pair(hash_1, hash_2)
        distance = sum(bit_1 != bit_2 for bit_1, bit_2 in zip(bits_1, bits_2))
        normalized_distance = distance / len(bits_1)
        similarity = 1.0 - normalized_distance

        return ComparisonResult(
            distance=distance,
            normalized_distance=normalized_distance,
            similarity=similarity,
            is_similar=normalized_distance <= active_threshold,
        )


def hamming_distance(hash_1: HashInput, hash_2: HashInput) -> int:
    """Hàm tiện ích: tính Hamming Distance thô."""
    return HammingDistance().calculate(hash_1, hash_2)


def normalized_hamming_distance(hash_1: HashInput, hash_2: HashInput) -> float:
    """Hàm tiện ích: tính Hamming Distance chuẩn hóa."""
    return HammingDistance().normalized(hash_1, hash_2)


def similarity_score(hash_1: HashInput, hash_2: HashInput) -> float:
    """Hàm tiện ích: tính độ tương đồng trong khoảng [0, 1]."""
    return HammingDistance().similarity(hash_1, hash_2)
