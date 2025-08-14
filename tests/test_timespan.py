import abjad


def test_timespan_annotation():
    """
    Annotated timespans maintain their annotations after mutation.

    TODO: is this possibly exactly the wrong behavior?
    """

    timespan = abjad.Timespan(
        abjad.duration.offset(1, 4),
        abjad.duration.offset(7, 8),
        annotation=["a", "b", "c", "foo"],
    )
    left_timespan, right_timespan = timespan.split_at_offset(
        abjad.duration.offset(1, 2)
    )
    left_timespan.annotation.append("foo")

    assert timespan.annotation == ["a", "b", "c", "foo", "foo"]
    assert left_timespan.annotation == ["a", "b", "c", "foo", "foo"]
    assert right_timespan.annotation == ["a", "b", "c", "foo", "foo"]
