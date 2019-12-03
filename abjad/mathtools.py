"""
Abjad's math library.
"""

try:
    import quicktions as fractions  # type: ignore
except ImportError:
    import fractions  # type: ignore
import collections
import itertools
import math
import numbers
import typing

from abjad.system.FormatSpecification import FormatSpecification
from abjad.system.StorageFormatManager import StorageFormatManager

### FUNCTIONS ###


def all_are_equal(argument) -> bool:
    """
    Is true when ``argument`` is an iterable collection of equal items.

    ..  container:: example

        >>> abjad.mathtools.all_are_equal([99, 99, 99, 99, 99, 99])
        True

        >>> abjad.mathtools.all_are_equal(17)
        False

    ..  container:: example

        Is true when ``argument`` is empty:

        >>> abjad.mathtools.all_are_equal([])
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

        >>> items = [1, '2', 3.0, abjad.Fraction(4, 1)]
        >>> abjad.mathtools.all_are_integer_equivalent(items)
        True

        >>> abjad.mathtools.all_are_integer_equivalent([1, '2', 3.5, 4])
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

        >>> items = [1, 2, 3.0, abjad.Fraction(4, 1)]
        >>> abjad.mathtools.all_are_integer_equivalent_numbers(items)
        True

        >>> abjad.mathtools.all_are_integer_equivalent_numbers([1, 2, 3.5, 4])
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

        >>> items = [0, 0.0, abjad.Fraction(0), 2, 2.0, abjad.Fraction(2)]
        >>> abjad.mathtools.all_are_nonnegative_integer_equivalent_numbers(items)
        True

        >>> items = [0, 0.0, abjad.Fraction(0), -2, 2.0, abjad.Fraction(2)]
        >>> abjad.mathtools.all_are_nonnegative_integer_equivalent_numbers(items)
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
        >>> abjad.mathtools.all_are_nonnegative_integer_powers_of_two(items)
        True

        >>> abjad.mathtools.all_are_nonnegative_integer_powers_of_two(17)
        False

    ..  container:: example

        Is true when ``argument`` is empty:

        >>> abjad.mathtools.all_are_nonnegative_integer_powers_of_two([])
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

        >>> abjad.mathtools.all_are_nonnegative_integers([0, 1, 2, 99])
        True

        >>> abjad.mathtools.all_are_nonnegative_integers([0, 1, 2, -99])
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
        >>> abjad.mathtools.all_are_pairs_of_types(items, float, str)
        True

        >>> abjad.mathtools.all_are_pairs_of_types('foo', float, str)
        False

    ..  container:: example

        Is true when ``argument`` is empty:

        >>> abjad.mathtools.all_are_pairs_of_types([], float, str)
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

        >>> abjad.mathtools.all_are_positive_integers([1, 2, 3, 99])
        True

        >>> abjad.mathtools.all_are_positive_integers(17)
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

        >>> abjad.mathtools.are_relatively_prime([13, 14, 15])
        True

        >>> abjad.mathtools.are_relatively_prime([13, 14, 15, 16])
        False

        >>> abjad.mathtools.are_relatively_prime('text')
        False

    ..  container:: example

        Returns true when ``argument`` is empty:

        >>> abjad.mathtools.are_relatively_prime([])
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


def arithmetic_mean(argument) -> typing.Union[int, float]:
    """
    Gets arithmetic mean of ``argument``.

    ..  container:: example

        >>> abjad.mathtools.arithmetic_mean([1, 2, 2, 20, 30])
        11

        >>> abjad.mathtools.arithmetic_mean([1, 2, 20])
        Fraction(23, 3)

        >>> abjad.mathtools.arithmetic_mean([2, 2, 20.0])
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
        ...     print(k, '\t', abjad.mathtools.binomial_coefficient(8, k))
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

        >>> abjad.mathtools.cumulative_products([1, 2, 3, 4, 5, 6, 7, 8])
        [1, 2, 6, 24, 120, 720, 5040, 40320]

        >>> abjad.mathtools.cumulative_products([1, -2, 3, -4, 5, -6, 7, -8])
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

        >>> abjad.mathtools.cumulative_sums([1, 2, 3, 4, 5, 6, 7, 8], start=0)
        [0, 1, 3, 6, 10, 15, 21, 28, 36]

        >>> abjad.mathtools.cumulative_sums([1, 2, 3, 4, 5, 6, 7, 8], start=None)
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


# TODO: move to Sequence
def cumulative_sums_pairwise(argument):
    """
    Gets pairwise cumulative sums of ``argument`` from zero.

    ..  container:: example

        >>> abjad.mathtools.cumulative_sums_pairwise([1, 2, 3, 4, 5, 6])
        [(0, 1), (1, 3), (3, 6), (6, 10), (10, 15), (15, 21)]

    Returns pairs in new object of ``argument`` type.
    """
    import abjad

    sums = cumulative_sums(argument)
    pairs = abjad.sequence(sums).nwise()
    return type(argument)([tuple(_) for _ in pairs])


def difference_series(argument):
    """
    Gets difference series of ``argument``.

    ..  container:: example

        >>> abjad.mathtools.difference_series([1, 1, 2, 3, 5, 5, 6])
        [0, 1, 1, 2, 0, 1]

        >>> abjad.mathtools.difference_series([9, 6, 8, 5, 7, 4, 6])
        [-3, 2, -3, 2, -3, 2]

    Returns new object of ``argument`` type.
    """
    result = []
    for i, n in enumerate(argument[1:]):
        result.append(n - argument[i])
    return type(argument)(result)


def divisors(n) -> typing.List[int]:
    """
    Gets positive divisors of ``n`` in increasing order.

    ..  container:: example

        >>> abjad.mathtools.divisors(84)
        [1, 2, 3, 4, 6, 7, 12, 14, 21, 28, 42, 84]

        >>> for x in range(10, 20):
        ...     print(x, abjad.mathtools.divisors(x))
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

        >>> abjad.mathtools.divisors(-27)
        [1, 3, 9, 27]

    Raises not implemented error on ``0``.
    """
    if not isinstance(n, int):
        message = "must be integer: {!r}."
        message = message.format(n)
        raise TypeError(message)
    if n == 0:
        message = "all numbers divide zero evenly."
        raise NotImplementedError(message)
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


