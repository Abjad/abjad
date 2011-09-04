from abjad.tools.containertools.Container import Container
from abjad.tools.componenttools._Component import _Component
from abjad.tools import durationtools


def _yield_vertical_moments_forward_in_expr(expr):
    '''.. versionadded: 1.1.2

    Optimized to avoid full-score traversal.
    '''
    from abjad.tools.verticalitytools.VerticalMoment import VerticalMoment

    if not isinstance(expr, _Component):
        raise TypeError('must be Abjad component.')

    governors = (expr, )
    cur_offset, stop_offsets, buffer = durationtools.Offset(0), [], []
    _buffer_components_starting_with(expr, buffer, stop_offsets)

    while buffer:
        yield VerticalMoment(cur_offset, governors, tuple(buffer))
        cur_offset, stop_offsets = min(stop_offsets), []
        _update_buffer(cur_offset, buffer, stop_offsets)


def _buffer_components_starting_with(component, buffer, stop_offsets):
    if not isinstance(component, _Component):
        raise TypeError('must be Abjad component.')
    buffer.append(component)
    stop_offsets.append(component._offset.stop)
    if isinstance(component, Container):
        if component.is_parallel:
            for x in component.music:
                _buffer_components_starting_with(x, buffer, stop_offsets)
        else:
            if component:
                _buffer_components_starting_with(component[0], buffer, stop_offsets)


def _next_in_parent(component):
    from abjad.tools import componenttools
    if not isinstance(component, _Component):
        raise TypeError('must be component.')
    parent, start, stop = componenttools.get_parent_and_start_stop_indices_of_components([component])
    assert start == stop
    if parent is None:
        raise StopIteration
    # can not advance within parallel parent
    if parent.is_parallel:
        raise StopIteration
    try:
        return parent[start + 1]
    except IndexError:
        raise StopIteration


def _update_buffer(cur_offset, buffer, stop_offsets):
    #print ''
    #print 'At %s with %s ...' % (cur_offset, buffer)
    for component in buffer[:]:
        #print component, component._offset.stop
        if component._offset.stop <= cur_offset:
            #print 'removing %s ...' % component
            buffer.remove(component)
            #print buffer
            try:
                next_component = _next_in_parent(component)
                _buffer_components_starting_with(
                    next_component, buffer, stop_offsets)
            except StopIteration:
                pass
        else:
            stop_offsets.append(component._offset.stop)
    #print ''
