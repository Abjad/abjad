from abjad.tools import durationtools
from abjad.tools import sequencetools


# TODO: change signature to 
# _partition_components_by_durations(components, durations, ...)
def _partition_components_by_durations(
    duration_type,
    components,
    durations,
    fill='exact',
    cyclic=False,
    overhang=False,
    ):
    '''Partition `components` according to `durations`.

    Set `duration_type` to ``'prolated'`` or ``'seconds'``.

    When `fill` is ``'exact'`` then parts must equal `durations` exactly.

    When `fill` is ``'less'`` then parts must be 
    less than or equal to `durations`.

    When `fill` is ``'greater'`` then parts must be 
    greater or equal to `durations`.

    Read `durations` cyclically when `cyclic` is true.

    Return remaining components at end in final part when `overhang` is true.
    '''

    # coerce input
    durations = [durationtools.Duration(x) for x in durations]
    if cyclic:
        durations = sequencetools.CyclicTuple(durations)

    # initialize loop variables
    result = []
    part = []
    current_duration_index = 0
    target_duration = durations[current_duration_index]
    cumulative_duration = durationtools.Duration(0)

    # loop through components
    components_copy = list(components[:])
    while True:
        try:
            component = components_copy.pop(0)
        except IndexError:
            break
        if duration_type == 'seconds':
            component_duration = component.duration_in_seconds
        elif duration_type == 'prolated':
            component_duration = component.duration
        candidate_duration = cumulative_duration + component_duration
        if candidate_duration < target_duration:
            part.append(component)
            cumulative_duration = candidate_duration
        elif candidate_duration == target_duration:
            part.append(component)
            result.append(part)
            part = []
            cumulative_duration = durationtools.Duration(0)
            current_duration_index += 1
            try:
                target_duration = durations[current_duration_index]
            except IndexError:
                break
        elif target_duration < candidate_duration:
            if fill == 'exact':
                raise PartitionError
            elif fill == 'less':
                result.append(part)
                part = [component]
                if duration_type == 'seconds':
                    cumulative_duration = \
                        sum([x.duration_in_seconds for x in part])
                elif duration_type == 'prolated':
                    cumulative_duration = sum([x.duration for x in part])
                current_duration_index += 1
                try:
                    target_duration = durations[current_duration_index]
                except IndexError:
                    break
                if target_duration < cumulative_duration:
                    message = 'target duration {}'
                    message += ' is less than cumulative duration {}.'
                    message = message.format(
                        target_duration, cumulative_duration)
                    raise PartitionError(message)
            elif fill == 'greater':
                part.append(component)
                result.append(part)
                part = []
                cumulative_duration = durationtools.Duration(0)
                current_duration_index += 1
                try:
                    target_duration = durations[current_duration_index]
                except IndexError:
                    break
    if len(part):
        if overhang:
            result.append(part)
    if len(components_copy):
        if overhang:
            result.append(components_copy)
    return result
