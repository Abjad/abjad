from abjad.exceptions import PartitionError
from abjad.tools import durationtools


def _partition_components_by_durations(duration_type, components, durations,
    fill = 'exact', cyclic = False, overhang = False):
    '''Partition `components` according to `durations`.

    Set `duration_type` to ``'prolated'`` or ``'seconds'``.

    When `fill` is ``'exact'`` then parts must equal `durations` exactly.

    When `fill` is ``'less'`` then parts must be less than or equal to `durations`.

    When `fill` is ``'greater'`` then parts must be greater or equal to `durations`.

    Read `durations` cyclically when `cyclic` is true.

    Return remaining components at end in final part when `overhang` is true.
    '''

    #assert isinstance(durations, list)
    #assert all([isinstance(x, (int, float, durationtools.Duration)) for x in durations])
    _durations = [  ]
    for duration in durations:
        if isinstance(duration, (int, float, durationtools.Duration)):
            _durations.append(duration)
        else:
            try:
                _durations.append(durationtools.Duration(duration))
            except TypeError:
                raise AssertionError
    durations = _durations
    assert all([isinstance(x, (int, float, durationtools.Duration)) for x in durations])

    len_durations = len(durations)
    result = []
    part = []
    cur_duration_idx = 0
    target_duration = durations[cur_duration_idx]
    cum_duration = durationtools.Duration(0)

    components_copy = list(components[:])
    while True:
        #print part
        try:
            component = components_copy.pop(0)
        except IndexError:
            break
        # collapse these 4 lines to only the 4th line after duration migration
        if duration_type == 'seconds':
            component_duration = component.duration_in_seconds
        elif duration_type == 'prolated':
            component_duration = component.prolated_duration
        elif duration_type == 'preprolated':
            component_duration = component.preprolated_duration
        else:
            #print 'debug %s' % duration_type
            component_duration = getattr(component.duration, duration_type)
        candidate_duration = cum_duration + component_duration
        if candidate_duration < target_duration:
            #print 'not there yet'
            part.append(component)
            cum_duration = candidate_duration
        elif candidate_duration == target_duration:
            part.append(component)
            result.append(part)
            part = []
            cum_duration = durationtools.Duration(0)
            cur_duration_idx += 1
            target_duration = _get_next(durations, cur_duration_idx, cyclic)
        elif target_duration < candidate_duration:
            #print 'greater!'
            if fill == 'exact':
                raise PartitionError
            elif fill == 'less':
                result.append(part)
                part = [component]
                # collapse to 4th line after duration migration
                if duration_type == 'seconds':
                    cum_duration = sum([x.duration_in_seconds for x in part])
                elif duration_type == 'preprolated':
                    cum_duration = sum([x.preprolated_duration for x in part])
                elif duration_type == 'prolated':
                    cum_duration = sum([x.prolated_duration for x in part])
                else:
                    cum_duration = sum([getattr(x.duration, duration_type) for x in part])
                cur_duration_idx += 1
                target_duration = _get_next(durations, cur_duration_idx, cyclic)
                if target_duration is None:
                    break
                if target_duration < cum_duration:
                    raise PartitionError('target duration "%s" is less than cumulative duration "%s"' %
                        (target_duration, cum_duration))
            elif fill == 'greater':
                part.append(component)
                result.append(part)
                part = []
                cum_duration = durationtools.Duration(0)
                cur_duration_idx += 1
                target_duration = _get_next(durations, cur_duration_idx, cyclic)
        if target_duration is None:
            break

    if len(part):
        if overhang:
            result.append(part)

    if len(components_copy):
        if overhang:
            result.append(components_copy)

    return result


def _get_next(durations, cur_duration_idx, cyclic):
    try:
        if cyclic:
            return durations[cur_duration_idx % len(durations)]
        else:
            return durations[cur_duration_idx]
    except IndexError:
        return None
