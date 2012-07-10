from abjad.demos.mozart import helpers


def test_demos_mozart_01():

    piano_staff = helpers.build_mozart_piano_staff()

    assert len(piano_staff) == 2
    assert 0 < piano_staff.prolated_duration
    assert piano_staff[0].prolated_duration == piano_staff[1].prolated_duration

    lily_file = helpers.build_mozart_lily(piano_staff)

