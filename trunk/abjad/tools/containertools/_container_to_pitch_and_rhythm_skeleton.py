from abjad.tools import componenttools


def _container_to_pitch_and_rhythm_skeleton(container, include_keyword_attributes=False):
    from abjad.tools import contexttools
    from abjad.tools import measuretools
    from abjad.tools import tuplettools
    from abjad.tools.leaftools._get_leaf_keyword_attributes import \
        _get_leaf_keyword_attributes

    class_name = container.__class__.__name__
    contents = []
    for x in container:
        if include_keyword_attributes:
            skeleton = \
                componenttools.component_to_pitch_and_rhythm_skeleton_with_interface_attributes(x)
        else:
            skeleton = componenttools.component_to_pitch_and_rhythm_skeleton(x)
        skeleton = skeleton.split('\n')
        skeleton = ['\t' + line for line in skeleton]
        skeleton = '\n'.join(skeleton)
        contents.append(skeleton)
    contents = ',\n'.join(contents)
    if include_keyword_attributes:
        keyword_attributes = _get_leaf_keyword_attributes(container)
    else:
        keyword_attributes = []
    if keyword_attributes:
        keyword_attributes = ',\n'.join(keyword_attributes)
        keyword_attributes = '\n' + keyword_attributes
    if isinstance(container, measuretools.Measure):
        meter = contexttools.get_effective_time_signature(container)
        meter_pair = (meter.numerator, meter.denominator)
        return '%s(%s, [\n%s\n])' % (class_name, str(meter_pair), contents)
    elif isinstance(container, tuplettools.FixedDurationTuplet):
        duration = repr(container.target_duration)
        if keyword_attributes:
            return '%s(%s, [\n%s\n], %s)' % (class_name, duration, contents, keyword_attributes)
        else:
            return '%s(%s, [\n%s\n])' % (class_name, duration, contents)
    elif isinstance(container, tuplettools.Tuplet):
        multiplier = repr(container.multiplier)
        if keyword_attributes:
            return '%s(%s, [\n%s\n], %s)' % (class_name, multiplier, contents, keyword_attributes)
        else:
            return '%s(%s, [\n%s\n])' % (class_name, multiplier, contents)
    else:
        if keyword_attributes:
            return '%s([\n%s\n], %s)' % (class_name, contents, keyword_attributes)
        else:
            return '%s([\n%s\n])' % (class_name, contents)
