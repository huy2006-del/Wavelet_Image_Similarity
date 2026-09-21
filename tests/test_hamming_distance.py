"""Unit test cho module src/similarity/hamming_distance.py.

Chạy từ thư mục gốc project:

    pytest tests/test_hamming_distance.py -v

Mục tiêu:
- Kiểm tra Hamming Distance cơ bản.
- Kiểm tra normalized distance và similarity.
- Kiểm tra ngưỡng Similar / Dissimilar.
- Kiểm tra nhiều kiểu dữ liệu đầu vào.
- Kiểm tra các trường hợp dữ liệu không hợp lệ.
"""

import sys
from pathlib import Path

import numpy as np
import pytest

# Cho phép chạy test trực tiếp từ thư mục project.
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.similarity.hamming_distance import (  # noqa: E402
    HammingDistance,
    hamming_distance,
    normalized_hamming_distance,
    similarity_score,
)


class TestHammingDistanceCalculate:
    """Test hàm tính Hamming Distance thô."""

    def test_identical_hashes_have_zero_distance(self):
        hamming = HammingDistance()

        result = hamming.calculate("10110110", "10110110")

        assert result == 0

    def test_known_hashes_return_correct_distance(self):
        hamming = HammingDistance()

        # Hai chuỗi khác nhau tại 2 vị trí.
        result = hamming.calculate("10110110", "10100111")

        assert result == 2

    def test_completely_different_hashes(self):
        hamming = HammingDistance()

        result = hamming.calculate("00000000", "11111111")

        assert result == 8

    def test_accepts_list_input(self):
        hamming = HammingDistance()

        hash_1 = [1, 0, 1, 1]
        hash_2 = [1, 1, 1, 0]

        assert hamming.calculate(hash_1, hash_2) == 2

    def test_accepts_numpy_array_input(self):
        hamming = HammingDistance()

        hash_1 = np.array([1, 0, 1, 0], dtype=np.uint8)
        hash_2 = np.array([1, 1, 1, 0], dtype=np.uint8)

        assert hamming.calculate(hash_1, hash_2) == 1

    def test_accepts_boolean_numpy_array(self):
        hamming = HammingDistance()

        hash_1 = np.array([True, False, True, False])
        hash_2 = np.array([True, True, True, False])

        assert hamming.calculate(hash_1, hash_2) == 1


class TestNormalizedDistanceAndSimilarity:
    """Test khoảng cách chuẩn hóa và độ tương đồng."""

    def test_normalized_distance(self):
        hamming = HammingDistance()

        # 2 bit khác nhau trên tổng 8 bit => 2/8 = 0.25
        result = hamming.normalized("10110110", "10100111")

        assert result == pytest.approx(0.25)

    def test_similarity_score(self):
        hamming = HammingDistance()

        # similarity = 1 - 0.25 = 0.75
        result = hamming.similarity("10110110", "10100111")

        assert result == pytest.approx(0.75)

    def test_identical_hashes_have_full_similarity(self):
        hamming = HammingDistance()

        assert hamming.normalized("11110000", "11110000") == pytest.approx(0.0)
        assert hamming.similarity("11110000", "11110000") == pytest.approx(1.0)

    def test_opposite_hashes_have_zero_similarity(self):
        hamming = HammingDistance()

        assert hamming.normalized("0000", "1111") == pytest.approx(1.0)
        assert hamming.similarity("0000", "1111") == pytest.approx(0.0)


class TestCompareAndThreshold:
    """Test kết quả phân loại Similar / Dissimilar."""

    def test_similar_when_distance_below_threshold(self):
        hamming = HammingDistance(threshold=0.30)

        result = hamming.compare("10110110", "10100111")

        assert result.distance == 2
        assert result.normalized_distance == pytest.approx(0.25)
        assert result.similarity == pytest.approx(0.75)
        assert result.is_similar is True
        assert result.label == "Similar"

    def test_dissimilar_when_distance_above_threshold(self):
        hamming = HammingDistance(threshold=0.20)

        result = hamming.compare("10110110", "10100111")

        assert result.is_similar is False
        assert result.label == "Dissimilar"

    def test_equal_to_threshold_is_still_similar(self):
        hamming = HammingDistance(threshold=0.25)

        # normalized distance đúng bằng 0.25.
        result = hamming.compare("10110110", "10100111")

        assert result.is_similar is True

    def test_compare_can_override_object_threshold(self):
        hamming = HammingDistance(threshold=0.10)

        result = hamming.compare(
            "10110110",
            "10100111",
            threshold=0.30,
        )

        assert result.is_similar is True


class TestUtilityFunctions:
    """Test ba hàm tiện ích ở cuối module."""

    def test_hamming_distance_function(self):
        assert hamming_distance("1010", "1001") == 2

    def test_normalized_hamming_distance_function(self):
        result = normalized_hamming_distance("1010", "1001")

        assert result == pytest.approx(0.5)

    def test_similarity_score_function(self):
        result = similarity_score("1010", "1001")

        assert result == pytest.approx(0.5)


class TestInvalidInput:
    """Test các trường hợp đầu vào sai."""

    def test_different_hash_lengths_raise_error(self):
        hamming = HammingDistance()

        with pytest.raises(ValueError, match="cùng độ dài"):
            hamming.calculate("1010", "101")

    def test_empty_hash_raises_error(self):
        hamming = HammingDistance()

        with pytest.raises(ValueError, match="không được rỗng"):
            hamming.calculate("", "")

    def test_non_binary_string_raises_error(self):
        hamming = HammingDistance()

        with pytest.raises(ValueError, match="0 và 1"):
            hamming.calculate("1021", "1011")

    def test_non_binary_list_raises_error(self):
        hamming = HammingDistance()

        with pytest.raises(ValueError, match="nhị phân"):
            hamming.calculate([1, 0, 2, 1], [1, 0, 1, 1])

    def test_unsupported_type_raises_error(self):
        hamming = HammingDistance()

        with pytest.raises(TypeError):
            hamming.calculate(1010, 1011)

    @pytest.mark.parametrize("threshold", [-0.01, 1.01])
    def test_invalid_constructor_threshold_raises_error(self, threshold):
        with pytest.raises(ValueError, match="threshold"):
            HammingDistance(threshold=threshold)

    def test_invalid_compare_threshold_raises_error(self):
        hamming = HammingDistance()

        with pytest.raises(ValueError, match="threshold"):
            hamming.compare("1010", "1010", threshold=1.5)
