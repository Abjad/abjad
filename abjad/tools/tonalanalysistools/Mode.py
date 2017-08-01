# -*- coding: utf-8 -*-
from abjad.tools import datastructuretools
from abjad.tools import pitchtools
from abjad.tools.abctools import AbjadValueObject


class Mode(AbjadValueObject):
    '''Mode.

    ::

        >>> from abjad.tools import tonalanalysistools

    ..  container:: example

        Initializes from string:

        ::

            >>> tonalanalysistools.Mode('major')
            Mode('major')

    ..  container:: example

        Initializes from other mode:

        ::

            >>> mode = tonalanalysistools.Mode('dorian')
            >>> tonalanalysistools.Mode(mode)
            Mode('dorian')

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_named_interval_segment',
        '_mode_name',
        )

    ### INITIALIZER ###

    def __init__(self, mode_name='dorian'):
        if isinstance(mode_name, str):
            mode_name = mode_name
        elif isinstance(mode_name, Mode):
            mode_name = mode_name.mode_name
        else:
            message = 'must be mode or mode name: {!r}.'
            message = message.format(mode_name)
            raise TypeError(message)
        mdi_segment = self._initialize_with_mode_name(mode_name)
        self._named_interval_segment = mdi_segment
        self._mode_name = mode_name

    ### SPECIAL METHODS ###

    def __eq__(self, argument):
        r'''Is true when `argument` is a mode with mode name equal to that of
        this mode. Otherwise false.

        ..  container:: example

            ::

                >>> mode_1 = tonalanalysistools.Mode('major')
                >>> mode_2 = tonalanalysistools.Mode('major')
                >>> mode_3 = tonalanalysistools.Mode('dorian')

            ::

                >>> mode_1 == mode_1
                True
                >>> mode_1 == mode_2
                True
                >>> mode_1 == mode_3
                False

            ::

                >>> mode_2 == mode_1
                True
                >>> mode_2 == mode_2
                True
                >>> mode_2 == mode_3
                False


            ::

                >>> mode_3 == mode_1
                False
                >>> mode_3 == mode_2
                False
                >>> mode_3 == mode_3
                True

        Returns true or false.
        '''
        return super(Mode, self).__eq__(argument)

    def __hash__(self):
        r'''Hashes mode.

        Required to be explicitly redefined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(Mode, self).__hash__()

    def __len__(self):
        r'''Length of mode.

        ..  container:: example

            ::

                >>> len(tonalanalysistools.Mode('dorian'))
                7

        Returns nonnegative integer.
        '''
        return len(self.named_interval_segment)

    def __str__(self):
        r'''String representation of mode.

        ..  container:: example

            ::

                >>> str(tonalanalysistools.Mode('dorian'))
                'dorian'

        Returns string.
        '''
        return self.mode_name

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        import abjad
        values = [self.mode_name]
        return abjad.FormatSpecification(
            client=self,
            repr_is_indented=False,
            storage_format_is_indented=False,
            storage_format_args_values=values,
            )

    def _initialize_with_mode_name(self, mode_name):
        mdi_segment = []
        m2 = pitchtools.NamedInterval('m2')
        M2 = pitchtools.NamedInterval('M2')
        A2 = pitchtools.NamedInterval('aug2')
        dorian = [M2, m2, M2, M2, M2, m2, M2]
        if mode_name == 'dorian':
            mdi_segment.extend(datastructuretools.Sequence(dorian).rotate(n=0))
        elif mode_name == 'phrygian':
            mdi_segment.extend(datastructuretools.Sequence(dorian).rotate(n=-1))
        elif mode_name == 'lydian':
            mdi_segment.extend(datastructuretools.Sequence(dorian).rotate(n=-2))
        elif mode_name == 'mixolydian':
            mdi_segment.extend(datastructuretools.Sequence(dorian).rotate(n=-3))
        elif mode_name in ('aeolian', 'minor', 'natural minor'):
            mdi_segment.extend(datastructuretools.Sequence(dorian).rotate(n=-4))
        elif mode_name == 'locrian':
            mdi_segment.extend(datastructuretools.Sequence(dorian).rotate(n=-5))
        elif mode_name in ('ionian', 'major'):
            mdi_segment.extend(datastructuretools.Sequence(dorian).rotate(n=-6))
        elif mode_name == 'melodic minor':
            mdi_segment.extend([M2, m2, M2, M2, M2, M2, m2])
        elif mode_name == 'harmonic minor':
            mdi_segment.extend([M2, m2, M2, M2, m2, A2, m2])
        else:
            message = 'unknown mode name: {!r}.'
            message = message.format(mode_name)
            raise ValueError(message)
        return pitchtools.IntervalSegment(
            items=mdi_segment,
            item_class=pitchtools.NamedInterval,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def mode_name(self):
        r'''Gets name.

        ..  container:: example

            ::

                >>> tonalanalysistools.Mode('major').mode_name
                'major'

            ::

                >>> tonalanalysistools.Mode('dorian').mode_name
                'dorian'

        Returns string.
        '''
        return self._mode_name

    @property
    def named_interval_segment(self):
        r'''Gets named interval segmen

        ..  container:: example

            ::

                >>> mode = tonalanalysistools.Mode('major')
                >>> str(mode.named_interval_segment)
                '<+M2, +M2, +m2, +M2, +M2, +M2, +m2>'

            ::

                >>> mode = tonalanalysistools.Mode('dorian')
                >>> str(mode.named_interval_segment)
                '<+M2, +m2, +M2, +M2, +M2, +m2, +M2>'

        Returns named interval segment.
        '''
        return self._named_interval_segment
