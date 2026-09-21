"""
Thí nghiệm so sánh hai ảnh bằng Wavelet Hash + Hamming Distance.

Ví dụ chạy từ thư mục gốc project:

    python experiments/compare_images.py \
        data/input/similar/pair_01/image_01.jpg \
        data/input/similar/pair_01/image_02.jpg \
        --threshold 0.25

Lưu ý: script này kết nối module của TV1 -> TV2 -> TV3 -> TV4. Vì vậy
`WaveletTransform` và `WaveletHash` phải được các thành viên tương ứng cài đặt.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Any, Dict

# Cho phép chạy trực tiếp: python experiments/compare_images.py ...
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.preprocessing.image_preprocessor import preprocess_image
from src.similarity.hamming_distance import HammingDistance


def _build_wavelet_pipeline():
    """Khởi tạo module Wavelet Transform và Wavelet Hash.

    Hai class này thuộc phần TV2/TV3. Import được đặt trong hàm để lỗi được
    giải thích rõ nếu hai module đó vẫn đang là placeholder.
    """
    try:
        from src.wavelet.wavelet_transform import WaveletTransform
        from src.wavelet.wavelet_hash import WaveletHash
    except (ImportError, AttributeError) as exc:
        raise RuntimeError(
            "Chưa thể chạy compare_images.py vì module của TV2/TV3 chưa hoàn chỉnh. "
            "Cần có class WaveletTransform và WaveletHash."
        ) from exc

    return WaveletTransform(), WaveletHash()


def compare_images(
    image_1_path: str | Path,
    image_2_path: str | Path,
    threshold: float = 0.25,
) -> Dict[str, Any]:
    """So sánh hai ảnh và trả về kết quả đầy đủ.

    Parameters
    ----------
    image_1_path, image_2_path
        Đường dẫn tới hai ảnh cần so sánh.
    threshold
        Ngưỡng Hamming Distance chuẩn hóa trong [0, 1].

    Returns
    -------
    dict
        Chứa hash, Hamming Distance, normalized distance, similarity và nhãn.
    """
    image_1_path = Path(image_1_path)
    image_2_path = Path(image_2_path)

    # TV1: preprocessing
    processed_1 = preprocess_image(image_1_path)
    processed_2 = preprocess_image(image_2_path)

    # TV2 + TV3: Wavelet Transform và Wavelet Hash
    wavelet_transform, wavelet_hash = _build_wavelet_pipeline()
    transformed_1 = wavelet_transform.transform(processed_1)
    transformed_2 = wavelet_transform.transform(processed_2)
    hash_1 = wavelet_hash.generate(transformed_1)
    hash_2 = wavelet_hash.generate(transformed_2)

    # TV4: Hamming Distance + phân loại
    hamming = HammingDistance(threshold=threshold)
    comparison = hamming.compare(hash_1, hash_2)

    return {
        "image_1": str(image_1_path),
        "image_2": str(image_2_path),
        "hash_1": hash_1,
        "hash_2": hash_2,
        "hash_length": len(hash_1),
        "hamming_distance": comparison.distance,
        "normalized_distance": comparison.normalized_distance,
        "similarity": comparison.similarity,
        "similarity_percent": comparison.similarity * 100.0,
        "threshold": threshold,
        "result": comparison.label,
    }


def print_result(result: Dict[str, Any]) -> None:
    """In kết quả thí nghiệm theo định dạng dễ đưa vào báo cáo."""
    print("=" * 64)
    print("IMAGE COMPARISON RESULT")
    print("=" * 64)
    print(f"Image 1             : {result['image_1']}")
    print(f"Image 2             : {result['image_2']}")
    print(f"Hash 1              : {result['hash_1']}")
    print(f"Hash 2              : {result['hash_2']}")
    print(f"Hash length         : {result['hash_length']} bits")
    print(f"Hamming Distance    : {result['hamming_distance']}")
    print(f"Normalized Distance : {result['normalized_distance']:.4f}")
    print(f"Similarity          : {result['similarity_percent']:.2f}%")
    print(f"Threshold           : {result['threshold']:.4f}")
    print(f"Result              : {result['result']}")
    print("=" * 64)


def _build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "So sánh hai ảnh bằng Wavelet Hash và Hamming Distance. "
            "Threshold là Hamming Distance chuẩn hóa trong [0, 1]."
        )
    )
    parser.add_argument("image_1", help="Đường dẫn ảnh thứ nhất.")
    parser.add_argument("image_2", help="Đường dẫn ảnh thứ hai.")
    parser.add_argument(
        "--threshold",
        type=float,
        default=0.25,
        help=(
            "Ngưỡng Hamming Distance chuẩn hóa (mặc định: 0.25). "
            "Ngưỡng cuối cùng nên được chọn bằng ROC trên dataset."
        ),
    )
    return parser


def main() -> None:
    parser = _build_arg_parser()
    args = parser.parse_args()

    try:
        result = compare_images(args.image_1, args.image_2, args.threshold)
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        parser.error(str(exc))

    print_result(result)


if __name__ == "__main__":
    main()