def factors(n) -> typing.List[int]:
    """
    Gets prime factors less than or equal to ``n`` .

    ..  container:: example

        >>> abjad.mathtools.factors(84)
        [2, 2, 3, 7]

        >>> for n in range(10, 20):
        ...   print(n, abjad.mathtools.factors(n))
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
        message = "must be positive integer: {!r}."
        message = message.format(n)
        raise TypeError(message)
    factor = 2
    factors = []
    while 1 < n:
        if n % factor == 0:
            factors.append(factor)
            n = n / factor
        else:
            factor = factor + 1
    return factors


def fraction_to_proper_fraction(rational,) -> typing.Tuple[int, fractions.Fraction]:
    """
    Changes ``rational`` to proper fraction.

    ..  container:: example

        >>> abjad.mathtools.fraction_to_proper_fraction(abjad.Fraction(116, 8))
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

        >>> abjad.mathtools.greatest_common_divisor(84, -94, -144)
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
        ...     print('\t%s\t%s' % (n, abjad.mathtools.greatest_power_of_two_less_equal(n)))
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
        ...     print('\t%s\t%s' % (n, abjad.mathtools.greatest_power_of_two_less_equal(n, i=1)))
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
        message = "must be positive: {!r}."
        message = message.format(n)
        raise ValueError(message)
    return 2 ** (int(math.log(n, 2)) - i)


def integer_equivalent_number_to_integer(number) -> typing.Union[int, float]:
    """
    Changes integer-equivalent ``number`` to integer.

    ..  container:: example

        Returns integer-equivalent number as integer:

        >>> abjad.mathtools.integer_equivalent_number_to_integer(17.0)
        17

    ..  container:: example

        Returns noninteger-equivalent number unchanged:

        >>> abjad.mathtools.integer_equivalent_number_to_integer(17.5)
        17.5

    """
    if is_integer_equivalent_number(number):
        return int(number)
    else:
        return number


def integer_to_base_k_tuple(n, k) -> typing.Tuple[int, ...]:
    """
    Changes nonnegative integer ``n`` to base-`k` tuple.

    ..  container:: example

        Gets base-10 digits of 1066:

        >>> abjad.mathtools.integer_to_base_k_tuple(1066, 10)
        (1, 0, 6, 6)

    ..  container:: example

        Gets base-2 digits of 1066:

        >>> abjad.mathtools.integer_to_base_k_tuple(1066, 2)
        (1, 0, 0, 0, 0, 1, 0, 1, 0, 1, 0)

    ..  container:: example

        Gets base-26 digits of 1066:

        >>> abjad.mathtools.integer_to_base_k_tuple(1066, 26)
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
        current_power = k ** current_exponent
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
        ...     print('{}\t{}'.format(n, abjad.mathtools.integer_to_binary_string(n)))
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
        ...     print('%s\t%s' % (n, abjad.mathtools.is_assignable_integer(n)))
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

        >>> abjad.mathtools.is_integer_equivalent(12.0)
        True

        >>> abjad.mathtools.is_integer_equivalent('12')
        True

        >>> abjad.mathtools.is_integer_equivalent('foo')
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

        >>> tuple_ = (2.0, '3', abjad.Fraction(4, 1))
        >>> abjad.mathtools.is_integer_equivalent_n_tuple(tuple_, 3)
        True

        >>> tuple_ = (2.5, '3', abjad.Fraction(4, 1))
        >>> abjad.mathtools.is_integer_equivalent_n_tuple(tuple_, 3)
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

        >>> abjad.mathtools.is_integer_equivalent_number(12.0)
        True

        >>> abjad.mathtools.is_integer_equivalent_number(abjad.Duration(1, 2))
        False

    """
    if int(argument) == argument:
        return True
    return False


def is_nonnegative_integer(argument) -> bool:
    """
    Is true when ``argument`` equals a nonnegative integer.

    ..  container:: example

        >>> abjad.mathtools.is_nonnegative_integer(99)
        True

        >>> abjad.mathtools.is_nonnegative_integer(0)
        True

        >>> abjad.mathtools.is_nonnegative_integer(-1)
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
        >>> abjad.mathtools.is_nonnegative_integer_equivalent_number(duration)
        True

    """
    return is_integer_equivalent_number(argument) and 0 <= argument


def is_nonnegative_integer_power_of_two(argument) -> bool:
    """
    Is true when ``argument`` is a nonnegative integer power of 2.

    ..  container:: example

        >>> for n in range(10):
        ...     print(n, abjad.mathtools.is_nonnegative_integer_power_of_two(n))
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

        >>> abjad.mathtools.is_positive_integer(99)
        True

        >>> abjad.mathtools.is_positive_integer(0)
        False

        >>> abjad.mathtools.is_positive_integer(-1)
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

        >>> abjad.mathtools.is_positive_integer_equivalent_number(
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
        ...     print(n, abjad.mathtools.is_positive_integer_power_of_two(n))
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

        >>> abjad.mathtools.least_common_multiple(2, 4, 5, 10, 20)
        20

        >>> abjad.mathtools.least_common_multiple(4, 4)
        4

        >>> abjad.mathtools.least_common_multiple(4, 5)
        20

        >>> abjad.mathtools.least_common_multiple(4, 6)
        12

        >>> abjad.mathtools.least_common_multiple(4, 7)
        28

        >>> abjad.mathtools.least_common_multiple(4, 8)
        8

        >>> abjad.mathtools.least_common_multiple(4, 9)
        36

        >>> abjad.mathtools.least_common_multiple(4, 10)
        20

        >>> abjad.mathtools.least_common_multiple(4, 11)
        44

    """
    if len(integers) == 1:
        if not isinstance(integers[0], int):
            message = "must be integer: {!r}."
            message = message.format(integers[0])
            raise TypeError(message)
        if not 0 < integers[0]:
            message = "must be positive: {!r}."
            message = message.format(integers[0])
            raise ValueError(message)
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


