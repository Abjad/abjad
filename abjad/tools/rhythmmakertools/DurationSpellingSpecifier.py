# -*- encoding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools.abctools import AbjadObject


class DurationSpellingSpecifier(AbjadObject):
    r'''Duration spelling speficifier.
    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_decrease_durations_monotonically',
        '_forbidden_written_duration',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        decrease_durations_monotonically=True,
        forbidden_written_duration=None,
        ):
        assert isinstance(decrease_durations_monotonically, bool)
        if forbidden_written_duration is not None:
            forbidden_written_duration = durationtools.Duration(
                forbidden_written_duration)
        self._decrease_durations_monotonically = decrease_durations_monotonically 
        self._forbidden_written_duration = forbidden_written_duration

    ### SPECIAL METHODS ###

    def __eq__(self, arg):
        r'''Is true when `arg` is a duration spelling specifier with
        values of `decrease_durations_monotonically` and `forbidden_written_duration`
        equal to those of this duration spelling specifier. Otherwise false.

        ..  container:: example

            ::

                >>> specifier_1 = rhythmmakertools.DurationSpellingSpecifier(
                ...     decrease_durations_monotonically=True,
                ...     )
                >>> specifier_2 = rhythmmakertools.DurationSpellingSpecifier(
                ...     decrease_durations_monotonically=False,
                ...     )

            ::

                >>> specifier_1 == specifier_1
                True
                >>> specifier_1 == specifier_2
                False
                >>> specifier_2 == specifier_1
                False
                >>> specifier_2 == specifier_2
                True

        Returns boolean.
        '''
        if isinstance(arg, type(self)):
            if self.decrease_durations_monotonically == arg.decrease_durations_monotonically and \
                self.forbidden_written_duration == \
                arg.forbidden_written_duration:
                return True
        return False

    def __format__(self, format_specification=''):
        r'''Formats duration spelling specifier.

        ..  container:: example

            ::

                >>> specifier = rhythmmakertools.DurationSpellingSpecifier()
                >>> print format(specifier)
                rhythmmakertools.DurationSpellingSpecifier(
                    decrease_durations_monotonically=True,
                    )

        Returns string.
        '''
        return AbjadObject.__format__(
            self,
            format_specification=format_specification,
            )

    def __makenew__(self, *args, **kwargs):
        r'''Makes new duration spelling specifier with optional `kwargs`.

        Returns new duration spelling specifier.
        '''
        from abjad.tools import systemtools
        assert not args
        arguments = {}
        manager = systemtools.StorageFormatManager
        argument_names = manager.get_keyword_argument_names(self)
        for argument_name in argument_names:
            arguments[argument_name] = getattr(self, argument_name)
        arguments.update(kwargs)
        return type(self)(**arguments)

    def __repr__(self):
        r'''Gets interpreter representation of duration spelling specifier.

        ..  container:: example

            ::

                >>> rhythmmakertools.DurationSpellingSpecifier()
                DurationSpellingSpecifier(decrease_durations_monotonically=True)

        Returns string.
        '''
        return AbjadObject.__repr__(self)

    ### PUBLIC PROPERTIES ###

    @property
    def decrease_durations_monotonically(self):
        r'''Is true when all durations should be spelled as a tied series of
        monotonically decreasing values. Otherwise false.

        ..  container:: example

            ::

                >>> specifier = rhythmmakertools.DurationSpellingSpecifier()
                >>> specifier.decrease_durations_monotonically
                True

        Defaults to true.

        Returns boolean.
        '''
        return self._decrease_durations_monotonically

    @property
    def forbidden_written_duration(self):
        r'''Gets forbidden written duration.

        ..  container:: example

            ::

                >>> specifier = rhythmmakertools.DurationSpellingSpecifier()
                >>> specifier.forbidden_written_duration is None
                True

        Defaults to none.

        Returns duration or none.
        '''
        return self._forbidden_written_duration

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Reverses duration spelling specifier.

        ..  container:: example

            ::

                >>> specifier = rhythmmakertools.DurationSpellingSpecifier()
                >>> print format(specifier)
                rhythmmakertools.DurationSpellingSpecifier(
                    decrease_durations_monotonically=True,
                    )

            ::

                >>> reversed_specifier = specifier.reverse()
                >>> print format(reversed_specifier)
                rhythmmakertools.DurationSpellingSpecifier(
                    decrease_durations_monotonically=False,
                    )

        Negates `decrecase_monotonically`.

        Returns new duration spelling specifier.
        '''
        decrease_durations_monotonically = not self.decrease_durations_monotonically
        arguments = {
            'decrease_durations_monotonically': decrease_durations_monotonically,
            'forbidden_written_duration': self.forbidden_written_duration,
            }
        result = type(self)(**arguments)
        return result
