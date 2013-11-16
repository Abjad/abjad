# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools.spannertools.Beam import Beam


class ComplexBeam(Beam):
    r'''A complex beam spanner.

    ::

        >>> staff = Staff("c'16 e'16 r16 f'16 g'2")
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            c'16
            e'16
            r16
            f'16
            g'2
        }

    ::

        >>> beam = spannertools.ComplexBeam()
        >>> attach(beam, staff[:4])
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            \set stemLeftBeamCount = #0
            \set stemRightBeamCount = #2
            c'16 [
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #2
            e'16 ]
            r16
            \set stemLeftBeamCount = #2
            \set stemRightBeamCount = #0
            f'16 [ ]
            g'2
        }

    '''

    ### INITIALIZER ###

    def __init__(
        self, 
        components=None, 
        lone=False, 
        direction=None,
        overrides=None,
        ):
        Beam.__init__(
            self, 
            components=components, 
            direction=direction,
            overrides=overrides,
            )
        self.lone = lone

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        Beam._copy_keyword_args(self, new)
        new.lone = self.lone

    def _format_before_leaf(self, leaf):
        r'''Spanner format contribution to output before leaf.
        '''
        result = []
        result.extend(Beam._format_before_leaf(self, leaf))
        if self.is_beamable_component(leaf):
            if self._is_my_only_leaf(leaf):
                left, right = self._get_left_right_for_lone_leaf(leaf)
            elif self._is_exterior_leaf(leaf):
                left, right = self._get_left_right_for_exterior_leaf(leaf)
            else:
                left, right = self._get_left_right_for_interior_leaf(leaf)
            if left is not None:
                result.append(r'\set stemLeftBeamCount = #%s' % left)
            if right is not None:
                result.append(r'\set stemRightBeamCount = #%s' % right)
        return result

    def _format_right_of_leaf(self, leaf):
        r'''Spanner format contribution to output right of leaf.
        '''
        from abjad.tools import scoretools
        result = []
        #if leaf.beam.beamable:
        if self.is_beamable_component(leaf):
            previous_leaf = leaf._get_leaf(-1)
            next_leaf = leaf._get_leaf(1)
            # lone
            if self._is_my_only_leaf(leaf):
                if self.lone:
                    if self.direction is not None:
                        result.append('%s [' % self.direction)
                    else:
                        result.append('[')
            # otherwise
            elif self._is_my_first_leaf(leaf) or not previous_leaf or \
                not self.is_beamable_component(previous_leaf):
                if self.direction is not None:
                    result.append('%s [' % self.direction)
                else:
                    result.append('[')
            # lone
            if self._is_my_only_leaf(leaf):
                if self.lone:
                    result.append(']')
            # otherwise
            elif self._is_my_last_leaf(leaf) or not next_leaf or \
                not self.is_beamable_component(next_leaf):
                result.append(']')
        return result

    def _get_left_right_for_exterior_leaf(self, leaf):
        r'''Get left and right flag counts for exterior leaf in spanner.
        '''
        from abjad.tools import scoretools
        # lone
        if self._is_my_only_leaf(leaf):
            left, right = self._get_left_right_for_lone_leaf(leaf)
        # first
        elif self._is_my_first_leaf(leaf) or not leaf._get_leaf(-1):
            left = 0
            right = leaf.written_duration.flag_count
        # last
        elif self._is_my_last_leaf(leaf) or leaf._get_leaf(1):
            left = leaf.written_duration.flag_count
            right = 0
        else:
            raise ValueError('leaf must be first or last in spanner.')
        return left, right

    def _get_left_right_for_interior_leaf(self, leaf):
        r'''Interior leaves are neither first nor last in spanner.
        Interior leaves may be surrounded by beamable leaves.
        Interior leaves may be surrounded by unbeamable leaves.
        Four cases total for beamability of surrounding leaves.
        '''
        from abjad.tools import scoretools
        previous_leaf = leaf._get_leaf(-1)
        previous_written = previous_leaf.written_duration
        current_written = leaf.written_duration
        next_leaf = leaf._get_leaf(1)
        next_written = next_leaf.written_duration
        previous_flag_count = previous_written.flag_count
        current_flag_count = current_written.flag_count
        next_flag_count = next_written.flag_count
        # [unbeamable leaf beamable]
        if not self.is_beamable_component(previous_leaf) and \
            self.is_beamable_component(next_leaf):
            left = current_flag_count
            right = min(current_flag_count, next_flag_count)
        # [beamable leaf unbeamable]
        if self.is_beamable_component(previous_leaf) and \
            not self.is_beamable_component(next_leaf):
            left = min(current_flag_count, previous_flag_count)
            right = current_flag_count
        # [unbeamable leaf unbeamable]
        elif not self.is_beamable_component(previous_leaf) and \
            not self.is_beamable_component(next_leaf):
            left = current_flag_count
            right = current_flag_count
        # [beamable leaf beamable]
        else:
            left = min(current_flag_count, previous_flag_count)
            right = min(current_flag_count, next_flag_count)
            if left != current_flag_count and right != current_flag_count:
                left = current_flag_count
        return left, right

    def _get_left_right_for_lone_leaf(self, leaf):
        r'''Get left and right flag counts for only leaf in spanner.
        '''
        current_flag_count = leaf.written_duration.flag_count
        left, right = None, None
        if self.lone == 'left':
            left = current_flag_count
            right = 0
        elif self.lone == 'right':
            left = 0
            right = current_flag_count
        elif self.lone in ('both', True):
            left = current_flag_count
            right = current_flag_count
        elif self.lone in ('neither', False):
            left = None
            right = None
        else:
            raise ValueError("'lone' must be left, right, both.")
        return left, right

    ### PUBLIC PROPERTIES ###

    @apply
    def lone():
        def fget(self):
            r'''Beam lone leaf and force beam nibs to left:

            ::

                >>> note = Note("c'16")

            ::

                >>> beam = spannertools.ComplexBeam(lone='left')
                >>> attach(beam, note)
                >>> show(note) # doctest: +SKIP

            ..  doctest::

                >>> print format(note)
                \set stemLeftBeamCount = #2
                \set stemRightBeamCount = #0
                c'16 [ ]

            Beam lone leaf and force beam nibs to right:

            ::

                >>> note = Note("c'16")

            ::

                >>> beam = spannertools.ComplexBeam(lone='right')
                >>> attach(beam, note)

            ..  doctest::

                >>> print format(note)
                \set stemLeftBeamCount = #0
                \set stemRightBeamCount = #2
                c'16 [ ]

            Beam lone leaf and force beam nibs to both left and right:

            ::

                >>> note = Note("c'16")

            ::

                >>> beam = spannertools.ComplexBeam(lone='both')
                >>> attach(beam, note)

            ..  doctest::

                >>> print format(note)
                \set stemLeftBeamCount = #2
                \set stemRightBeamCount = #2
                c'16 [ ]

            Beam lone leaf and accept LilyPond default nibs at 
            both left and right:

            ::

                >>> note = Note("c'16")

            ::

                >>> beam = spannertools.ComplexBeam(lone=True)
                >>> attach(beam, note)

            ..  doctest::

                >>> print format(note)
                \set stemLeftBeamCount = #2
                \set stemRightBeamCount = #2
                c'16 [ ]

            Do not beam lone leaf:

            ::

                >>> note = Note("c'16")

            ::

                >>> beam = spannertools.ComplexBeam(lone=False)
                >>> attach(beam, note)

            ..  doctest::

                >>> print format(note)
                c'16

            Set to ``'left'``, ``'right'``, ``'both'``, true or false 
            as shown above.

            Ignore this setting when spanner contains more than one leaf.
            '''
            return self._lone
        def fset(self, arg):
            assert isinstance(arg, bool) or arg in ('left', 'right', 'both')
            self._lone = arg
        return property(**locals())