def partition_integer_by_ratio(n, ratio) -> typing.List[int]:
    """
    Partitions positive integer-equivalent ``n`` by ``ratio``.

    ..  container:: example

        >>> abjad.mathtools.partition_integer_by_ratio(10, [1, 2])
        [3, 7]

    ..  container:: example

        Partitions positive integer-equivalent ``n`` by ``ratio`` with negative
        parts:

        >>> abjad.mathtools.partition_integer_by_ratio(10, [1, -2])
        [3, -7]

    ..  container:: example

        Partitions negative integer-equivalent ``n`` by ``ratio``:

        >>> abjad.mathtools.partition_integer_by_ratio(-10, [1, 2])
        [-3, -7]

    ..  container:: example

        Partitions negative integer-equivalent ``n`` by ``ratio`` with negative
        parts:

        >>> abjad.mathtools.partition_integer_by_ratio(-10, [1, -2])
        [-3, 7]

    ..  container:: example

        More examples:

        >>> abjad.mathtools.partition_integer_by_ratio(10, [1])
        [10]

        >>> abjad.mathtools.partition_integer_by_ratio(10, [1, 1])
        [5, 5]

        >>> abjad.mathtools.partition_integer_by_ratio(10, [1, -1, -1])
        [3, -4, -3]

        >>> abjad.mathtools.partition_integer_by_ratio(-10, [1, 1, 1, 1])
        [-3, -2, -3, -2]

        >>> abjad.mathtools.partition_integer_by_ratio(-10, [1, 1, 1, 1, 1])
        [-2, -2, -2, -2, -2]

    Returns result with weight equal to absolute value of ``n``.
    """
    if not is_integer_equivalent_number(n):
        message = "is not integer-equivalent number: {!r}."
        message = message.format(n)
        raise TypeError(message)
    ratio = Ratio(ratio).numbers
    if not all(is_integer_equivalent_number(part) for part in ratio):
        message = "some parts in {!r} not integer-equivalent numbers."
        message = message.format(ratio)
        raise TypeError(message)
    result = [0]
    divisions = [float(abs(n)) * abs(part) / weight(ratio) for part in ratio]
    cumulative_divisions = cumulative_sums(divisions, start=None)
    for division in cumulative_divisions:
        rounded_division = int(round(division)) - sum(result)
        if division - round(division) == 0.5:
            rounded_division += 1
        result.append(rounded_division)
    result = result[1:]
    if sign(n) == -1:
        result = [-x for x in result]
    ratio_signs = [sign(x) for x in ratio]
    result = [pair[0] * pair[1] for pair in zip(ratio_signs, result)]
    return result


def partition_integer_into_canonic_parts(
    n, decrease_parts_monotonically=True
) -> typing.Tuple[int, ...]:
    """
    Partitions integer ``n`` into canonic parts.

    ..  container:: example

        Returns all parts positive on positive ``n``:

        >>> for n in range(1, 11):
        ...     print(n, abjad.mathtools.partition_integer_into_canonic_parts(n))
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
        ...     print(n, abjad.mathtools.partition_integer_into_canonic_parts(n))
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
        ...     print(n, abjad.mathtools.partition_integer_into_canonic_parts(n,
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

        >>> abjad.mathtools.sign(-96.2)
        -1

        Returns 0 when ``n`` is 0:

        >>> abjad.mathtools.sign(0)
        0

        Returns 1 on positive ``n``:

        >>> abjad.mathtools.sign(abjad.Duration(9, 8))
        1

    """
    return (0 < n) - (n < 0)


def weight(argument) -> int:
    """
    Gets weight of ``argument``.

    ..  container:: example

        >>> abjad.mathtools.weight([-1, -2, 3, 4, 5])
        15

    ..  container:: example

        >>> abjad.mathtools.weight([])
        0

    Defined equal to sum of the absolute value of items in ``argument``.
    """
    return sum([abs(_) for _ in argument])


def yield_all_compositions_of_integer(n) -> typing.Generator:
    """
    Yields all compositions of positive integer ``n``.

    ..  container:: example

        >>> for tuple_ in abjad.mathtools.yield_all_compositions_of_integer(5):
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


### CLASSES ###


class Infinity(object):
    """
    Infinity.

    ..  container:: example

        All numbers compare less than infinity:

        >>> 9999999 < Infinity
        True

        >>> 2**38 < Infinity
        True

    ..  container:: example

        Infinity compares equal to itself:

        >>> Infinity == Infinity
        True

    ..  container:: example

        Negative infinity compares less than infinity:

        >>> NegativeInfinity < Infinity
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
        Is true when ``argument`` is also infinity.
        """
        return StorageFormatManager.compare_objects(self, argument)

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

        Redefined with ``__eq__()``.
        """
        hash_values = StorageFormatManager(self).get_hash_values()
        try:
            result = hash(hash_values)
        except TypeError:
            raise TypeError(f"unhashable type: {self}")
        return result

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
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    def __sub__(self, argument):
        """
        Subtracts ``argument`` from infinity.

        Returns infinity or 0 if ``argument`` is also infinity.
        """
        if argument is self:
            return 0
        return self

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        from abjad import system

        return system.FormatSpecification(
            client=self,
            repr_text=type(self).__name__,
            storage_format_text=type(self).__name__,
        )


