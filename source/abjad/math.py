"""
Abjad's math library.
"""

import collections
import fractions
import itertools
import math
import numbers
import typing


def all_are_equal(argument) -> bool:
    """
    Is true when ``argument`` is an iterable collection of equal items.

    ..  container:: example

        >>> abjad.math.all_are_equal([99, 99, 99, 99, 99, 99])
        True

        >>> abjad.math.all_are_equal(17)
        False

    ..  container:: example

        Is true when ``argument`` is empty:

        >>> abjad.math.all_are_equal([])
        True

    """
    try:
        first_element = None
        for element in argument:
            if first_element is None:
                first_element = element
            else:
                if not element == first_element:
                    return False
        return True
    except TypeError:
        return False


def all_are_integer_equivalent(argument) -> bool:
    """
    Is true when ``argument`` is an iterable collection with
    integer-equivalent items.

    ..  container:: example

        >>> import fractions
        >>> items = [1, '2', 3.0, fractions.Fraction(4, 1)]
        >>> abjad.math.all_are_integer_equivalent(items)
        True

        >>> abjad.math.all_are_integer_equivalent([1, '2', 3.5, 4])
        False

    """
    try:
        return all(is_integer_equivalent(_) for _ in argument)
    except TypeError:
        return False


def all_are_integer_equivalent_numbers(argument) -> bool:
    """
    Is true when ``argument`` is an iterable collection with
    integer-equivalent items.

    ..  container:: example

        >>> import fractions
        >>> items = [1, 2, 3.0, fractions.Fraction(4, 1)]
        >>> abjad.math.all_are_integer_equivalent_numbers(items)
        True

        >>> abjad.math.all_are_integer_equivalent_numbers([1, 2, 3.5, 4])
        False

    """
    try:
        return all(is_integer_equivalent_number(_) for _ in argument)
    except TypeError:
        return False


def all_are_nonnegative_integer_equivalent_numbers(argument) -> bool:
    """
    Is true when ``argument`` is an iterable collection of nonnegative
    integer-equivalent numbers.

    ..  container:: example

        >>> import fractions
        >>> items = [0, 0.0, fractions.Fraction(0), 2, 2.0, fractions.Fraction(2)]
        >>> abjad.math.all_are_nonnegative_integer_equivalent_numbers(items)
        True

        >>> items = [0, 0.0, fractions.Fraction(0), -2, 2.0, fractions.Fraction(2)]
        >>> abjad.math.all_are_nonnegative_integer_equivalent_numbers(items)
        False

    """
    try:
        return all(is_nonnegative_integer_equivalent_number(_) for _ in argument)
    except TypeError:
        return False


def all_are_nonnegative_integer_powers_of_two(argument) -> bool:
    """
    Is true when ``argument`` is an iterable collection of nonnegative
    integer powers of two.

    ..  container:: example

        >>> items = [0, 1, 1, 1, 2, 4, 32, 32]
        >>> abjad.math.all_are_nonnegative_integer_powers_of_two(items)
        True

        >>> abjad.math.all_are_nonnegative_integer_powers_of_two(17)
        False

    ..  container:: example

        Is true when ``argument`` is empty:

        >>> abjad.math.all_are_nonnegative_integer_powers_of_two([])
        True

    """
    try:
        return all(is_nonnegative_integer_power_of_two(_) for _ in argument)
    except TypeError:
        return False


def all_are_nonnegative_integers(argument) -> bool:
    """
    Is true when ``argument`` is an iterable collection of nonnegative
    integers.

    ..  container:: example

        >>> abjad.math.all_are_nonnegative_integers([0, 1, 2, 99])
        True

        >>> abjad.math.all_are_nonnegative_integers([0, 1, 2, -99])
        False

    """
    try:
        return all(is_nonnegative_integer(_) for _ in argument)
    except TypeError:
        return False


