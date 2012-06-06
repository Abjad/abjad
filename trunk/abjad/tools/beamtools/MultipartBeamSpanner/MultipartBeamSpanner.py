from abjad.tools.beamtools.BeamSpanner import BeamSpanner


class MultipartBeamSpanner(BeamSpanner):
    r'''.. versionadded:: 2.0

    Abjad multipart beam spanner::

        >>> staff = Staff("c'8 d'8 e'4 f'8 g'8 r4")

    ::

        >>> beamtools.MultipartBeamSpanner(staff[:])
        MultipartBeamSpanner(c'8, d'8, e'4, f'8, g'8, r4)

    ::

        >>> f(staff)
        \new Staff {
            c'8 [
            d'8 ]
            e'4
            f'8 [
            g'8 ]
            r4
        }

    Avoid rests.

    Avoid large-duration notes.

    Return multipart beam spanner.
    '''

    ### INITIALIZER ###

    def __init__(self, components=None, direction=None):
        BeamSpanner.__init__(self, components, direction=direction)

    ### PRIVATE METHODS ###

    def _format_right_of_leaf(self, leaf):
        from abjad.tools import beamtools
        from abjad.tools import leaftools
        result = []
        direction_string = ''
        if self.direction is not None:
            direction_string = '%s ' % self.direction
        if beamtools.is_beamable_component(leaf):
            if 1 < len(self.leaves):
                prev = leaftools.get_nth_leaf_in_thread_from_leaf(leaf, -1)
                if id(prev) not in [id(x) for x in self.leaves]:
                    prev = None
                next = leaftools.get_nth_leaf_in_thread_from_leaf(leaf, 1)
                if id(next) not in [id(x) for x in self.leaves]:
                    next = None
                if self._is_my_first_leaf(leaf):
                    if next is not None:
                        if beamtools.is_beamable_component(next):
                            result.append('%s[' % direction_string)
                else:
                    if prev is not None:
                        if not beamtools.is_beamable_component(prev):
                            if next is not None:
                                result.append('%s[' % direction_string)
                if self._is_my_last_leaf(leaf):
                    if prev is not None:
                        if beamtools.is_beamable_component(prev):
                            result.append(']')
                else:
                    next = leaftools.get_nth_leaf_in_thread_from_leaf(leaf, 1)
                    if next is not None and not beamtools.is_beamable_component(next):
                        result.append(']')
        return result
