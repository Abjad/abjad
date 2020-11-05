import abjad


class Aggregate(object):

    __slots__ = ("_pitch_segment", "_ratio")

    def __init__(self, pitch_segment=None, ratio=None):
        if pitch_segment is not None:
            pitch_segment = abjad.PitchSegment(pitch_segment)
        self._pitch_segment = pitch_segment
        if ratio is not None:
            ratio = abjad.Ratio(ratio)
        self._ratio = ratio

    def __eq__(self, argument):
        return abjad.StorageFormatManager.compare_objects(self, argument)

    def __format__(self, format_specification=""):
        return abjad.StorageFormatManager(self).get_storage_format()

    @property
    def pitch_segment(self):
        return self._pitch_segment

    @property
    def ratio(self):
        return self._ratio


def test_new_01():

    old_aggregate = Aggregate(
        pitch_segment=abjad.PitchSegment("c d e f"),
        ratio=abjad.Ratio([1, 2, 3]),
    )

    assert abjad.storage(old_aggregate) == abjad.String.normalize(
        r"""
        test_new.Aggregate(
            pitch_segment=abjad.PitchSegment(
                (
                    abjad.NamedPitch('c'),
                    abjad.NamedPitch('d'),
                    abjad.NamedPitch('e'),
                    abjad.NamedPitch('f'),
                    ),
                item_class=abjad.NamedPitch,
                ),
            ratio=abjad.Ratio((1, 2, 3)),
            )
        """
    )

    new_aggregate = abjad.new(old_aggregate)

    assert new_aggregate is not old_aggregate
    assert new_aggregate == old_aggregate
    assert abjad.storage(old_aggregate) == abjad.String.normalize(
        r"""
        test_new.Aggregate(
            pitch_segment=abjad.PitchSegment(
                (
                    abjad.NamedPitch('c'),
                    abjad.NamedPitch('d'),
                    abjad.NamedPitch('e'),
                    abjad.NamedPitch('f'),
                    ),
                item_class=abjad.NamedPitch,
                ),
            ratio=abjad.Ratio((1, 2, 3)),
            )
        """
    )
    assert abjad.storage(new_aggregate) == abjad.String.normalize(
        r"""
        test_new.Aggregate(
            pitch_segment=abjad.PitchSegment(
                (
                    abjad.NamedPitch('c'),
                    abjad.NamedPitch('d'),
                    abjad.NamedPitch('e'),
                    abjad.NamedPitch('f'),
                    ),
                item_class=abjad.NamedPitch,
                ),
            ratio=abjad.Ratio((1, 2, 3)),
            )
        """
    )


def test_new_02():

    old_aggregate = Aggregate(
        pitch_segment=abjad.PitchSegment("c d e f"),
        ratio=abjad.Ratio([1, 2, 3]),
    )

    assert abjad.storage(old_aggregate) == abjad.String.normalize(
        r"""
        test_new.Aggregate(
            pitch_segment=abjad.PitchSegment(
                (
                    abjad.NamedPitch('c'),
                    abjad.NamedPitch('d'),
                    abjad.NamedPitch('e'),
                    abjad.NamedPitch('f'),
                    ),
                item_class=abjad.NamedPitch,
                ),
            ratio=abjad.Ratio((1, 2, 3)),
            )
        """
    )

    new_aggregate = abjad.new(old_aggregate, ratio=(4, 5))

    assert new_aggregate is not old_aggregate
    assert new_aggregate != old_aggregate
    assert abjad.storage(old_aggregate) == abjad.String.normalize(
        r"""
        test_new.Aggregate(
            pitch_segment=abjad.PitchSegment(
                (
                    abjad.NamedPitch('c'),
                    abjad.NamedPitch('d'),
                    abjad.NamedPitch('e'),
                    abjad.NamedPitch('f'),
                    ),
                item_class=abjad.NamedPitch,
                ),
            ratio=abjad.Ratio((1, 2, 3)),
            )
        """
    )
    assert abjad.storage(new_aggregate) == abjad.String.normalize(
        r"""
        test_new.Aggregate(
            pitch_segment=abjad.PitchSegment(
                (
                    abjad.NamedPitch('c'),
                    abjad.NamedPitch('d'),
                    abjad.NamedPitch('e'),
                    abjad.NamedPitch('f'),
                    ),
                item_class=abjad.NamedPitch,
                ),
            ratio=abjad.Ratio((4, 5)),
            )
        """
    )


