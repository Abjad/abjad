# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class StemTremolo(AbjadValueObject):
    r'''A stem tremolo.

    ::

        >>> note = Note("c'4")
        >>> stem_tremolo = indicatortools.StemTremolo(16)
        >>> attach(stem_tremolo, note)
        >>> show(note) # doctest: +SKIP

    ..  doctest::

        >>> print(format(note))
        c'4 :16

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

        ::

            >>> print(format(stem_tremolo))
            :16

        Returns string.
        '''
        from abjad.tools import systemtools
        if format_specification in ('', 'lilypond'):
            return self._lilypond_format
        elif format_specification == 'storage':
            return systemtools.StorageFormatManager.get_storage_format(self)
        return str(self)

    def __str__(self):
        r'''String representation of stem tremolo.

        Returns string.
        '''
        return ':{!s}'.format(self.tremolo_flags)

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        lilypond_format_bundle.right.stem_tremolos.append(str(self))
        return lilypond_format_bundle

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        return str(self)

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            is_indented=False,
            )

    ### PUBLIC PROPERTIES ###

    @property
    def tremolo_flags(self):
        r'''Flags of stem tremolo.

        ::

            >>> stem_tremolo.tremolo_flags
            16

        Returns nonnegative integer power of ``2``.
        '''
        return self._tremolo_flags