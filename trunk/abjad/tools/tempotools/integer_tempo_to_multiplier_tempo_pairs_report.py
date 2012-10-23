from abjad.tools import durationtools


def integer_tempo_to_multiplier_tempo_pairs_report(integer_tempo,
    maximum_numerator=None, maximum_denominator=None):
    '''.. versionadded:: 2.0

    Print all multiplier / tempo pairs possible from `integer_tempo`.

    Allow no tempo less than half `integer_tempo` or 
    greater than double `integer_tempo`::

        >>> tempotools.integer_tempo_to_multiplier_tempo_pairs_report(
        ...   58, maximum_numerator=8, maximum_denominator=8)
        2:1     29
        1:1     58
        2:3     87
        1:2     116

    With more lenient numerator and denominator::

        >>> tempotools.integer_tempo_to_multiplier_tempo_pairs_report(
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

    pairs = tempotools.integer_tempo_to_multiplier_tempo_pairs(
      integer_tempo, maximum_numerator, maximum_denominator)

    for multiplier, tempo in pairs:
      prolation_string = durationtools.rational_to_prolation_string(multiplier)
      print '%s\t%s' % (prolation_string, tempo)