class NegativeInfinity(Infinity):
    """
    Negative infinity.

    ..  container:: example

        All numbers compare greater than negative infinity:

        >>> NegativeInfinity < -9999999
        True

    ..  container:: example

        Negative infinity compares equal to itself:

        >>> NegativeInfinity == NegativeInfinity
        True

    ..  container:: example

        Negative infinity compares less than infinity:

        >>> NegativeInfinity < Infinity
        True

    Initializes as a system singleton at start-up.

    Available as a built-in after Abjad start.
    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self):
        self._value = float("-infinity")


class NonreducedFraction(fractions.Fraction):
    """
    Nonreduced fraction.

    ..  container:: example

        Initializes with an integer numerator and integer denominator:

        >>> abjad.NonreducedFraction(3, 6)
        NonreducedFraction(3, 6)

    ..  container:: example

        Initializes with only an integer denominator:

        >>> abjad.NonreducedFraction(3)
        NonreducedFraction(3, 1)

    ..  container:: example

        Initializes with an integer pair:

        >>> abjad.NonreducedFraction((3, 6))
        NonreducedFraction(3, 6)

    ..  container:: example

        Initializes with an integer singleton:

        >>> abjad.NonreducedFraction((3,))
        NonreducedFraction(3, 1)

    ..  container:: example

        Nonreduced fractions inherit from built-in fraction:

        >>> isinstance(abjad.NonreducedFraction(3, 6), abjad.Fraction)
        True

    ..  container:: example

        Nonreduced fractions are numbers:

        >>> import numbers

        >>> isinstance(abjad.NonreducedFraction(3, 6), numbers.Number)
        True

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_numerator", "_denominator")

    ### CONSTRUCTOR ###

    # dummy docstring prevents Sphinx warnings
    def __new__(class_, *arguments):
        """
        Constructs nonreduced fraction.
        """
        is_fraction_like = False
        if len(arguments) == 1:
            try:
                numerator = arguments[0].numerator
                denominator = arguments[0].denominator
                is_fraction_like = True
            except AttributeError:
                pass
        if is_fraction_like:
            pass
        elif len(arguments) == 1 and isinstance(arguments[0], int):
            numerator = arguments[0]
            denominator = 1
        elif (
            len(arguments) == 1
            and isinstance(arguments[0], tuple)
            and len(arguments[0]) == 1
        ):
            numerator = arguments[0][0]
            denominator = 1
        elif (
            len(arguments) == 1
            and isinstance(arguments[0], tuple)
            and isinstance(arguments[0][0], int)
            and isinstance(arguments[0][1], int)
        ):
            numerator, denominator = arguments[0]
        elif len(arguments) == 1 and isinstance(arguments[0], str):
            numerator, denominator = class_._parse_input_string(arguments[0])
        elif (
            isinstance(arguments, tuple)
            and len(arguments) == 2
            and isinstance(arguments[0], int)
            and isinstance(arguments[1], int)
        ):
            numerator = arguments[0]
            denominator = arguments[1]
        elif len(arguments) == 0:
            numerator = 0
            denominator = 1
        else:
            message = "can not initialize {}: {!r}."
            message = message.format(class_.__name__, arguments)
            raise ValueError(message)
        numerator *= sign(denominator)
        denominator = abs(denominator)
        self = fractions.Fraction.__new__(class_, numerator, denominator)
        self._numerator = numerator
        self._denominator = denominator
        return self

    def __init__(self, *arguments):
        """
        Dummy initializer to satisfy mypy.
        """
        pass

    ### SPECIAL METHODS ###

    def __abs__(self):
        """
        Gets absolute value of nonreduced fraction.

        ..  container:: example

            >>> abs(abjad.NonreducedFraction(-3, 3))
            NonreducedFraction(3, 3)

        Returns nonreduced fraction.
        """
        pair = (abs(self.numerator), self.denominator)
        return self._from_pair(pair)

    def __add__(self, argument):
        """
        Adds ``argument`` to nonreduced fraction.

        ..  container:: example

            >>> abjad.NonreducedFraction(3, 3) + 1
            NonreducedFraction(6, 3)

            >>> 1 + abjad.NonreducedFraction(3, 3)
            NonreducedFraction(6, 3)

        Returns nonreduced fraction.
        """
        if isinstance(argument, int):
            numerator = self.numerator + argument * self.denominator
            pair = (numerator, self.denominator)
            return self._from_pair(pair)
        if getattr(argument, "denominator", "foo") == "foo":
            raise ValueError(argument)
        if self.denominator == argument.denominator:
            numerator = self.numerator + argument.numerator
            pair = (numerator, self.denominator)
            return self._from_pair(pair)
        else:
            denominators = [self.denominator, argument.denominator]
            denominator = least_common_multiple(*denominators)
            self_multiplier = denominator // self.denominator
            argument_multiplier = denominator // argument.denominator
            self_numerator = self_multiplier * self.numerator
            argument_numerator = argument_multiplier * argument.numerator
            pair = (self_numerator + argument_numerator, denominator)
            return self._from_pair(pair)

    def __div__(self, argument):
        """
        Divides nonreduced fraction by ``argument``.

        ..  container:: example

            >>> abjad.NonreducedFraction(3, 3) / 1
            NonreducedFraction(3, 3)

        Returns nonreduced fraction.
        """
        denominators = [self.denominator]
        if isinstance(argument, type(self)):
            denominators.append(argument.denominator)
            argument = argument.reduce()
        fraction = self.reduce() / argument
        return self._fraction_with_denominator(fraction, max(denominators))

    def __eq__(self, argument):
        """
        Is true when ``argument`` equals nonreduced fraction.

        ..  container:: example

            >>> abjad.NonreducedFraction(3, 3) == 1
            True

        Returns true or false.
        """
        return self.reduce() == argument

    def __format__(self, format_specification=""):
        """
        Formats nonreduced fraction.

        ..  container:: example

            >>> fraction = abjad.NonreducedFraction(-6, 3)
            >>> print(format(fraction))
            abjad.NonreducedFraction(-6, 3)

        Returns string.
        """
        if format_specification in ("", "storage"):
            return StorageFormatManager(self).get_storage_format()
        return str(self)

    def __ge__(self, argument):
        """
        Is true when nonreduced fraction is greater than or equal to
        ``argument``.

        ..  container:: example

            >>> abjad.NonreducedFraction(3, 3) >= 1
            True

        Returns true or false.
        """
        return self.reduce() >= argument

    def __gt__(self, argument):
        """
        Is true when nonreduced fraction is greater than ``argument``.

        ..  container:: example

            >>> abjad.NonreducedFraction(3, 3) > 1
            False

        Returns true or false.
        """
        return self.reduce() > argument

    def __hash__(self):
        """
        Hashes nonreduced fraction.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        """
        return super().__hash__()

    def __le__(self, argument):
        """
        Is true when nonreduced fraction is less than or equal to ``argument``.

        ..  container:: example

            >>> abjad.NonreducedFraction(3, 3) <= 1
            True

        Returns true or false.
        """
        return self.reduce() <= argument

    def __lt__(self, argument):
        """
        Is true when nonreduced fraction is less than ``argument``.

        ..  container:: example

            >>> abjad.NonreducedFraction(3, 3) < 1
            False

        Returns true or false.
        """
        return self.reduce() < argument

    def __mul__(self, argument):
        """
        Multiplies nonreduced fraction by ``argument``.

        ..  container:: example

            >>> abjad.NonreducedFraction(3, 3) * 3
            NonreducedFraction(9, 3)

        Returns nonreduced fraction.
        """
        denominators = [self.denominator]
        if isinstance(argument, type(self)):
            denominators.append(argument.denominator)
            argument = argument.reduce()
        fraction = self.reduce() * argument
        return self._fraction_with_denominator(fraction, max(denominators))

    def __neg__(self):
        """
        Negates nonreduced fraction.

        ..  container:: example

            >>> -abjad.NonreducedFraction(3, 3)
            NonreducedFraction(-3, 3)

        Returns nonreduced fraction.
        """
        pair = (-self.numerator, self.denominator)
        return self._from_pair(pair)

    def __pow__(self, argument):
        """
        Raises nonreduced fraction to ``argument``.

        ..  container:: example

            >>> abjad.NonreducedFraction(3, 6) ** -1
            NonreducedFraction(6, 3)

        Returns nonreduced fraction.
        """
        if argument == -1:
            pair = (self.denominator, self.numerator)
            return self._from_pair(pair)
        return super().__pow__(argument)

    def __radd__(self, argument):
        """
        Adds nonreduced fraction to ``argument``.

        ..  container:: example

            >>> 1 + abjad.NonreducedFraction(3, 3)
            NonreducedFraction(6, 3)

        Returns nonreduced fraction.
        """
        return self + argument

    def __rdiv__(self, argument):
        """
        Divides ``argument`` by nonreduced fraction.

        ..  container:: example

            >>> 1 / abjad.NonreducedFraction(3, 3)
            NonreducedFraction(3, 3)

        Returns nonreduced fraction.
        """
        denominators = [self.denominator]
        if isinstance(argument, type(self)):
            denominators.append(argument.denominator)
            argument = argument.reduce()
        fraction = argument / self.reduce()
        return self._fraction_with_denominator(fraction, max(denominators))

    __rtruediv__ = __rdiv__

    def __repr__(self):
        """
        Gets interpreter representation of nonreduced fraction.

        ..  container:: example

            >>> abjad.NonreducedFraction(3, 6)
            NonreducedFraction(3, 6)

        Returns string.
        """
        return StorageFormatManager(self).get_repr_format()

    def __rmul__(self, argument):
        """
        Multiplies ``argument`` by nonreduced fraction.

        ..  container:: example

            >>> 3 * abjad.NonreducedFraction(3, 3)
            NonreducedFraction(9, 3)

        Returns nonreduced fraction.
        """
        return self * argument

    def __rsub__(self, argument):
        """
        Subtracts nonreduced fraction from ``argument``.

        ..  container:: example

            >>> 1 - abjad.NonreducedFraction(3, 3)
            NonreducedFraction(0, 3)

        Returns nonreduced fraction.
        """
        return -self + argument

    def __str__(self):
        """
        Gets string representation of nonreduced fraction.

        ..  container:: example

            >>> fraction = abjad.NonreducedFraction(-6, 3)

            >>> str(fraction)
            '-6/3'

        Returns string.
        """
        return "{}/{}".format(self.numerator, self.denominator)

    def __sub__(self, argument):
        """
        Subtracts ``argument`` from nonreduced fraction.

        ..  container:: example

            >>> abjad.NonreducedFraction(3, 3) - 2
            NonreducedFraction(-3, 3)

            >>> abjad.NonreducedFraction(5, 4) - abjad.NonreducedFraction(18, 16)
            NonreducedFraction(2, 16)

            >>> abjad.NonreducedFraction(18, 16) - abjad.NonreducedFraction(5, 4)
            NonreducedFraction(-2, 16)

        Returns nonreduced fraction.
        """
        denominators = [self.denominator]
        if isinstance(argument, type(self)):
            denominators.append(argument.denominator)
            argument = argument.reduce()
        fraction = self.reduce() - argument
        return self._fraction_with_denominator(fraction, max(denominators))

    def __truediv__(self, argument) -> "NonreducedFraction":
        """
        Divides nonreduced fraction in Python 3.

        Returns nonreduced fraction.
        """
        return self.__div__(argument)

    ### PRIVATE METHODS ###

    def _fraction_with_denominator(self, fraction, denominator):
        denominators = [denominator, fraction.denominator]
        denominator = least_common_multiple(*denominators)
        result = self._from_pair(fraction)
        result = result.with_denominator(denominator)
        return result

    def _from_pair(self, pair):
        """
        Method is designed to be subclassed.
        """
        return type(self)(pair)

    def _get_format_specification(self):
        return FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_args_values=[self.numerator, self.denominator],
            storage_format_is_indented=False,
            storage_format_kwargs_names=[],
        )

    @staticmethod
    def _parse_input_string(string):
        if "/" in string:
            numerator, denominator = string.split("/")
            numerator = int(numerator)
            denominator = int(denominator)
        else:
            numerator = int(string)
            denominator = 1
        return numerator, denominator

    ### PUBLIC METHODS ###

    def multiply(self, multiplier, preserve_numerator=False) -> "NonreducedFraction":
        """
        Multiplies nonreduced fraction by ``multiplier`` with numerator
        preservation where possible.

        ..  container:: example

            >>> fraction = abjad.NonreducedFraction(9, 16)

            >>> fraction.multiply((2, 3), preserve_numerator=True)
            NonreducedFraction(9, 24)

            >>> fraction.multiply((1, 2), preserve_numerator=True)
            NonreducedFraction(9, 32)

            >>> fraction.multiply((5, 6), preserve_numerator=True)
            NonreducedFraction(45, 96)

            >>> fraction = abjad.NonreducedFraction(3, 8)

            >>> fraction.multiply((2, 3), preserve_numerator=True)
            NonreducedFraction(3, 12)

        """
        if preserve_numerator:
            multiplier = fractions.Fraction(*multiplier)
            self_denominator = self.denominator
            candidate_result_denominator = self_denominator / multiplier
            if candidate_result_denominator.denominator == 1:
                pair = (self.numerator, candidate_result_denominator.numerator)
                return self._from_pair(pair)
            else:
                denominator = candidate_result_denominator.denominator
                result_numerator = self.numerator * denominator
                result_denominator = candidate_result_denominator.numerator
                pair = (result_numerator, result_denominator)
                return self._from_pair(pair)
        else:
            return multiplier * self

    def multiply_with_cross_cancelation(self, multiplier) -> "NonreducedFraction":
        """
        Multiplies nonreduced fraction by ``argument`` with cross-cancelation.

        ..  container:: example

            >>> fraction = abjad.NonreducedFraction(4, 8)

            >>> fraction.multiply_with_cross_cancelation((2, 3))
            NonreducedFraction(4, 12)

            >>> fraction.multiply_with_cross_cancelation((4, 1))
            NonreducedFraction(4, 2)

            >>> fraction.multiply_with_cross_cancelation((3, 5))
            NonreducedFraction(12, 40)

            >>> fraction.multiply_with_cross_cancelation((6, 5))
            NonreducedFraction(12, 20)

            >>> fraction = abjad.NonreducedFraction(5, 6)
            >>> fraction.multiply_with_cross_cancelation((6, 5))
            NonreducedFraction(1, 1)

        """
        multiplier = fractions.Fraction(*multiplier)
        self_numerator_factors = factors(self.numerator)
        multiplier_denominator_factors = factors(multiplier.denominator)
        for factor in multiplier_denominator_factors[:]:
            if factor in self_numerator_factors:
                self_numerator_factors.remove(factor)
                multiplier_denominator_factors.remove(factor)
        self_denominator_factors = factors(self.denominator)
        multiplier_numerator_factors = factors(multiplier.numerator)
        for factor in multiplier_numerator_factors[:]:
            if factor in self_denominator_factors:
                self_denominator_factors.remove(factor)
                multiplier_numerator_factors.remove(factor)
        result_numerator_factors = self_numerator_factors + multiplier_numerator_factors
        result_denominator_factors = (
            self_denominator_factors + multiplier_denominator_factors
        )
        result_numerator = 1
        for factor in result_numerator_factors:
            result_numerator *= factor
        result_denominator = 1
        for factor in result_denominator_factors:
            result_denominator *= factor
        pair = (result_numerator, result_denominator)
        return self._from_pair(pair)

    def multiply_without_reducing(self, argument) -> "NonreducedFraction":
        """
        Multiplies nonreduced fraction by ``argument`` without reducing.

        ..  container:: example

            >>> fraction = abjad.NonreducedFraction(3, 8)

            >>> fraction.multiply_without_reducing((3, 3))
            NonreducedFraction(9, 24)

            >>> fraction = abjad.NonreducedFraction(4, 8)

            >>> fraction.multiply_without_reducing((4, 5))
            NonreducedFraction(16, 40)

            >>> fraction.multiply_without_reducing((3, 4))
            NonreducedFraction(12, 32)

        """
        argument = self._from_pair(argument)
        numerator = self.numerator * argument.numerator
        denominator = self.denominator * argument.denominator
        pair = (numerator, denominator)
        return self._from_pair(pair)

    def reduce(self) -> fractions.Fraction:
        """
        Reduces nonreduced fraction.

        ..  container:: example

            >>> fraction = abjad.NonreducedFraction(-6, 3)

            >>> fraction.reduce()
            Fraction(-2, 1)

        """
        return fractions.Fraction(self.numerator, self.denominator)

    def with_denominator(self, denominator) -> "NonreducedFraction":
        """
        Returns new nonreduced fraction with integer ``denominator``.

        ..  container:: example

            >>> abjad.NonreducedFraction(3, 6).with_denominator(12)
            NonreducedFraction(6, 12)

        ..  container:: example

            >>> for numerator in range(12):
            ...     fraction = abjad.NonreducedFraction(numerator, 6)
            ...     print(fraction, fraction.with_denominator(12))
            ...
            0/6 0/12
            1/6 2/12
            2/6 4/12
            3/6 6/12
            4/6 8/12
            5/6 10/12
            6/6 12/12
            7/6 14/12
            8/6 16/12
            9/6 18/12
            10/6 20/12
            11/6 22/12

            >>> for numerator in range(12):
            ...     fraction = abjad.NonreducedFraction(numerator, 6)
            ...     print(fraction, fraction.with_denominator(8))
            ...
            0/6 0/8
            1/6 1/6
            2/6 2/6
            3/6 4/8
            4/6 4/6
            5/6 5/6
            6/6 8/8
            7/6 7/6
            8/6 8/6
            9/6 12/8
            10/6 10/6
            11/6 11/6

            >>> for numerator in range(12):
            ...     fraction = abjad.NonreducedFraction(numerator, 6)
            ...     print(fraction, fraction.with_denominator(12))
            ...
            0/6 0/12
            1/6 2/12
            2/6 4/12
            3/6 6/12
            4/6 8/12
            5/6 10/12
            6/6 12/12
            7/6 14/12
            8/6 16/12
            9/6 18/12
            10/6 20/12
            11/6 22/12

        """
        current_numerator, current_denominator = self.pair
        multiplier = fractions.Fraction(denominator, current_denominator)
        new_numerator = multiplier * current_numerator
        new_denominator = multiplier * current_denominator
        if new_numerator.denominator == 1 and new_denominator.denominator == 1:
            pair = (new_numerator.numerator, new_denominator.numerator)
        else:
            pair = (current_numerator, current_denominator)
        return self._from_pair(pair)

    def with_multiple_of_denominator(self, denominator) -> "NonreducedFraction":
        """
        Returns new nonreduced fraction with multiple of integer
        ``denominator``.

        ..  container:: example

            >>> fraction = abjad.NonreducedFraction(3, 6)

            >>> fraction.with_multiple_of_denominator(5)
            NonreducedFraction(5, 10)

        ..  container:: example

            >>> abjad.NonreducedFraction(1, 2).with_multiple_of_denominator(2)
            NonreducedFraction(1, 2)

            >>> abjad.NonreducedFraction(1, 2).with_multiple_of_denominator(4)
            NonreducedFraction(2, 4)

            >>> abjad.NonreducedFraction(1, 2).with_multiple_of_denominator(8)
            NonreducedFraction(4, 8)

            >>> abjad.NonreducedFraction(1, 2).with_multiple_of_denominator(16)
            NonreducedFraction(8, 16)

        """
        result = self.with_denominator(denominator)
        while not result.denominator == denominator:
            denominator *= 2
            result = result.with_denominator(denominator)
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def denominator(self) -> int:
        """
        Gets denominator of nonreduced fraction.

        ..  container:: example

            >>> abjad.NonreducedFraction(-6, 3).denominator
            3

        """
        return self._denominator

    @property
    def imag(self) -> int:
        """
        Gets zero because nonreduced fractions have no imaginary part.

            >>> abjad.NonreducedFraction(-6, 3).imag
            0

        """
        return 0

    @property
    def numerator(self) -> int:
        """
        Gets numerator of nonreduced fraction.

            >>> abjad.NonreducedFraction(-6, 3).numerator
            -6

        """
        return self._numerator

    @property
    def pair(self) -> typing.Tuple[int, int]:
        """
        Gets (numerator, denominator) pair of nonreduced fraction.

            >>> abjad.NonreducedFraction(-6, 3).pair
            (-6, 3)

        """
        return self.numerator, self.denominator

    @property
    def real(self) -> "NonreducedFraction":
        """
        Gets nonreduced fraction because nonreduced fractions are their own
        real component.

            >>> abjad.NonreducedFraction(-6, 3).real
            NonreducedFraction(-6, 3)

        """
        return self


