from pathlib import Path
import sys

import numpy as np
import pytest
# Allow this test file to be run directly from the project root without
# requiring the project to be installed as a package.
PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.wavelet.wavelet_hash import (  # noqa: E402
    DEFAULT_HASH_SIZE,
    WaveletHash,
    generate_wavelet_hash,
)


def test_default_hash_has_fixed_length():
    """The default configuration must produce a 64-bit hash."""
    coefficients = np.arange(64, dtype=np.float32).reshape(8, 8)

    result = WaveletHash().generate(coefficients)

    assert isinstance(result, str)
    assert len(result) == 64
    assert set(result) <= {"0", "1"}


def test_same_coefficients_produce_same_hash():
    """Hash generation must be deterministic."""
    coefficients = np.arange(256, dtype=np.float32).reshape(16, 16)

    hasher = WaveletHash()

    assert hasher.generate(coefficients) == hasher.generate(coefficients)


def test_identical_coefficients_produce_identical_hash():
    """Two identical coefficient matrices must have identical hashes."""
    coefficients = np.random.default_rng(42).normal(size=(32, 32))

    hasher = WaveletHash()

    assert hasher.generate(coefficients) == hasher.generate(coefficients.copy())


def test_hash_size_controls_hash_length():
    """Custom hash dimensions must control the output bit length."""
    coefficients = np.arange(256, dtype=np.float32).reshape(16, 16)

    result = WaveletHash(hash_size=(4, 4)).generate(coefficients)

    assert len(result) == 16


def test_pywavelets_style_dwt2_output_is_supported():
    """The common pywt.dwt2 output form (LL, (LH, HL, HH)) is supported."""
    ll = np.arange(64, dtype=np.float32).reshape(8, 8)
    lh = np.zeros((8, 8), dtype=np.float32)
    hl = np.zeros((8, 8), dtype=np.float32)
    hh = np.zeros((8, 8), dtype=np.float32)

    result = WaveletHash().generate((ll, (lh, hl, hh)))

    assert len(result) == DEFAULT_HASH_SIZE[0] * DEFAULT_HASH_SIZE[1]
    assert set(result) <= {"0", "1"}


def test_mapping_wavelet_output_is_supported():
    """A mapping with LL/LH/HL/HH keys is accepted."""
    coefficients = {
        "LL": np.arange(64, dtype=np.float32).reshape(8, 8),
        "LH": np.zeros((8, 8), dtype=np.float32),
        "HL": np.zeros((8, 8), dtype=np.float32),
        "HH": np.zeros((8, 8), dtype=np.float32),
    }

    result = WaveletHash().generate(coefficients)

    assert len(result) == 64


def test_median_quantization_is_binary_and_expected():
    """Values above the median are 1; values at/below it are 0."""
    coefficients = np.array([[1, 2], [3, 4]], dtype=np.float32)

    result = WaveletHash(hash_size=(2, 2)).generate(coefficients)

    # median = 2.5 -> [0, 0, 1, 1]
    assert result == "0011"


def test_generate_bits_matches_string_api():
    """The debug/visualization API must match the primary string API."""
    coefficients = np.arange(64, dtype=np.float32).reshape(8, 8)

    hasher = WaveletHash()

    bit_matrix = hasher.generate_bits(coefficients)
    bit_string = hasher.generate(coefficients)

    assert bit_matrix.shape == (8, 8)
    assert bit_matrix.dtype == np.uint8
    assert "".join(map(str, bit_matrix.ravel())) == bit_string


def test_functional_api_matches_class_api():
    """The convenience function must use the same algorithm."""
    coefficients = np.arange(64, dtype=np.float32).reshape(8, 8)

    expected = WaveletHash().generate(coefficients)

    assert generate_wavelet_hash(coefficients) == expected


@pytest.mark.parametrize(
    "invalid_hash_size",
    [
        (0, 8),
        (8, 0),
        (-1, 8),
        (8,),
        (8, 8, 8),
        ("8", 8),
    ],
)
def test_invalid_hash_size_is_rejected(invalid_hash_size):
    """Invalid hash dimensions must fail early with a clear exception."""
    with pytest.raises(ValueError):
        WaveletHash(hash_size=invalid_hash_size)


@pytest.mark.parametrize(
    "invalid_coefficients",
    [
        np.array([]),
        np.array([1, 2, 3]),
        np.array([[1, np.nan], [2, 3]], dtype=np.float32),
        {"LH": np.ones((8, 8))},
        object(),
    ],
)
def test_invalid_coefficients_are_rejected(invalid_coefficients):
    """Invalid Wavelet outputs must not silently generate a wrong hash."""
    with pytest.raises(ValueError):
        WaveletHash().generate(invalid_coefficients)
