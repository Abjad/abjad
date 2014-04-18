# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.abctools.AbjadObject import AbjadObject


class StemTremolo(AbjadObject):
    '''A stem tremolo.

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

    def __init__(self, *args):
        if len(args) == 1 and isinstance(args[0], type(self)):
            tremolo_flags = args[0].tremolo_flags
        elif len(args) == 1 and not isinstance(args[0], type(self)):
            tremolo_flags = args[0]
        elif len(args) == 0:
            tremolo_flags = 16
        else:
            message = 'can not initialize {}: {!r}.'
            message = message.format(type(self).__name__, args)
            raise ValueError(message)
        if not mathtools.is_nonnegative_integer_power_of_two(tremolo_flags):
            message = 'must be nonnegative integer power of 2: {!r}.'
            message = message.format(tremolo_flags)
            raise ValueError(message)
        self._tremolo_flags = tremolo_flags

    ### SPECIAL METHODS ###

    def __copy__(self, *args):
        r'''Copies stem tremolo.

        ::

            >>> import copy
            >>> stem_tremolo_1 = indicatortools.StemTremolo(16)
            >>> stem_tremolo_2 = copy.copy(stem_tremolo_1)

        ::

            >>> stem_tremolo_1 == stem_tremolo_2
            True

        ::

            >>> stem_tremolo_1 is not stem_tremolo_2
            True

        Returns new stem tremolo.
        '''
        return type(self)(self.tremolo_flags)

    def __eq__(self, expr):
        r'''Is true when `expr` is a stem tremolo with a tremolo flag count
        equal to that of this stem tremolo.  Otherwise false:

        ::

            >>> stem_tremolo_1 = indicatortools.StemTremolo(16)
            >>> stem_tremolo_2 = indicatortools.StemTremolo(16)
            >>> stem_tremolo_3 = indicatortools.StemTremolo(32)

        ::

            >>> stem_tremolo_1 == stem_tremolo_1
            True
            >>> stem_tremolo_1 == stem_tremolo_2
            True
            >>> stem_tremolo_1 == stem_tremolo_3
            False
            >>> stem_tremolo_2 == stem_tremolo_1
            True
            >>> stem_tremolo_2 == stem_tremolo_2
            True
            >>> stem_tremolo_2 == stem_tremolo_3
            False
            >>> stem_tremolo_3 == stem_tremolo_1
            False
            >>> stem_tremolo_3 == stem_tremolo_2
            False
            >>> stem_tremolo_3 == stem_tremolo_3
            True

        Returns boolean.
        '''
        if isinstance(expr, type(self)):
            if self.tremolo_flags == expr.tremolo_flags:
                return True
        return False

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

    def __hash__(self):
        r'''Hashes stem tremolo.

        Required to be explicitely re-defined on Python 3 if __eq__ changes.

        Returns integer.
        '''
        return super(StemTremolo, self).__hash__()

    def __str__(self):
        r'''String representation of stem tremolo.

        Returns string.
        '''
        return ':{!s}'.format(self.tremolo_flags)

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format(self):
        return str(self)

    @property
    def _lilypond_format_bundle(self):
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        lilypond_format_bundle.right.stem_tremolos.append(str(self))
        return lilypond_format_bundle

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        return systemtools.StorageFormatSpecification(
            self,
            is_indented=False,
            positional_argument_values=(
                self.tremolo_flags,
                ),
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