def all_are_pairs_of_types(argument, first_type, second_type) -> bool:
    """
    Is true when ``argument`` is an iterable collection whose members are all
    of length 2, and where the first member of each pair is an instance of
    ``first_type`` and where the second member of each pair is an instance of
    ``second_type``.

    ..  container:: example

        >>> items = [(1., 'a'), (2.1, 'b'), (3.45, 'c')]
        >>> abjad.math.all_are_pairs_of_types(items, float, str)
        True

        >>> abjad.math.all_are_pairs_of_types('foo', float, str)
        False

    ..  container:: example

        Is true when ``argument`` is empty:

        >>> abjad.math.all_are_pairs_of_types([], float, str)
        True

    """
    try:
        return all(
            (
                len(_) == 2
                and isinstance(_[0], first_type)
                and isinstance(_[1], second_type)
            )
            for _ in argument
        )
    except (KeyError, TypeError):
        return False


def all_are_positive_integers(argument) -> bool:
    """
    Is true when ``argument`` is an iterable collection of positive integers.

    ..  container:: example

        >>> abjad.math.all_are_positive_integers([1, 2, 3, 99])
        True

        >>> abjad.math.all_are_positive_integers(17)
        False

    """
    try:
        return all(is_positive_integer(_) for _ in argument)
    except TypeError:
        return False


def are_relatively_prime(argument) -> bool:
    """
    Is true when ``argument`` is an iterable collection of relative primes.

    ..  container:: example

        >>> abjad.math.are_relatively_prime([13, 14, 15])
        True

        >>> abjad.math.are_relatively_prime([13, 14, 15, 16])
        False

        >>> abjad.math.are_relatively_prime('text')
        False

    ..  container:: example

        Returns true when ``argument`` is empty:

        >>> abjad.math.are_relatively_prime([])
        True

    """
    if not isinstance(argument, collections.abc.Iterable):
        return False
    if not all(isinstance(_, numbers.Number) for _ in argument):
        return False
    all_factors: typing.Set[int] = set([])
    for number in argument:
        current_factors = factors(number)
        current_factors_ = set(current_factors)
        if all_factors & current_factors_:
            return False
        all_factors.update(current_factors_)
    return True


def arithmetic_mean(argument) -> int | float | fractions.Fraction:
    """
    Gets arithmetic mean of ``argument``.

    ..  container:: example

        >>> abjad.math.arithmetic_mean([1, 2, 2, 20, 30])
        11

        >>> abjad.math.arithmetic_mean([1, 2, 20])
        Fraction(23, 3)

        >>> abjad.math.arithmetic_mean([2, 2, 20.0])
        8.0

    Raises exception when ``argument`` is not iterable.
    """
    if not isinstance(argument, collections.abc.Sequence):
        raise TypeError(argument)
    total = sum(argument)
    length = len(argument)
    if isinstance(total, float):
        return total / length
    result = fractions.Fraction(sum(argument), len(argument))
    int_result = int(result)
    if int_result == result:
        return int_result
    else:
        return result


def binomial_coefficient(n, k) -> int:
    """
    Gets binomial coefficient of ``n`` choose ``k``.

    ..  container:: example

        >>> for k in range(8):
        ...     print(k, '\t', abjad.math.binomial_coefficient(8, k))
        ...
        0  1
        1  8
        2  28
        3  56
        4  70
        5  56
        6  28
        7  8

    """
    return math.factorial(n) // (math.factorial(n - k) * math.factorial(k))


def cumulative_products(argument):
    """
    Gets cumulative products of ``argument``.

    ..  container:: example

        >>> abjad.math.cumulative_products([1, 2, 3, 4, 5, 6, 7, 8])
        [1, 2, 6, 24, 120, 720, 5040, 40320]

        >>> abjad.math.cumulative_products([1, -2, 3, -4, 5, -6, 7, -8])
        [1, -2, -6, 24, 120, -720, -5040, 40320]

    Raises exception when ``argument`` is not iterable.

    Returns new object of ``argument`` type.
    """
    if not isinstance(argument, collections.abc.Iterable):
        raise TypeError(argument)
    if len(argument) == 0:
        return type(argument)([])
    result = [argument[0]]
    for element in argument[1:]:
        result.append(result[-1] * element)
    return type(argument)(result)


