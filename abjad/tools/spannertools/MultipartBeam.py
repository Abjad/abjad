# -*- encoding: utf-8 -*-
from abjad.tools.spannertools.Beam import Beam


class MultipartBeam(Beam):
    r'''A multipart beam spanner.

    ::

        >>> staff = Staff("c'8 d'8 e'4 f'8 g'8 r4")
        >>> show(staff) # doctest: +SKIP

    ::

        >>> beam = spannertools.MultipartBeam()
        >>> attach(beam, staff[:])
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            c'8 [
            d'8 ]
            e'4
            f'8 [
            g'8 ]
            r4
        }

    Avoids rests.

    Avoids large-duration notes.
    '''

    ### INITIALIZER ###

    def __init__(
        self, 
        components=None, 
        direction=None,
        overrides=None,
        ):
        Beam.__init__(
            self, 
            components, 
            direction=direction,
            overrides=overrides,
            )

    ### PRIVATE METHODS ###

    def _format_right_of_leaf(self, leaf):
        from abjad.tools import scoretools
        result = []
        direction_string = ''
        if self.direction is not None:
            direction_string = '%s ' % self.direction
        if self.is_beamable_component(leaf):
            if 1 < len(self.leaves):
                previous = leaf._get_leaf(-1)
                if id(previous) not in [id(x) for x in self.leaves]:
                    previous = None
                next = leaf._get_leaf(1)
                if id(next) not in [id(x) for x in self.leaves]:
                    next = None
                if self._is_my_first_leaf(leaf):
                    if next is not None:
                        if self.is_beamable_component(next):
                            result.append('%s[' % direction_string)
                else:
                    if previous is not None:
                        if not self.is_beamable_component(previous):
                            if next is not None:
                                result.append('%s[' % direction_string)
                if self._is_my_last_leaf(leaf):
                    if previous is not None:
                        if self.is_beamable_component(previous):
                            result.append(']')
                else:
                    next = leaf._get_leaf(1)
                    if next is not None and \
                        not self.is_beamable_component(next):
                        result.append(']')
        return result
