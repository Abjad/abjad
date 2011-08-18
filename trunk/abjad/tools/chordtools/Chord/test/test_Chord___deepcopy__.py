from abjad import *
import copy


def test_Chord___deepcopy___01():
    '''Ensure deepcopied note heads attach correctly to chord.
    '''

    chord_1 = Chord("<c' e' g'>4")
    chord_1[0].tweak.color = 'red'
    chord_2 = copy.deepcopy(chord_1)

    assert chord_2[0]._client is chord_2
    assert chord_2[1]._client is chord_2
    assert chord_2[2]._client is chord_2

    assert chord_1.format == chord_2.format
    assert chord_1 is not chord_2

    assert chord_1[0] == chord_2[0]
    assert chord_1[1] == chord_2[1]
    assert chord_1[2] == chord_2[2]

    assert chord_1[0] is not chord_2[0]
    assert chord_1[1] is not chord_2[1]
    assert chord_1[2] is not chord_2[2]

    assert chord_1.format == "<\n\t\\tweak #'color #red\n\tc'\n\te'\n\tg'\n>4"
    assert chord_2.format == "<\n\t\\tweak #'color #red\n\tc'\n\te'\n\tg'\n>4"
