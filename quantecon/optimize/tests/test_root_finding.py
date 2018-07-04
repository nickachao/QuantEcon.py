import numpy as np
from numpy.testing import assert_almost_equal, assert_allclose
from numba import njit

from quantecon.optimize import newton, newton_secant

@njit
def func(x):
    """
    Function for testing on.
    """
    return (x**3 - 1)


@njit
def func_prime(x):
    """
    Derivative for func.
    """
    return (3*x**2)


@njit
def func_two(x):
    """
    Harder function for testing on.
    """
    return np.sin(4 * (x - 1/4)) + x + x**20 - 1


@njit
def func_two_prime(x):
    """
    Derivative for func_two.
    """
    return 4*np.cos(4*(x - 1/4)) + 20*x**19 + 1


def test_newton_basic():
    """
    Uses the function f defined above to test the scalar maximization 
    routine.
    """
    true_fval = 1.0
    fval = newton(func, 5, func_prime)
    assert_almost_equal(true_fval, fval.root, decimal=4)
    

def test_newton_basic_two():
    """
    Uses the function f defined above to test the scalar maximization 
    routine.
    """
    true_fval = 1.0
    fval = newton(func, 5, func_prime)
    assert_allclose(true_fval, fval.root, rtol=1e-5, atol=0)
    
    
def test_newton_hard():
    """
    Harder test for convergence.
    """
    true_fval = 0.408
    fval = newton(func_two, 0.4, func_two_prime)
    assert_allclose(true_fval, fval.root, rtol=1e-5, atol=0.01)
    

def test_secant_basic():
    """
    Basic test for secant option.
    """
    true_fval = 1.0
    fval = newton_secant(func, 5)
    assert_allclose(true_fval, fval.root, rtol=1e-5, atol=0.001)


def test_secant_hard():
    """
    Harder test for convergence for secant function.
    """
    true_fval = 0.408
    fval = newton_secant(func_two, 0.4)
    assert_allclose(true_fval, fval.root, rtol=1e-5, atol=0.01)


# executing testcases.

if __name__ == '__main__':
    import sys
    import nose

    argv = sys.argv[:]
    argv.append('--verbose')
    argv.append('--nocapture')
    nose.main(argv=argv, defaultTest=__file__)
