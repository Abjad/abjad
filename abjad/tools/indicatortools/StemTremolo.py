# -*- coding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools import systemtools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class StemTremolo(AbjadValueObject):
    r'''Stem tremolo.

    ::

        >>> import abjad

    ..  container:: example

        Sixteenth-note tremolo:

        ::

            >>> note = abjad.Note("c'4")
            >>> stem_tremolo = abjad.StemTremolo(16)
            >>> abjad.attach(stem_tremolo, note)
            >>> show(note) # doctest: +SKIP

        ..  docs::

            >>> f(note)
            c'4 :16

    ..  container:: example

        Thirty-second-note tremolo:

        ::

            >>> note = abjad.Note("c'4")
            >>> stem_tremolo = abjad.StemTremolo(32)
            >>> abjad.attach(stem_tremolo, note)
            >>> show(note) # doctest: +SKIP

        ..  docs::

            >>> f(note)
            c'4 :32

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_tremolo_flags',
        )

    _format_slot = 'right'

    ### INITIALIZER ###

    def __init__(self, tremolo_flags=16):
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

            Sixteenth-note tremolo:

            ::

                >>> stem_tremolo = abjad.StemTremolo(16)
                >>> print(format(stem_tremolo))
                :16

        ..  container:: example

            Thirty-second-note tremolo:

            ::

                >>> stem_tremolo = abjad.StemTremolo(32)
                >>> print(format(stem_tremolo))
                :32

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'lilypond'):
            return self._get_lilypond_format()
        elif format_specification == 'storage':
            return systemtools.StorageFormatAgent(self).get_storage_format()
        return str(self)

    def __str__(self):
        r'''String representation of stem tremolo.

        ..  container:: example

            Sixteenth-note tremolo:

            ::

                >>> stem_tremolo = abjad.StemTremolo(16)
                >>> print(str(stem_tremolo))
                :16

        ..  container:: example

            Thirty-second-note tremolo:

            ::

                >>> stem_tremolo = abjad.StemTremolo(32)
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

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        bundle.right.stem_tremolos.append(self._get_lilypond_format())
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def tremolo_flags(self):
        r'''Gets tremolo flags of stem tremolo.

        ..  container:: example

            Sixteenth-note tremolo:

            ::

                >>> stem_tremolo = abjad.StemTremolo(16)
                >>> stem_tremolo.tremolo_flags
                16

        ..  container:: example

            Thirty-second-note tremolo:

            ::

                >>> stem_tremolo = abjad.StemTremolo(32)
                >>> stem_tremolo.tremolo_flags
                32

        Set to nonnegative integer power of 2.

        Defaults to 16.

        Returns nonnegative integer power of 2.
        '''
        return self._tremolo_flags
