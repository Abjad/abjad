from abjad.tools import durationtools


def report_integer_tempo_rewrite_pairs(integer_tempo,
    maximum_numerator=None, maximum_denominator=None):
    '''.. versionadded:: 2.0

    Report `integer_tempo` rewrite pairs.

    Allow no tempo less than half `integer_tempo` or 
    greater than double `integer_tempo`::

        >>> tempotools.report_integer_tempo_rewrite_pairs(
        ...   58, maximum_numerator=8, maximum_denominator=8)
        2:1     29
        1:1     58
        2:3     87
        1:2     116

    With more lenient numerator and denominator::

        >>> tempotools.report_integer_tempo_rewrite_pairs(
        ...     58, maximum_numerator=30, maximum_denominator=30)
        2:1     29
        29:15   30
        29:16   32
        29:17   34
        29:18   36
        29:19   38
        29:20   40
        29:21   42
        29:22   44
        29:23   46
        29:24   48
        29:25   50
        29:26   52
        29:27   54
        29:28   56
        1:1     58
        29:30   60
        2:3     87
        1:2     116

    Return none.
    '''
    from abjad.tools import tempotools

    pairs = tempotools.rewrite_integer_tempo(
      integer_tempo, maximum_numerator=maximum_numerator, maximum_denominator=maximum_denominator)

    for multiplier, tempo in pairs:
      print '{}\t{}'.format(multiplier.prolation_string, tempo)
