import pytest

from animations.prime_factor import naive_lpf, optimized_lpf, is_prime_naive, is_prime_opt

@pytest.mark.parametrize("n", [1, 2, 3, 4, 15, 21, 37, 97, 180])
def test_lpf_agreement(n):
    assert naive_lpf(n) == optimized_lpf(n)

@pytest.mark.parametrize("n", [0, 1, 2, 3, 4, 5, 18, 37, 97, 100])
def test_is_prime_agreement(n):
    assert is_prime_naive(n) == is_prime_opt(n)

