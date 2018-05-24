def sign(n):
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

    Returns -1, 0 or 1.
    """
    return (0 < n) - (n < 0)
