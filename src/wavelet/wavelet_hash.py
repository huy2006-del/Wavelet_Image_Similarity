This module converts Wavelet coefficients produced by the Wavelet Transform
stage into a fixed-length binary hash.

Expected pipeline:

    preprocessed image
        -> WaveletTransform
        -> WaveletHash.generate(...)
        -> HammingDistance.calculate(...)

The class deliberately does not load images and does not calculate Hamming
Distance. Those responsibilities belong to the preprocessing and similarity
modules respectively.
"""

from __future__ import annotations

from typing import Any, Mapping, Sequence, Tuple

import cv2
import numpy as np


DEFAULT_HASH_SIZE: Tuple[int, int] = (8, 8)


class WaveletHash:
    """Generate a deterministic binary hash from Wavelet coefficients.

    The default algorithm uses the low-frequency approximation (LL) component
    because it contains the coarse structure of the image and is generally
    less sensitive to small high-frequency changes.

    Steps:
        1. Extract the LL/approximation coefficients.
        2. Resize them to ``hash_size``.
        3. Quantize each coefficient against the median.
        4. Flatten the binary matrix to a bit string.

    Parameters
    ----------
    hash_size:
        ``(width, height)`` of the binary hash matrix. The default is 8x8,
        producing a 64-bit hash.

    Raises
    ------
    ValueError
        If ``hash_size`` is invalid or the supplied coefficients are empty,
        non-numeric, or cannot be converted to a 2-D approximation array.
    """

    def __init__(self, hash_size: Tuple[int, int] = DEFAULT_HASH_SIZE) -> None:
        self.hash_size = self._validate_hash_size(hash_size)

    @staticmethod
    def _validate_hash_size(
        hash_size: Tuple[int, int],
    ) -> Tuple[int, int]:
        """Validate and normalize the requested hash dimensions."""
        if not isinstance(hash_size, (tuple, list)) or len(hash_size) != 2:
            raise ValueError("hash_size phải có dạng (width, height).")

        width, height = hash_size

        if (
            isinstance(width, bool)
            or isinstance(height, bool)
            or not isinstance(width, (int, np.integer))
            or not isinstance(height, (int, np.integer))
            or width <= 0
            or height <= 0
        ):
            raise ValueError(
                "width và height của hash_size phải là số nguyên dương."
            )

        return int(width), int(height)

    @staticmethod
    def _is_numeric_array(value: Any) -> bool:
        """Return True when ``value`` can represent numeric array data."""
        try:
            array = np.asarray(value)
        except (TypeError, ValueError):
            return False

        return np.issubdtype(array.dtype, np.number)

    @classmethod
    def _extract_approximation(cls, coefficients: Any) -> np.ndarray:
        """Extract a 2-D LL/approximation coefficient matrix.

        The method accepts common representations that a Wavelet Transform
        implementation may return:

        * a plain 2-D NumPy array (already the LL component);
        * a tuple/list ``(LL, details)`` returned by ``pywt.dwt2``;
        * a mapping containing ``"LL"`` or ``"ll"``;
        * a mapping containing ``"approximation"`` or ``"approx"``;
        * a mapping with the standard four subbands ``LL/LH/HL/HH``.

        This keeps TV3 loosely coupled to TV2's concrete return type while
        preserving a clear preference for the LL component.
        """
        value = coefficients

        if isinstance(value, Mapping):
            for key in ("LL", "ll", "approximation", "approx"):
                if key in value:
                    value = value[key]
                    break
            else:
                # Some implementations expose all four subbands as a mapping.
                required = ("LL", "LH", "HL", "HH")
                if all(key in value for key in required):
                    value = value["LL"]
                else:
                    raise ValueError(
                        "Không tìm thấy hệ số LL/approximation trong Wavelet coefficients."
                    )

        elif isinstance(value, (tuple, list)):
            # pywt.dwt2 convention: (cA, (cH, cV, cD)).
            if len(value) == 2 and cls._is_numeric_array(value[0]):
                value = value[0]
            elif len(value) == 4 and cls._is_numeric_array(value[0]):
                # Also support an explicit (LL, LH, HL, HH) representation.
                value = value[0]
            else:
                raise ValueError(
                    "Không nhận diện được cấu trúc Wavelet coefficients."
                )

        try:
            array = np.asarray(value, dtype=np.float32)
        except (TypeError, ValueError) as exc:
            raise ValueError(
                "Wavelet coefficients phải là dữ liệu số."
            ) from exc

        if array.ndim != 2:
            raise ValueError(
                "Hệ số LL/approximation phải là ma trận 2 chiều."
            )

        if array.size == 0:
            raise ValueError("Wavelet coefficients không được rỗng.")

        if not np.all(np.isfinite(array)):
            raise ValueError(
                "Wavelet coefficients chứa NaN hoặc vô cực."
            )

        return array

    def _resize_coefficients(self, approximation: np.ndarray) -> np.ndarray:
        """Resize LL coefficients to the configured hash dimensions."""
        width, height = self.hash_size
        resized = cv2.resize(
            approximation,
            (width, height),
            interpolation=cv2.INTER_AREA,
        )

        return np.asarray(resized, dtype=np.float32)

    @staticmethod
    def _quantize(coefficients: np.ndarray) -> np.ndarray:
        """Convert coefficients to bits using their median as threshold.

        A coefficient strictly greater than the median becomes 1; all other
        coefficients become 0. Using ``>`` instead of ``>=`` makes the rule
        deterministic when coefficients are equal to the median.
        """
        median = float(np.median(coefficients))
        return (coefficients > median).astype(np.uint8)

    def generate(self, coefficients: Any) -> str:
        """Generate a fixed-length binary Wavelet Hash.

        Parameters
        ----------
        coefficients:
            Wavelet Transform output, preferably containing the LL
            approximation coefficients.

        Returns
        -------
        str
            Binary string containing exactly
            ``hash_size[0] * hash_size[1]`` bits.

        Examples
        --------
        >>> transform_output = (np.ones((16, 16)), (None, None, None))
        >>> len(WaveletHash().generate(transform_output))
        64
        """
        approximation = self._extract_approximation(coefficients)
        resized = self._resize_coefficients(approximation)
        bits = self._quantize(resized)

        return "".join("1" if bit else "0" for bit in bits.ravel())

    def generate_bits(self, coefficients: Any) -> np.ndarray:
        """Generate the binary hash as a 2-D NumPy array.

        This helper is useful for debugging and visualization. The primary
        pipeline API remains :meth:`generate`, which returns a bit string
        suitable for Hamming Distance.
        """
        approximation = self._extract_approximation(coefficients)
        resized = self._resize_coefficients(approximation)
        return self._quantize(resized)


# Functional API for simple integrations.
def generate_wavelet_hash(
    coefficients: Any,
    hash_size: Tuple[int, int] = DEFAULT_HASH_SIZE,
) -> str:
    """Generate a Wavelet Hash without explicitly creating ``WaveletHash``."""
    return WaveletHash(hash_size=hash_size).generate(coefficients)


__all__ = [
    "DEFAULT_HASH_SIZE",
    "WaveletHash",
    "generate_wavelet_hash",
]
