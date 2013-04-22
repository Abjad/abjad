from abjad.tools import pitchtools
from experimental.tools.musicexpressiontools import StatalServer
__all__ = []


example_aggregates = [
    [-13, -5, 2, 3, 6, 8, 10, 12, 13, 16, 17, 21],
    [-13, -12, -10, -5, -2, 5, 6, 8, 15, 16, 21, 25],
    [-22, -14, -12, -8, -4, -1, 7, 17, 18, 21, 27, 37],
    [-2, 0, 2, 7, 8, 11, 15, 16, 17, 18, 21, 25]]
__all__.append('example_aggregates')

example_octave_transposition = pitchtools.OctaveTranspositionMapping([
    ('[A0, C4)', -12),
    ('[C4, C8)', 12)])
__all__.append('example_octave_transposition')

example_pitches_1 = StatalServer([
    [0, 1, 2, 3, 4, 5],
    [6, 7, 8, 9, 10, 11],
    [12, 13, 14, 15, 16, 17],
    [18, 19, 20, 21, 22, 23]])
__all__.append('example_pitches_1')