def cumulative_sums(argument, start=0):
    """
    Gets cumulative sums of ``argument``.

    ..  container:: example

        >>> abjad.math.cumulative_sums([1, 2, 3, 4, 5, 6, 7, 8], start=0)
        [0, 1, 3, 6, 10, 15, 21, 28, 36]

        >>> abjad.math.cumulative_sums([1, 2, 3, 4, 5, 6, 7, 8], start=None)
        [1, 3, 6, 10, 15, 21, 28, 36]

    Raises exception when ``argument`` is not iterable.

    Returns new object of ``argument`` type.
    """
    if start is None:
        result = []
    else:
        result = [start]
    for item in argument:
        if result:
            new = result[-1] + item
            result.append(new)
        else:
            result.append(item)
    return type(argument)(result)


def difference_series(argument):
    """
    Gets difference series of ``argument``.

    ..  container:: example

        >>> abjad.math.difference_series([1, 1, 2, 3, 5, 5, 6])
        [0, 1, 1, 2, 0, 1]

        >>> abjad.math.difference_series([9, 6, 8, 5, 7, 4, 6])
        [-3, 2, -3, 2, -3, 2]

    Returns new object of ``argument`` type.
    """
    result = []
    for i, n in enumerate(argument[1:]):
        result.append(n - argument[i])
    return type(argument)(result)


def divide_integer_by_ratio(n, ratio) -> list[fractions.Fraction | float]:
    """
    Divides integer ``n`` by tuple ``ratio``.

    ..  container:: example

        >>> abjad.math.divide_integer_by_ratio(1, (1, 1, 3))
        [Fraction(1, 5), Fraction(1, 5), Fraction(3, 5)]

    ..  container:: example

        >>> abjad.math.divide_integer_by_ratio(1.0, (1, 1, 3))
        [0.2, 0.2, 0.6]

    """
    assert isinstance(n, int | float), repr(n)
    assert isinstance(ratio, tuple), repr(ratio)
    denominator = sum(ratio)
    factors = [fractions.Fraction(_, denominator) for _ in ratio]
    result = [n * _ for _ in factors]
    return result


