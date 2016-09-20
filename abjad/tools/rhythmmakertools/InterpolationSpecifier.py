# -*- coding: utf-8 -*-
from abjad.tools import durationtools
from abjad.tools.abctools import AbjadValueObject


class InterpolationSpecifier(AbjadValueObject):
    r'''Interpolation specifier.
    '''

    ### CLASS VARIABLES ###

    __documentation_section__ = 'Specifiers'

    __slots__ = (
        '_start_duration',
        '_stop_duration',
        '_written_duration',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        start_duration=durationtools.Duration(1, 8),
        stop_duration=durationtools.Duration(1, 16),
        written_duration=durationtools.Duration(1, 16),
        ):
        self._start_duration = durationtools.Duration(start_duration)
        self._stop_duration = durationtools.Duration(stop_duration)
        self._written_duration = durationtools.Duration(written_duration)

    ### PUBLIC METHODS ###

    def reverse(self):
        r'''Swaps start duration and stop duration of interpolation specifier.

        ..  container:: example

            **Example 1.** Changes accelerando specifier to ritardando
            specifier:

            ::

                >>> accelerando_specifier = rhythmmakertools.InterpolationSpecifier(
                ...     start_duration=Duration(1, 4),
                ...     stop_duration=Duration(1, 16),
                ...     written_duration=Duration(1, 16),
                ...     )
                >>> ritardando_specifier = accelerando_specifier.reverse()
                >>> print(format(ritardando_specifier))
                rhythmmakertools.InterpolationSpecifier(
                    start_duration=durationtools.Duration(1, 16),
                    stop_duration=durationtools.Duration(1, 4),
                    written_duration=durationtools.Duration(1, 16),
                    )

        ..  container:: example

            **Example 2.** Changes ritardando specifier to accelerando
            specifier:

            ::

                >>> accelerando_specifier = rhythmmakertools.InterpolationSpecifier(
                ...     start_duration=Duration(1, 16),
                ...     stop_duration=Duration(1, 4),
                ...     written_duration=Duration(1, 16),
                ...     )
                >>> ritardando_specifier = accelerando_specifier.reverse()
                >>> print(format(ritardando_specifier))
                rhythmmakertools.InterpolationSpecifier(
                    start_duration=durationtools.Duration(1, 4),
                    stop_duration=durationtools.Duration(1, 16),
                    written_duration=durationtools.Duration(1, 16),
                    )

        Copies written duration from source.
        '''
        return type(self)(
            start_duration=self.stop_duration,
            stop_duration=self.start_duration,
            written_duration=self.written_duration,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def start_duration(self):
        r'''Gets start duration.

        Defaults to ``1/8``.

        Set to positive duration.

        Returns position duration.
        '''
        return self._start_duration

    @property
    def stop_duration(self):
        r'''Gets stop duration.

        Defaults to ``1/16``.

        Set to positive duration.

        Returns position duration.
        '''
        return self._stop_duration

    @property
    def written_duration(self):
        r'''Gets written duration.

        Defaults to ``1/16``.

        Set to positive duration.

        Returns position duration.
        '''
        return self._written_duration
