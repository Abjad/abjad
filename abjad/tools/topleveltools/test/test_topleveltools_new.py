# -*- coding: utf-8 -*-
from abjad import *


class Aggregate(abctools.AbjadValueObject):

    __slots__ = ('_pitch_segment', '_ratio')

    def __init__(self, pitch_segment=None, ratio=None):
        if pitch_segment is not None:
            pitch_segment = pitchtools.PitchSegment(pitch_segment)
        self._pitch_segment = pitch_segment
        if ratio is not None:
            ratio = mathtools.Ratio(ratio)
        self._ratio = ratio

    @property
    def pitch_segment(self):
        return self._pitch_segment

    @property
    def ratio(self):
        return self._ratio


def test_topleveltools_new_01():

    old_aggregate = Aggregate(
        pitch_segment=pitchtools.PitchSegment('c d e f'),
        ratio=mathtools.Ratio([1, 2, 3])
        )

    assert format(old_aggregate) == stringtools.normalize(
        r'''
        test_topleveltools_new.Aggregate(
            pitch_segment=pitchtools.PitchSegment(
                (
                    pitchtools.NamedPitch('c'),
                    pitchtools.NamedPitch('d'),
                    pitchtools.NamedPitch('e'),
                    pitchtools.NamedPitch('f'),
                    ),
                item_class=pitchtools.NamedPitch,
                ),
            ratio=mathtools.Ratio((1, 2, 3)),
            )
        ''')

    new_aggregate = new(old_aggregate)

    assert new_aggregate is not old_aggregate
    assert new_aggregate == old_aggregate
    assert format(old_aggregate) == stringtools.normalize(
        r'''
        test_topleveltools_new.Aggregate(
            pitch_segment=pitchtools.PitchSegment(
                (
                    pitchtools.NamedPitch('c'),
                    pitchtools.NamedPitch('d'),
                    pitchtools.NamedPitch('e'),
                    pitchtools.NamedPitch('f'),
                    ),
                item_class=pitchtools.NamedPitch,
                ),
            ratio=mathtools.Ratio((1, 2, 3)),
            )
        ''')
    assert format(new_aggregate) == stringtools.normalize(
        r'''
        test_topleveltools_new.Aggregate(
            pitch_segment=pitchtools.PitchSegment(
                (
                    pitchtools.NamedPitch('c'),
                    pitchtools.NamedPitch('d'),
                    pitchtools.NamedPitch('e'),
                    pitchtools.NamedPitch('f'),
                    ),
                item_class=pitchtools.NamedPitch,
                ),
            ratio=mathtools.Ratio((1, 2, 3)),
            )
        ''')


def test_topleveltools_new_02():

    old_aggregate = Aggregate(
        pitch_segment=pitchtools.PitchSegment('c d e f'),
        ratio=mathtools.Ratio([1, 2, 3])
        )

    assert format(old_aggregate) == stringtools.normalize(
        r'''
        test_topleveltools_new.Aggregate(
            pitch_segment=pitchtools.PitchSegment(
                (
                    pitchtools.NamedPitch('c'),
                    pitchtools.NamedPitch('d'),
                    pitchtools.NamedPitch('e'),
                    pitchtools.NamedPitch('f'),
                    ),
                item_class=pitchtools.NamedPitch,
                ),
            ratio=mathtools.Ratio((1, 2, 3)),
            )
        ''')

    new_aggregate = new(
        old_aggregate,
        ratio=(4, 5),
        )

    assert new_aggregate is not old_aggregate
    assert new_aggregate != old_aggregate
    assert format(old_aggregate) == stringtools.normalize(
        r'''
        test_topleveltools_new.Aggregate(
            pitch_segment=pitchtools.PitchSegment(
                (
                    pitchtools.NamedPitch('c'),
                    pitchtools.NamedPitch('d'),
                    pitchtools.NamedPitch('e'),
                    pitchtools.NamedPitch('f'),
                    ),
                item_class=pitchtools.NamedPitch,
                ),
            ratio=mathtools.Ratio((1, 2, 3)),
            )
        ''')
    assert format(new_aggregate) == stringtools.normalize(
        r'''
        test_topleveltools_new.Aggregate(
            pitch_segment=pitchtools.PitchSegment(
                (
                    pitchtools.NamedPitch('c'),
                    pitchtools.NamedPitch('d'),
                    pitchtools.NamedPitch('e'),
                    pitchtools.NamedPitch('f'),
                    ),
                item_class=pitchtools.NamedPitch,
                ),
            ratio=mathtools.Ratio((4, 5)),
            )
        ''')


