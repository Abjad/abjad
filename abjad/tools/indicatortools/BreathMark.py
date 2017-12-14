from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from abjad.tools.datastructuretools.constants import *


class BreathMark(AbjadValueObject):
    r'''Breath mark.

    ..  container:: example

        Attached to a single note:

        >>> note = abjad.Note("c'4")
        >>> breath_mark = abjad.BreathMark()
        >>> abjad.attach(breath_mark, note)
        >>> abjad.show(note) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(note)
            c'4 \breathe

    ..  container:: example

        Attached to notes in a staff:

        >>> staff = abjad.Staff("c'8 d' e' f' g' a' b' c''")
        >>> abjad.attach(abjad.Beam(), staff[:4])
        >>> abjad.attach(abjad.Beam(), staff[4:])
        >>> abjad.attach(abjad.BreathMark(), staff[3])
        >>> abjad.attach(abjad.BreathMark(), staff[7])
        >>> abjad.show(staff) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(staff)
            \new Staff {
                c'8 [
                d'8
                e'8
                f'8 ]
                \breathe
                g'8 [
                a'8
                b'8
                c''8 ]
                \breathe
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = ()

    _format_slot = 'after'

    _time_orientation = Right

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''Gets string representation of breath mark.

        ..  container:: example

            >>> str(abjad.BreathMark())
            '\\breathe'

        Returns string.
        '''
        return r'\breathe'

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return str(self)

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return str(self)

    def _get_lilypond_format_bundle(self, component=None):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        bundle.after.commands.append(self._get_lilypond_format())
        return bundle
