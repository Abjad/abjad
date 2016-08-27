# -*- coding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools import systemtools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class StemTremolo(AbjadValueObject):
    r'''Stem tremolo.

    ..  container:: example

        **Example 1.** Sixteenth-note tremolo:

        ::

            >>> note = Note("c'4")
            >>> stem_tremolo = indicatortools.StemTremolo(16)
            >>> attach(stem_tremolo, note)
            >>> show(note) # doctest: +SKIP

        ..  doctest::

            >>> print(format(note))
            c'4 :16

    ..  container:: example

        **Example 2.** Thirty-second-note tremolo:

        ::

            >>> note = Note("c'4")
            >>> stem_tremolo = indicatortools.StemTremolo(32)
            >>> attach(stem_tremolo, note)
            >>> show(note) # doctest: +SKIP

        ..  doctest::

            >>> print(format(note))
            c'4 :32

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_default_scope',
        '_tremolo_flags',
        )

    _format_slot = 'right'

    ### INITIALIZER ###

    def __init__(self, tremolo_flags=16):
        self._default_scope = None
        if isinstance(tremolo_flags, type(self)):
            tremolo_flags = tremolo_flags.tremolo_flags
        tremolo_flags = int(tremolo_flags)
        if not mathtools.is_nonnegative_integer_power_of_two(tremolo_flags):
            message = 'must be nonnegative integer power of 2: {!r}.'
            message = message.format(tremolo_flags)
            raise ValueError(message)
        self._tremolo_flags = tremolo_flags

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        r'''Formats stem tremolo.

        ..  container:: example

            **Example 1.** Sixteenth-note tremolo:

            ::

                >>> stem_tremolo = indicatortools.StemTremolo(16)
                >>> print(format(stem_tremolo))
                :16

        ..  container:: example

            **Example 2.** Thirty-second-note tremolo:

            ::

                >>> stem_tremolo = indicatortools.StemTremolo(32)
                >>> print(format(stem_tremolo))
                :32

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        elif format_specification == 'storage':
            return systemtools.StorageFormatAgent(self).get_storage_format()
        return str(self)

    def __str__(self):
        r'''String representation of stem tremolo.

        ..  container:: example

            **Example 1.** Sixteenth-note tremolo:

            ::

                >>> stem_tremolo = indicatortools.StemTremolo(16)
                >>> print(str(stem_tremolo))
                :16

        ..  container:: example

            **Example 2.** Thirty-second-note tremolo:

            ::

                >>> stem_tremolo = indicatortools.StemTremolo(32)
                >>> print(str(stem_tremolo))
                :32

        Returns string.
        '''
        return ':{!s}'.format(self.tremolo_flags)

    ### PRIVATE METHODS ###

    def _get_format_specification(self):
        return systemtools.FormatSpecification(
            client=self,
            storage_format_is_indented=False,
            )

    def _get_lilypond_format_bundle(self, component=None):
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        lilypond_format_bundle.right.stem_tremolos.append(str(self))
        return lilypond_format_bundle

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        return str(self)

    ### PUBLIC PROPERTIES ###

    @property
    def default_scope(self):
        r'''Gets default scope of stem tremolo.

        ..  container:: example

            **Example 1.** Sixteenth-note tremolo:

            ::

                >>> stem_tremolo = indicatortools.StemTremolo(16)
                >>> stem_tremolo.default_scope is None
                True

        ..  container:: example

            **Example 2.** Thirty-second-note tremolo:

            ::

                >>> stem_tremolo = indicatortools.StemTremolo(32)
                >>> stem_tremolo.default_scope is None
                True

        Returns none.
        '''
        return self._default_scope

    @property
    def tremolo_flags(self):
        r'''Gets tremolo flags of stem tremolo.

        ..  container:: example

            **Example 1.** Sixteenth-note tremolo:

            ::

                >>> stem_tremolo = indicatortools.StemTremolo(16)
                >>> stem_tremolo.tremolo_flags
                16

        ..  container:: example

            **Example 2.** Thirty-second-note tremolo:

            ::

                >>> stem_tremolo = indicatortools.StemTremolo(32)
                >>> stem_tremolo.tremolo_flags
                32

        Set to nonnegative integer power of 2.

        Defaults to 16.

        Returns nonnegative integer power of 2.
        '''
        return self._tremolo_flags
