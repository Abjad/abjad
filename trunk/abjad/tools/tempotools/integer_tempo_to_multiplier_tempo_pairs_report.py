from abjad.tools import durationtools
from abjad.tools.tempotools.integer_tempo_to_multiplier_tempo_pairs import integer_tempo_to_multiplier_tempo_pairs


def integer_tempo_to_multiplier_tempo_pairs_report(integer_tempo,
    maximum_numerator = None, maximum_denominator = None):
    '''.. versionadded:: 2.0

    Print all multiplier, tempo pairs possible from `integer_tempo`.

    Allow no tempi less than ``integer_tempo / 2`` nor greater than
    ``2 * integer_tempo``::

      abjad> from abjad.tools import tempotools

    ::

      abjad> tempotools.integer_tempo_to_multiplier_tempo_pairs_report(58, 8, 8)
      2:1     29
      1:1     58
      2:3     87
      1:2     116

    With more lenient numerator and denominator. ::

      abjad> tempotools.integer_tempo_to_multiplier_tempo_pairs_report(58, 30, 30)
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

    pairs = integer_tempo_to_multiplier_tempo_pairs(
      integer_tempo, maximum_numerator, maximum_denominator)

    for multiplier, tempo in pairs:
      prolation_string = durationtools.rational_to_prolation_string(multiplier)
      print '%s\t%s' % (prolation_string, tempo)
