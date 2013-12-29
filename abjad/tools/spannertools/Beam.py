# -*- encoding: utf-8 -*-
from abjad.tools import stringtools
from abjad.tools.spannertools.Spanner import Spanner


class Beam(Spanner):
    r'''A beam.

    ::

        >>> staff = Staff("c'8 d'8 e'8 f'8 g'2")
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            c'8
            d'8
            e'8
            f'8
            g'2
        }

    ::

        >>> beam = spannertools.Beam()
        >>> attach(beam, staff[:4])
        >>> show(staff) # doctest: +SKIP

    ..  doctest::

        >>> print format(staff)
        \new Staff {
            c'8 [
            d'8
            e'8
            f'8 ]
            g'2
        }

    '''

    ### INITIALIZER ###

    def __init__(self, direction=None, overrides=None):
        Spanner.__init__(self, overrides=overrides)
        self.direction = direction

    ### PRIVATE METHODS ###

    def _copy_keyword_args(self, new):
        #Spanner._copy_keyword_args(self, new)
        new.direction = self.direction

    def _format_right_of_leaf(self, leaf):
        result = []
        if self._is_my_first_leaf(leaf):
            if self.direction is not None:
                result.append('%s [' % self.direction)
            else:
                result.append('[')
        if self._is_my_last_leaf(leaf):
            result.append(']')
        return result

    ### PUBLIC METHODS ###

    @staticmethod
    def is_beamable_component(expr):
        '''True when `expr` is a beamable component. Otherwise false.

        ::

            >>> staff = Staff(r"r32 a'32 ( [ gs'32 fs''32 \staccato f''8 ) ]")
            >>> staff.extend(r"r8 e''8 ( ef'2 )")
            >>> show(staff) # doctest: +SKIP

        ::

            >>> for leaf in staff.select_leaves():
            ...     beam = spannertools.Beam
            ...     result = beam.is_beamable_component(leaf)
            ...     print '{:<8}\t{}'.format(leaf, result)
            ...
            r32     False
            a'32    True
            gs'32   True
            fs''32  True
            f''8    True
            r8      False
            e''8    True
            ef'2    False

        Returns boolean.
        '''
        from abjad.tools import scoretools
        from abjad.tools import scoretools
        if isinstance(expr, (scoretools.Note, scoretools.Chord)):
            if 0 < expr.written_duration.flag_count:
                return True
        return False

    ### PUBLIC PROPERTIES ###

    @property
    def direction(self):
        r'''Gets and sets direction of beam.

        Returns up or down.
        '''
        return self._direction

    @direction.setter
    def direction(self, arg):
        self._direction = \
            stringtools.arg_to_tridirectional_lilypond_symbol(arg)
