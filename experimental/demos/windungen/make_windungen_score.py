from abjad.tools import durationtools
from abjad.tools import pitchtools
from abjad.tools import sequencetools


def make_windungen_score(
    bandwidth=3,
    compress_reflections=True,
    leaf_duration=durationtools.Duration(1, 16),
    length=32,
    pitches=('c', 'd', 'e'),
    staff_count=12,
    ):

    from experimental.demos.windungen.WindungenScoreTemplate import WindungenScoreTemplate

    bandwidth = int(bandwidth)
    compress_reflections = bool(compress_reflections)
    leaf_duration = durationtools.Duration(leaf_duration)
    length = int(length)
    pitches = [pitchtools.NamedChromaticPitch(x) for x in pitches]
    staff_count = int(staff_count)

    assert 0 < bandwidth
    assert 0 < leaf_duration
    assert 0 < length
    assert 0 < len(pitches)
    assert 0 < staff_count

    score_template = WindungenScoreTemplate(staff_count=staff_count)
    score = score_template()

    all_pitches = sequencetools.repeat_sequence_to_length(length)

    matrix = make_cyclic_matrix_for_rotation_by_bandwidth()