def divisors(n) -> list[int]:
    """
    Gets positive divisors of ``n`` in increasing order.

    ..  container:: example

        >>> abjad.math.divisors(84)
        [1, 2, 3, 4, 6, 7, 12, 14, 21, 28, 42, 84]

        >>> for x in range(10, 20):
        ...     print(x, abjad.math.divisors(x))
        ...
        10 [1, 2, 5, 10]
        11 [1, 11]
        12 [1, 2, 3, 4, 6, 12]
        13 [1, 13]
        14 [1, 2, 7, 14]
        15 [1, 3, 5, 15]
        16 [1, 2, 4, 8, 16]
        17 [1, 17]
        18 [1, 2, 3, 6, 9, 18]
        19 [1, 19]

    ..  container:: example

        Allows nonpositive ``n``:

        >>> abjad.math.divisors(-27)
        [1, 3, 9, 27]

    Raises not implemented error on ``0``.
    """
    if not isinstance(n, int):
        raise TypeError(f"must be integer: {n!r}.")
    if n == 0:
        raise NotImplementedError("all numbers divide zero evenly.")
    n = abs(n)
    divisors = [1]
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            divisors.append(i)
    codivisors = [n // i for i in reversed(divisors)]
    if divisors[-1] == codivisors[0]:
        divisors.pop()
    divisors.extend(codivisors)
    divisors.sort()
    return divisors


def factors(n) -> list[int]:
    """
    Gets prime factors less than or equal to ``n`` .

    ..  container:: example

        >>> abjad.math.factors(84)
        [2, 2, 3, 7]

        >>> for n in range(10, 20):
        ...   print(n, abjad.math.factors(n))
        ...
        10 [2, 5]
        11 [11]
        12 [2, 2, 3]
        13 [13]
        14 [2, 7]
        15 [3, 5]
        16 [2, 2, 2, 2]
        17 [17]
        18 [2, 3, 3]
        19 [19]

    ``n`` must be a positive integer.

    Returns factors in increasing order.
    """
    if not is_positive_integer(n):
        raise TypeError(f"must be positive integer: {n!r}.")
    factor = 2
    factors = []
    while 1 < n:
        if n % factor == 0:
            factors.append(factor)
            n = n / factor
        else:
            factor = factor + 1
    return factors


def fraction_to_proper_fraction(
    rational,
) -> tuple[int, fractions.Fraction]:
    """
    Changes ``rational`` to proper fraction.

    ..  container:: example

        >>> import fractions
        >>> abjad.math.fraction_to_proper_fraction(fractions.Fraction(116, 8))
        (14, Fraction(1, 2))

    """
    assert isinstance(rational, fractions.Fraction), repr(rational)
    quotient = int(rational)
    residue = rational - quotient
    return quotient, residue


def greatest_common_divisor(*integers) -> int:
    """
    Calculates greatest common divisor of ``integers``.

    ..  container:: example

        >>> abjad.math.greatest_common_divisor(84, -94, -144)
        2

    Allows nonpositive input.

    Raises not implemented error when zero is included in input.
    """
    common_divisors = None
    for positive_integer in integers:
        all_divisors = set(divisors(positive_integer))
        if common_divisors is None:
            common_divisors = all_divisors
        else:
            common_divisors &= all_divisors
            if common_divisors == set([1]):
                return 1
    assert isinstance(common_divisors, set)
    return max(common_divisors)


def greatest_power_of_two_less_equal(n, i=0) -> int:
    r"""
    Gets greatest integer power of two less than or equal to positive ``n``.

    ..  container:: example

        >>> for n in range(10, 20):
        ...     print('\t%s\t%s' % (n, abjad.math.greatest_power_of_two_less_equal(n)))
        ...
        10 8
        11 8
        12 8
        13 8
        14 8
        15 8
        16 16
        17 16
        18 16
        19 16

        Greatest-but-``i`` integer power of ``2`` less than or equal to
        positive ``n``:

        >>> for n in range(10, 20):
        ...     print('\t%s\t%s' % (n, abjad.math.greatest_power_of_two_less_equal(n, i=1)))
        ...
        10 4
        11 4
        12 4
        13 4
        14 4
        15 4
        16 8
        17 8
        18 8
        19 8

    """
    if n <= 0:
        raise ValueError(f"must be positive: {n!r}.")
    return 2 ** (int(math.log(n, 2)) - i)


def integer_equivalent_number_to_integer(number) -> int | float:
    """
    Changes integer-equivalent ``number`` to integer.

    ..  container:: example

        Returns integer-equivalent number as integer:

        >>> abjad.math.integer_equivalent_number_to_integer(17.0)
        17

    ..  container:: example

        Returns noninteger-equivalent number unchanged:

        >>> abjad.math.integer_equivalent_number_to_integer(17.5)
        17.5

    """
    if is_integer_equivalent_number(number):
        return int(number)
    else:
        return number


def integer_to_base_k_tuple(n, k) -> tuple[int, ...]:
    """
    Changes nonnegative integer ``n`` to base-`k` tuple.

    ..  container:: example

        Gets base-10 digits of 1066:

        >>> abjad.math.integer_to_base_k_tuple(1066, 10)
        (1, 0, 6, 6)

    ..  container:: example

        Gets base-2 digits of 1066:

        >>> abjad.math.integer_to_base_k_tuple(1066, 2)
        (1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0)

    ..  container:: example

        Gets base-26 digits of 1066:

        >>> abjad.math.integer_to_base_k_tuple(1066, 26)
        (1, 15, 0)

    """
    assert isinstance(n, int), repr(n)
    assert 0 <= n, repr(n)
    if n == 0:
        return (0,)
    result = []
    current_exponent = math.trunc(math.log(n, k))
    remainder = n
    while 0 <= current_exponent:
        current_power = k**current_exponent
        current_digit = remainder // current_power
        result.append(current_digit)
        remainder -= current_digit * current_power
        current_exponent -= 1
    return tuple(result)


def integer_to_binary_string(n) -> str:
    r"""
    Changes positive integer ``n`` to binary string.

    ..  container:: example

        >>> for n in range(1, 16 + 1):
        ...     string = abjad.math.integer_to_binary_string(n)
        ...     print(f"{n}\t{string}")
        ...
        1  1
        2  10
        3  11
        4  100
        5  101
        6  110
        7  111
        8  1000
        9  1001
        10 1010
        11 1011
        12 1100
        13 1101
        14 1110
        15 1111
        16 10000

    """
    if n == 0:
        return "0"
    result = bin(abs(n)).lstrip("-0b")
    if n < 0:
        result = "-" + result
    return result


def is_assignable_integer(argument) -> bool:
    r"""
    Is true when ``argument`` is equivalent to an integer that can be written
    without recourse to ties.

    ..  container:: example

        >>> for n in range(0, 16 + 1):
        ...     print('%s\t%s' % (n, abjad.math.is_assignable_integer(n)))
        ...
        0  False
        1  True
        2  True
        3  True
        4  True
        5  False
        6  True
        7  True
        8  True
        9  False
        10 False
        11 False
        12 True
        13 False
        14 True
        15 True
        16 True

    """
    if isinstance(argument, int):
        if 0 < argument:
            if "01" not in integer_to_binary_string(argument):
                return True
    return False


def is_integer_equivalent(argument) -> bool:
    """
    Is true when ``argument`` is an integer-equivalent number.

    ..  container:: example

        >>> abjad.math.is_integer_equivalent(12.0)
        True

        >>> abjad.math.is_integer_equivalent('12')
        True

        >>> abjad.math.is_integer_equivalent('foo')
        False

    """
    if isinstance(argument, numbers.Number):
        return is_integer_equivalent_number(argument)
    try:
        int(argument)
        return True
    except (TypeError, ValueError):
        return False


def is_integer_equivalent_n_tuple(argument, n) -> bool:
    """
    Is true when ``argument`` is a tuple of ``n`` integer-equivalent items.

    ..  container:: example

        >>> import fractions
        >>> tuple_ = (2.0, '3', fractions.Fraction(4, 1))
        >>> abjad.math.is_integer_equivalent_n_tuple(tuple_, 3)
        True

        >>> tuple_ = (2.5, '3', fractions.Fraction(4, 1))
        >>> abjad.math.is_integer_equivalent_n_tuple(tuple_, 3)
        False

    """
    return (
        isinstance(argument, tuple)
        and len(argument) == n
        and all(is_integer_equivalent(_) for _ in argument)
    )


def is_integer_equivalent_number(argument) -> bool:
    """
    Is true when ``argument`` is a number and ``argument`` is equivalent to an
    integer.

    ..  container:: example

        >>> abjad.math.is_integer_equivalent_number(12.0)
        True

        >>> abjad.math.is_integer_equivalent_number(abjad.Duration(1, 2))
        False

    """
    if int(argument) == argument:
        return True
    return False


def is_nonnegative_integer(argument) -> bool:
    """
    Is true when ``argument`` equals a nonnegative integer.

    ..  container:: example

        >>> abjad.math.is_nonnegative_integer(99)
        True

        >>> abjad.math.is_nonnegative_integer(0)
        True

        >>> abjad.math.is_nonnegative_integer(-1)
        False

    """
    if argument == int(argument):
        if 0 <= argument:
            return True
    return False


def is_nonnegative_integer_equivalent_number(argument) -> bool:
    """
    Is true when ``argument`` is a nonnegative integer-equivalent number.

    ..  container:: example

        >>> duration = abjad.Duration(4, 2)
        >>> abjad.math.is_nonnegative_integer_equivalent_number(duration)
        True

    """
    return is_integer_equivalent_number(argument) and 0 <= argument


def is_nonnegative_integer_power_of_two(argument) -> bool:
    """
    Is true when ``argument`` is a nonnegative integer power of 2.

    ..  container:: example

        >>> for n in range(10):
        ...     print(n, abjad.math.is_nonnegative_integer_power_of_two(n))
        ...
        0 True
        1 True
        2 True
        3 False
        4 True
        5 False
        6 False
        7 False
        8 True
        9 False

    """
    if isinstance(argument, int):
        return not bool(argument & (argument - 1))
    elif isinstance(argument, fractions.Fraction):
        return is_nonnegative_integer_power_of_two(
            argument.numerator * argument.denominator
        )
    else:
        return False


def is_positive_integer(argument) -> bool:
    """
    Is true when ``argument`` equals a positive integer.

    ..  container:: example

        >>> abjad.math.is_positive_integer(99)
        True

        >>> abjad.math.is_positive_integer(0)
        False

        >>> abjad.math.is_positive_integer(-1)
        False

    """
    if argument == int(argument):
        if 0 < argument:
            return True
    return False


def is_positive_integer_equivalent_number(argument) -> bool:
    """
    Is true when ``argument`` is a positive integer-equivalent number.

    ..  container:: example

        >>> abjad.math.is_positive_integer_equivalent_number(
        ...     abjad.Duration(4, 2)
        ...     )
        True

    """
    try:
        return 0 < argument and is_integer_equivalent_number(argument)
    except TypeError:  # Python 3 comparisons with non-numbers
        return False


def is_positive_integer_power_of_two(argument) -> bool:
    r"""
    Is true when ``argument`` is a positive integer power of 2.

    ..  container:: example

        >>> for n in range(10):
        ...     print(n, abjad.math.is_positive_integer_power_of_two(n))
        ...
        0 False
        1 True
        2 True
        3 False
        4 True
        5 False
        6 False
        7 False
        8 True
        9 False

    """
    return 0 < argument and is_nonnegative_integer_power_of_two(argument)


def least_common_multiple(*integers) -> int:
    """
    Gets least common multiple of positive ``integers``.

    ..  container:: example

        >>> abjad.math.least_common_multiple(2, 4, 5, 10, 20)
        20

        >>> abjad.math.least_common_multiple(4, 4)
        4

        >>> abjad.math.least_common_multiple(4, 5)
        20

        >>> abjad.math.least_common_multiple(4, 6)
        12

        >>> abjad.math.least_common_multiple(4, 7)
        28

        >>> abjad.math.least_common_multiple(4, 8)
        8

        >>> abjad.math.least_common_multiple(4, 9)
        36

        >>> abjad.math.least_common_multiple(4, 10)
        20

        >>> abjad.math.least_common_multiple(4, 11)
        44

    """
    if len(integers) == 1:
        if not isinstance(integers[0], int):
            raise TypeError(f"must be integer: {integers[0]!r}.")
        if not 0 < integers[0]:
            raise ValueError(f"must be positive: {integers[0]!r}.")
        return integers[0]
    current_lcm = _least_common_multiple_helper(*integers[:2])
    for remaining_positive_integer in integers[2:]:
        current_lcm = _least_common_multiple_helper(
            current_lcm, remaining_positive_integer
        )
    return current_lcm


def _least_common_multiple_helper(m, n):
    assert isinstance(m, int), repr(m)
    assert isinstance(n, int), repr(n)
    factors_m = factors(m)
    factors_n = factors(n)
    for x in factors_m:
        try:
            factors_n.remove(x)
        except ValueError:
            pass
    result = 1
    for x in factors_m + factors_n:
        result *= x
    return result


def partition_integer_by_ratio(n, ratio) -> list[int]:
    """
    Partitions positive integer-equivalent ``n`` by ``ratio``.

    Returns result with weight equal to absolute value of ``n``.

    ..  container:: example

        >>> abjad.math.partition_integer_by_ratio(10, (1, 2))
        [3, 7]

    ..  container:: example

        Partitions positive integer-equivalent ``n`` by ``ratio`` with negative
        parts:

        >>> abjad.math.partition_integer_by_ratio(10, (1, -2))
        [3, -7]

    ..  container:: example

        Partitions negative integer-equivalent ``n`` by ``ratio``:

        >>> abjad.math.partition_integer_by_ratio(-10, (1, 2))
        [-3, -7]

    ..  container:: example

        Partitions negative integer-equivalent ``n`` by ``ratio`` with negative
        parts:

        >>> abjad.math.partition_integer_by_ratio(-10, (1, -2))
        [-3, 7]

    ..  container:: example

        More examples:

        >>> abjad.math.partition_integer_by_ratio(10, (1,))
        [10]

        >>> abjad.math.partition_integer_by_ratio(10, (1, 1))
        [5, 5]

        >>> abjad.math.partition_integer_by_ratio(10, (1, -1, -1))
        [3, -4, -3]

        >>> abjad.math.partition_integer_by_ratio(-10, (1, 1, 1, 1))
        [-3, -2, -3, -2]

        >>> abjad.math.partition_integer_by_ratio(-10, (1, 1, 1, 1, 1))
        [-2, -2, -2, -2, -2]

    """
    if not is_integer_equivalent_number(n):
        raise TypeError(f"is not integer-equivalent number: {n!r}.")
    if not all(is_integer_equivalent_number(_) for _ in ratio):
        raise ValueError(f"must be integer tuple ratio, not {ratio!r}.")
    result = [0]
    parts = [float(abs(n)) * abs(_) / weight(ratio) for _ in ratio]
    cumulative_parts = cumulative_sums(parts, start=None)
    for part in cumulative_parts:
        rounded_part = int(round(part)) - sum(result)
        if part - round(part) == 0.5:
            rounded_part += 1
        result.append(rounded_part)
    result = result[1:]
    if sign(n) == -1:
        result = [-_ for _ in result]
    ratio_signs = [sign(_) for _ in ratio]
    result = [pair[0] * pair[1] for pair in zip(ratio_signs, result)]
    return result


def partition_integer_into_canonic_parts(
    n, decrease_parts_monotonically=True
) -> tuple[int, ...]:
    """
    Partitions integer ``n`` into canonic parts.

    Returns all parts positive on positive ``n``:

    ..  container:: example

        >>> for n in range(1, 11):
        ...     print(n, abjad.math.partition_integer_into_canonic_parts(n))
        ...
        1 (1,)
        2 (2,)
        3 (3,)
        4 (4,)
        5 (4, 1)
        6 (6,)
        7 (7,)
        8 (8,)
        9 (8, 1)
        10 (8, 2)

    ..  container:: example

        Returns all parts negative on negative ``n``:

        >>> for n in reversed(range(-20, -10)):
        ...     print(n, abjad.math.partition_integer_into_canonic_parts(n))
        ...
        -11 (-8, -3)
        -12 (-12,)
        -13 (-12, -1)
        -14 (-14,)
        -15 (-15,)
        -16 (-16,)
        -17 (-16, -1)
        -18 (-16, -2)
        -19 (-16, -3)
        -20 (-16, -4)

    ..  container:: example

        Returns parts that increase monotonically:

        >>> for n in range(11, 21):
        ...     print(n, abjad.math.partition_integer_into_canonic_parts(n,
        ...         decrease_parts_monotonically=False))
        ...
        11 (3, 8)
        12 (12,)
        13 (1, 12)
        14 (14,)
        15 (15,)
        16 (16,)
        17 (1, 16)
        18 (2, 16)
        19 (3, 16)
        20 (4, 16)

    Returns tuple with parts that decrease monotonically.
    """
    assert isinstance(n, int), repr(n)
    assert isinstance(decrease_parts_monotonically, bool)
    if n == 0:
        return (0,)
    result = []
    previous_empty = True
    binary_n = integer_to_binary_string(abs(n))
    binary_length = len(binary_n)
    for i, character in enumerate(binary_n):
        if character == "1":
            place_value = 2 ** (binary_length - i - 1)
            if previous_empty:
                result.append(place_value)
            else:
                result[-1] += place_value
            previous_empty = False
        else:
            previous_empty = True
    sign_n = sign(n)
    if sign(n) == -1:
        result = [sign_n * _ for _ in result]
    if decrease_parts_monotonically:
        return tuple(result)
    else:
        return tuple(reversed(result))


def sign(n) -> int:
    """
    Gets sign of ``n``.

    ..  container:: example

        Returns -1 on negative ``n``:

        >>> abjad.math.sign(-96.2)
        -1

        Returns 0 when ``n`` is 0:

        >>> abjad.math.sign(0)
        0

        Returns 1 on positive ``n``:

        >>> abjad.math.sign(abjad.Duration(9, 8))
        1

    """
    return (0 < n) - (n < 0)


def weight(argument) -> int:
    """
    Gets weight of ``argument``.

    ..  container:: example

        >>> abjad.math.weight([-1, -2, 3, 4, 5])
        15

    ..  container:: example

        >>> abjad.math.weight([])
        0

    Defined equal to sum of the absolute value of items in ``argument``.
    """
    return sum([abs(_) for _ in argument])


def yield_all_compositions_of_integer(n: int) -> typing.Iterator[tuple[int, ...]]:
    """
    Yields all compositions of positive integer ``n``.

    ..  container:: example

        >>> for tuple_ in abjad.math.yield_all_compositions_of_integer(5):
        ...     tuple_
        ...
        (5,)
        (4, 1)
        (3, 2)
        (3, 1, 1)
        (2, 3)
        (2, 2, 1)
        (2, 1, 2)
        (2, 1, 1, 1)
        (1, 4)
        (1, 3, 1)
        (1, 2, 2)
        (1, 2, 1, 1)
        (1, 1, 3)
        (1, 1, 2, 1)
        (1, 1, 1, 2)
        (1, 1, 1, 1, 1)

    Lists parts in descending lex order.

    Parts sum to ``n``.

    Finds small values of ``n`` easily.

    Takes around 4 seconds for ``n`` equal to 17.
    """
    compositions = []
    integer = 0
    string_length = n
    while integer < 2 ** (n - 1):
        binary_string = integer_to_binary_string(integer)
        binary_string = binary_string.zfill(string_length)
        digits = [int(_) for _ in list(binary_string)]
        partition = []
        generator = itertools.groupby(digits, lambda _: _)
        for value, group in generator:
            partition.append(list(group))
        sublengths = [len(part) for part in partition]
        composition = tuple(sublengths)
        compositions.append(composition)
        integer += 1
    for composition in reversed(sorted(compositions)):
        yield composition


class Infinity:
    """
    Infinity.

    ..  container:: example

        All numbers compare less than infinity:

        >>> 9999999 < abjad.Infinity()
        True

        >>> 2**38 < abjad.Infinity()
        True

    ..  container:: example

        Infinity compares equal to itself:

        >>> abjad.Infinity() == abjad.Infinity()
        True

    ..  container:: example

        Negative infinity compares less than infinity:

        >>> abjad.NegativeInfinity() < abjad.Infinity()
        True

    Initializes as a system singleton at start-up.

    Available as a built-in after Abjad starts.
    """

    ### CLASS VARIABLES ###

    __slots__ = ("_value",)

    ### INTIALIZER ###

    def __init__(self):
        self._value = float("infinity")

    ### SPECIAL METHODS ###

    def __eq__(self, argument) -> bool:
        """
        Compares type.
        """
        return isinstance(argument, type(self))

    def __float__(self):
        """
        Convert infinity to float.

        Returns float.
        """
        return self._value

    def __ge__(self, argument):
        """
        Is true for all values of ``argument``.

        Returns true.
        """
        return self._value >= argument

    def __gt__(self, argument):
        """
        Is true for all noninfinite values of ``argument``.

        Returns true or false.
        """
        return self._value > argument

    def __hash__(self):
        """
        Hashes infinity.
        """
        return hash(self.__class__.__name__ + str(self))

    def __le__(self, argument):
        """
        Is true when ``argument`` is infinite.

        Returns true or false.
        """
        return self._value <= argument

    def __lt__(self, argument):
        """
        Is true for no values of ``argument``.

        Returns true or false.
        """
        return self._value < argument

    def __repr__(self) -> str:
        """
        Gets repr.
        """
        return f"{type(self).__name__}()"

    def __sub__(self, argument):
        """
        Subtracts ``argument`` from infinity.

        Returns infinity or 0 if ``argument`` is also infinity.
        """
        if argument is self:
            return 0
        return self


class NegativeInfinity(Infinity):
    """
    Negative infinity.

    ..  container:: example

        All numbers compare greater than negative infinity:

        >>> abjad.NegativeInfinity() < -9999999
        True

    ..  container:: example

        Negative infinity compares equal to itself:

        >>> abjad.NegativeInfinity() == abjad.NegativeInfinity()
        True

    ..  container:: example

        Negative infinity compares less than infinity:

        >>> abjad.NegativeInfinity() < abjad.Infinity()
        True

    Initializes as a system singleton at start-up.

    Available as a built-in after Abjad start.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self):
        self._value = float("-infinity")