class NonreducedRatio(collections.abc.Sequence):
    """
    Nonreduced ratio.

    ..  container:: example

        Initializes from numbers:

        >>> abjad.NonreducedRatio((2, 4))
        NonreducedRatio((2, 4))

        >>> abjad.NonreducedRatio((2, 4, 2))
        NonreducedRatio((2, 4, 2))

    ..  container:: example

        Initializes from string:

        >>> abjad.NonreducedRatio("2:4")
        NonreducedRatio((2, 4))

        >>> abjad.NonreducedRatio("2:4:2")
        NonreducedRatio((2, 4, 2))

    """

    ### CLASS VARIABLES ###

    __slots__ = ("_numbers",)

    ### INITIALIZER ###

    def __init__(self, numbers=(1, 1)):
        if isinstance(numbers, type(self)):
            numbers = numbers.numbers
        elif isinstance(numbers, str):
            strings = numbers.split(":")
            numbers = [int(_) for _ in strings]
        numbers = tuple(numbers)
        self._numbers = numbers

    ### SPECIAL METHODS ###

    def __contains__(self, argument):
        """
        Is true when ratio contains ``argument``.

        Returns true or false.
        """
        return argument in self._numbers

    def __eq__(self, argument):
        """
        Is true when ``argument`` is a nonreduced ratio with numerator and
        denominator equal to those of this nonreduced ratio.

        Returns true or false.
        """
        return StorageFormatManager.compare_objects(self, argument)

    def __format__(self, format_specification=""):
        """
        Formats duration.

        ..  container:: example

            >>> ratio = abjad.NonreducedRatio((2, 4, 2))
            >>> print(format(ratio))
            abjad.NonreducedRatio((2, 4, 2))

        Returns string.
        """
        import abjad

        if format_specification in ("", "storage"):
            return abjad.StorageFormatManager(self).get_storage_format()
        return str(self)

    def __getitem__(self, argument):
        """
        Gets item or slice identified by ``argument``.

        ..  container:: example

            >>> ratio = abjad.NonreducedRatio((2, 4, 2))
            >>> ratio[1]
            4

        Returns integer or tuple.
        """
        if isinstance(argument, slice):
            return tuple(self._numbers.__getitem__(argument))
        return self._numbers.__getitem__(argument)

    def __hash__(self):
        """
        Hashes non-reduced ratio.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        """
        return super().__hash__()

    def __iter__(self):
        """
        Iterates ratio.

        Returns generator.
        """
        return iter(self._numbers)

    def __len__(self):
        """
        Gets length of ratio.

        ..  container:: example

            >>> ratio = abjad.NonreducedRatio((2, 4, 2))
            >>> len(ratio)
            3

        Returns integer.
        """
        return len(self._numbers)

    def __repr__(self) -> str:
        """
        Gets interpreter representation.
        """
        return StorageFormatManager(self).get_repr_format()

    def __reversed__(self):
        """
        Iterates ratio in reverse.

        Returns generator.
        """
        return reversed(self._numbers)

    def __rtruediv__(self, number):
        """
        Divides ``number`` by ratio.

        ..  container:: example

            >>> 1 / abjad.Ratio((1, 1, 3))
            [Fraction(1, 5), Fraction(1, 5), Fraction(3, 5)]

        ..  container:: example

            >>> abjad.Fraction(1) / abjad.Ratio((1, 1, 3))
            [Fraction(1, 5), Fraction(1, 5), Fraction(3, 5)]

        ..  container:: example

            >>> 1.0 / abjad.Ratio((1, 1, 3))
            [0.2, 0.2, 0.6]

        Returns list of fractions or list of floats.
        """
        denominator = sum(self.numbers)
        factors = [fractions.Fraction(_, denominator) for _ in self.numbers]
        result = [_ * number for _ in factors]
        return result

    __rdiv__ = __rtruediv__

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        import abjad

        return abjad.FormatSpecification(
            client=self,
            storage_format_args_values=[self.numbers],
            storage_format_is_indented=False,
            storage_format_kwargs_names=[],
        )

    ### PUBLIC PROPERTIES ###

    @property
    def multipliers(self):
        """
        Gets multipliers of nonreduced ratio.

        ..  container:: example

            Nonreduced ratio of two numbers:

            >>> ratio = abjad.NonreducedRatio((2, 4))
            >>> ratio.multipliers
            (Multiplier(1, 3), Multiplier(2, 3))

        ..  container:: example

            Nonreduced ratio of three numbers:

            >>> ratio = abjad.NonreducedRatio((2, 4, 2))
            >>> ratio.multipliers
            (Multiplier(1, 4), Multiplier(1, 2), Multiplier(1, 4))

        Returns tuple of multipliers.
        """
        import abjad

        weight = sum(self.numbers)
        multipliers = [abjad.Multiplier((_, weight)) for _ in self.numbers]
        multipliers = tuple(multipliers)
        return multipliers

    @property
    def numbers(self):
        """
        Gets numbers of nonreduced ratio.

        ..  container:: example

            Nonreduced ratio of two numbers:

            >>> ratio = abjad.NonreducedRatio((2, 4))
            >>> ratio.numbers
            (2, 4)

        ..  container:: example

            Nonreduced ratio of three numbers:

            >>> ratio = abjad.NonreducedRatio((2, 4, 2))
            >>> ratio.numbers
            (2, 4, 2)

        Set to tuple of two or more numbers.

        Returns tuple of two or more numbers.
        """
        return self._numbers

    ### PUBLIC METHODS ###

    def count(self, argument):
        """
        Gets count of ``argument`` in ratio.

        Returns integer.
        """
        return self._numbers.count(argument)

    def index(self, argument):
        """
        Gets index of ``argument`` in ratio.

        Returns integer.
        """
        return self._numbers.index(argument)