def test_topleveltools_new_03():

    old_aggregate = Aggregate(
        pitch_segment=pitchtools.PitchSegment('c d e f'),
        )

    assert format(old_aggregate) == stringtools.normalize(
        r'''
        test_topleveltools_new.Aggregate(
            pitch_segment=pitchtools.PitchSegment(
                (
                    pitchtools.NamedPitch('c'),
                    pitchtools.NamedPitch('d'),
                    pitchtools.NamedPitch('e'),
                    pitchtools.NamedPitch('f'),
                    ),
                item_class=pitchtools.NamedPitch,
                ),
            )
        ''')

    new_aggregate = new(
        old_aggregate,
        pitch_segment='af bf df',
        ratio=(5, 4),
        )

    assert new_aggregate is not old_aggregate
    assert new_aggregate != old_aggregate
    assert format(old_aggregate) == stringtools.normalize(
        r'''
        test_topleveltools_new.Aggregate(
            pitch_segment=pitchtools.PitchSegment(
                (
                    pitchtools.NamedPitch('c'),
                    pitchtools.NamedPitch('d'),
                    pitchtools.NamedPitch('e'),
                    pitchtools.NamedPitch('f'),
                    ),
                item_class=pitchtools.NamedPitch,
                ),
            )
        ''')
    assert format(new_aggregate) == stringtools.normalize(
        r'''
        test_topleveltools_new.Aggregate(
            pitch_segment=pitchtools.PitchSegment(
                (
                    pitchtools.NamedPitch('af'),
                    pitchtools.NamedPitch('bf'),
                    pitchtools.NamedPitch('df'),
                    ),
                item_class=pitchtools.NamedPitch,
                ),
            ratio=mathtools.Ratio((5, 4)),
            )
        ''')


def test_topleveltools_new_04():

    old_aggregate = Aggregate(
        pitch_segment=pitchtools.PitchSegment('c d e f'),
        )

    assert format(old_aggregate) == stringtools.normalize(
        r'''
        test_topleveltools_new.Aggregate(
            pitch_segment=pitchtools.PitchSegment(
                (
                    pitchtools.NamedPitch('c'),
                    pitchtools.NamedPitch('d'),
                    pitchtools.NamedPitch('e'),
                    pitchtools.NamedPitch('f'),
                    ),
                item_class=pitchtools.NamedPitch,
                ),
            )
        ''')

    new_aggregate = new(
        old_aggregate,
        pitch_segment__rotate=2,
        ratio=[4, 5],
        )

    assert new_aggregate is not old_aggregate
    assert new_aggregate != old_aggregate
    assert format(old_aggregate) == stringtools.normalize(
        r'''
        test_topleveltools_new.Aggregate(
            pitch_segment=pitchtools.PitchSegment(
                (
                    pitchtools.NamedPitch('c'),
                    pitchtools.NamedPitch('d'),
                    pitchtools.NamedPitch('e'),
                    pitchtools.NamedPitch('f'),
                    ),
                item_class=pitchtools.NamedPitch,
                ),
            )
        ''')
    assert format(new_aggregate) == stringtools.normalize(
        r'''
        test_topleveltools_new.Aggregate(
            pitch_segment=pitchtools.PitchSegment(
                (
                    pitchtools.NamedPitch('e'),
                    pitchtools.NamedPitch('f'),
                    pitchtools.NamedPitch('c'),
                    pitchtools.NamedPitch('d'),
                    ),
                item_class=pitchtools.NamedPitch,
                ),
            ratio=mathtools.Ratio((4, 5)),
            )
        ''')


def test_topleveltools_new_05():

    old_aggregate = Aggregate(
        pitch_segment=pitchtools.PitchSegment('c d e f'),
        )

    assert format(old_aggregate) == stringtools.normalize(
        r'''
        test_topleveltools_new.Aggregate(
            pitch_segment=pitchtools.PitchSegment(
                (
                    pitchtools.NamedPitch('c'),
                    pitchtools.NamedPitch('d'),
                    pitchtools.NamedPitch('e'),
                    pitchtools.NamedPitch('f'),
                    ),
                item_class=pitchtools.NamedPitch,
                ),
            )
        ''')

    new_aggregate = new(
        old_aggregate,
        ratio=[4, 5],
        pitch_segment__rotate=2,
        )

    assert new_aggregate is not old_aggregate
    assert new_aggregate != old_aggregate
    assert format(old_aggregate) == stringtools.normalize(
        r'''
        test_topleveltools_new.Aggregate(
            pitch_segment=pitchtools.PitchSegment(
                (
                    pitchtools.NamedPitch('c'),
                    pitchtools.NamedPitch('d'),
                    pitchtools.NamedPitch('e'),
                    pitchtools.NamedPitch('f'),
                    ),
                item_class=pitchtools.NamedPitch,
                ),
            )
        ''')
    assert format(new_aggregate) == stringtools.normalize(
        r'''
        test_topleveltools_new.Aggregate(
            pitch_segment=pitchtools.PitchSegment(
                (
                    pitchtools.NamedPitch('e'),
                    pitchtools.NamedPitch('f'),
                    pitchtools.NamedPitch('c'),
                    pitchtools.NamedPitch('d'),
                    ),
                item_class=pitchtools.NamedPitch,
                ),
            ratio=mathtools.Ratio((4, 5)),
            )
        ''')