def test_new_03():

    old_aggregate = Aggregate(pitch_segment=abjad.PitchSegment("c d e f"))

    assert abjad.storage(old_aggregate) == abjad.String.normalize(
        r"""
        test_new.Aggregate(
            pitch_segment=abjad.PitchSegment(
                (
                    abjad.NamedPitch('c'),
                    abjad.NamedPitch('d'),
                    abjad.NamedPitch('e'),
                    abjad.NamedPitch('f'),
                    ),
                item_class=abjad.NamedPitch,
                ),
            )
        """
    )

    new_aggregate = abjad.new(old_aggregate, pitch_segment="af bf df", ratio=(5, 4))

    assert new_aggregate is not old_aggregate
    assert new_aggregate != old_aggregate
    assert abjad.storage(old_aggregate) == abjad.String.normalize(
        r"""
        test_new.Aggregate(
            pitch_segment=abjad.PitchSegment(
                (
                    abjad.NamedPitch('c'),
                    abjad.NamedPitch('d'),
                    abjad.NamedPitch('e'),
                    abjad.NamedPitch('f'),
                    ),
                item_class=abjad.NamedPitch,
                ),
            )
        """
    )
    assert abjad.storage(new_aggregate) == abjad.String.normalize(
        r"""
        test_new.Aggregate(
            pitch_segment=abjad.PitchSegment(
                (
                    abjad.NamedPitch('af'),
                    abjad.NamedPitch('bf'),
                    abjad.NamedPitch('df'),
                    ),
                item_class=abjad.NamedPitch,
                ),
            ratio=abjad.Ratio((5, 4)),
            )
        """
    )


def test_new_04():

    old_aggregate = Aggregate(pitch_segment=abjad.PitchSegment("c d e f"))

    assert abjad.storage(old_aggregate) == abjad.String.normalize(
        r"""
        test_new.Aggregate(
            pitch_segment=abjad.PitchSegment(
                (
                    abjad.NamedPitch('c'),
                    abjad.NamedPitch('d'),
                    abjad.NamedPitch('e'),
                    abjad.NamedPitch('f'),
                    ),
                item_class=abjad.NamedPitch,
                ),
            )
        """
    )

    new_aggregate = abjad.new(old_aggregate, pitch_segment__rotate=2, ratio=[4, 5])

    assert new_aggregate is not old_aggregate
    assert new_aggregate != old_aggregate
    assert abjad.storage(old_aggregate) == abjad.String.normalize(
        r"""
        test_new.Aggregate(
            pitch_segment=abjad.PitchSegment(
                (
                    abjad.NamedPitch('c'),
                    abjad.NamedPitch('d'),
                    abjad.NamedPitch('e'),
                    abjad.NamedPitch('f'),
                    ),
                item_class=abjad.NamedPitch,
                ),
            )
        """
    )
    assert abjad.storage(new_aggregate) == abjad.String.normalize(
        r"""
        test_new.Aggregate(
            pitch_segment=abjad.PitchSegment(
                (
                    abjad.NamedPitch('e'),
                    abjad.NamedPitch('f'),
                    abjad.NamedPitch('c'),
                    abjad.NamedPitch('d'),
                    ),
                item_class=abjad.NamedPitch,
                ),
            ratio=abjad.Ratio((4, 5)),
            )
        """
    )


def test_new_05():

    old_aggregate = Aggregate(pitch_segment=abjad.PitchSegment("c d e f"))

    assert abjad.storage(old_aggregate) == abjad.String.normalize(
        r"""
        test_new.Aggregate(
            pitch_segment=abjad.PitchSegment(
                (
                    abjad.NamedPitch('c'),
                    abjad.NamedPitch('d'),
                    abjad.NamedPitch('e'),
                    abjad.NamedPitch('f'),
                    ),
                item_class=abjad.NamedPitch,
                ),
            )
        """
    )

    new_aggregate = abjad.new(old_aggregate, ratio=[4, 5], pitch_segment__rotate=2)

    assert new_aggregate is not old_aggregate
    assert new_aggregate != old_aggregate
    assert abjad.storage(old_aggregate) == abjad.String.normalize(
        r"""
        test_new.Aggregate(
            pitch_segment=abjad.PitchSegment(
                (
                    abjad.NamedPitch('c'),
                    abjad.NamedPitch('d'),
                    abjad.NamedPitch('e'),
                    abjad.NamedPitch('f'),
                    ),
                item_class=abjad.NamedPitch,
                ),
            )
        """
    )
    assert abjad.storage(new_aggregate) == abjad.String.normalize(
        r"""
        test_new.Aggregate(
            pitch_segment=abjad.PitchSegment(
                (
                    abjad.NamedPitch('e'),
                    abjad.NamedPitch('f'),
                    abjad.NamedPitch('c'),
                    abjad.NamedPitch('d'),
                    ),
                item_class=abjad.NamedPitch,
                ),
            ratio=abjad.Ratio((4, 5)),
            )
        """
    )