class Ratio(NonreducedRatio):
    """
    Ratio.

    ..  container:: example

        Initializes from numbers:

        >>> abjad.Ratio((2, 4))
        Ratio((1, 2))

        >>> abjad.Ratio((2, 4, 2))
        Ratio((1, 2, 1))

    ..  container:: example

        Initializes from string:

        >>> abjad.Ratio("2:4")
        Ratio((1, 2))

        >>> abjad.Ratio("2:4:2")
        Ratio((1, 2, 1))

    """

    ### CLASS VARIABLES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, numbers=(1, 1)):
        if isinstance(numbers, type(self)):
            numbers = numbers.numbers
        elif isinstance(numbers, str):
            strings = numbers.split(":")
            numbers = [int(_) for _ in strings]
        numbers = [int(_) for _ in numbers]
        gcd = greatest_common_divisor(*numbers)
        numbers = [_ // gcd for _ in numbers]
        self._numbers = tuple(numbers)

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        """
        Is true when ``argument`` equals ratio.

        ..  container:: example

            >>> ratio_1 = abjad.Ratio((1, 2, 1))
            >>> ratio_2 = abjad.Ratio((1, 2, 1))
            >>> ratio_3 = abjad.Ratio((2, 3, 3))

            >>> ratio_1 == ratio_1
            True

            >>> ratio_1 == ratio_2
            True

            >>> ratio_1 == ratio_3
            False

            >>> ratio_2 == ratio_1
            True

            >>> ratio_2 == ratio_2
            True

            >>> ratio_2 == ratio_3
            False

            >>> ratio_3 == ratio_1
            False

            >>> ratio_3 == ratio_2
            False

            >>> ratio_3 == ratio_3
            True

        """
        return super().__eq__(argument)

    def __getitem__(self, argument):
        """
        Gets item or slice identified by ``argument``.

        ..  container:: example

            >>> ratio = abjad.Ratio((2, 4, 2))
            >>> ratio[1]
            2

        Returns integer or tuple.
        """
        if isinstance(argument, slice):
            return tuple(self._numbers.__getitem__(argument))
        return self._numbers.__getitem__(argument)

    def __hash__(self):
        """
        Hashes ratio.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        """
        return super().__hash__()

    def __len__(self):
        """
        Gets length of ratio.

        ..  container:: example

            >>> ratio = abjad.Ratio((2, 4, 2))
            >>> len(ratio)
            3

        Returns integer.
        """
        return len(self._numbers)

    def __str__(self):
        """
        Gets string representation of ratio.

        ..  container:: example

            Ratio of two numbers:

            >>> str(abjad.Ratio((2, 4)))
            '1:2'

        ..  container:: example

            Ratio of three numbers:

            >>> str(abjad.Ratio((2, 4, 2)))
            '1:2:1'

        Returns string.
        """
        numbers = (str(x) for x in self.numbers)
        return ":".join(numbers)

    ### PUBLIC PROPERTIES ###

    @property
    def multipliers(self):
        """
        Gets multipliers of ratio.

        ..  container:: example

            Ratio of two numbers:

            >>> ratio = abjad.Ratio((2, 4))
            >>> ratio.multipliers
            (Multiplier(1, 3), Multiplier(2, 3))

        ..  container:: example

            Ratio of three numbers:

            >>> ratio = abjad.Ratio((2, 4, 2))
            >>> ratio.multipliers
            (Multiplier(1, 4), Multiplier(1, 2), Multiplier(1, 4))

        Returns tuple of multipliers.
        """
        import abjad

        weight = sum(self.numbers)
        multipliers = [abjad.Multiplier((_, weight)) for _ in self.numbers]
        multipliers = tuple(multipliers)
        return multipliers

    @property
    def numbers(self):
        """
        Gets numbers of ratio.

        ..  container:: example

            Ratio of two numbers:

            >>> ratio = abjad.Ratio((2, 4))
            >>> ratio.numbers
            (1, 2)

        ..  container:: example

            Ratio of three numbers:

            >>> ratio = abjad.Ratio((2, 4, 2))
            >>> ratio.numbers
            (1, 2, 1)

        Set to tuple of two or more numbers.

        Returns tuple of two or more numbers.
        """
        return self._numbers

    @property
    def reciprocal(self):
        """
        Gets reciprocal.

        ..  container:: example

            Gets reciprocal:

            >>> abjad.Ratio((3, 2)).reciprocal
            Ratio((2, 3))

            >>> abjad.Ratio((3, 2, 7)).reciprocal
            Ratio((7, 2, 3))

        Returns new ratio.
        """
        numbers = list(reversed(self.numbers))
        return type(self)(numbers)
