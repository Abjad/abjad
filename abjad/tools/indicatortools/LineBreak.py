from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from abjad.tools.datastructuretools.constants import *


class LineBreak(AbjadValueObject):
    r'''Line break.

    ..  container:: example

        Formats closing slot by default:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> break_ = abjad.LineBreak()
        >>> abjad.attach(break_, staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        >>> abjad.f(staff)
        \new Staff {
            c'4
            d'4
            e'4
            f'4
            \break
        }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_context',
        '_format_slot',
        )

    _time_orientation = Right

    ### INITIALIZER ##

    def __init__(self, format_slot='closing'):
        self._context = 'Score'
        assert isinstance(format_slot, str), repr(format_slot)
        self._format_slot = format_slot

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return r'\break'

    def _get_lilypond_format_bundle(self, component=None):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        slot = bundle.get(self.format_slot)
        slot.commands.append(self._get_lilypond_format())
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def context(self):
        r'''Gets line break default context.

        ..  container:: example

            Defaults to score:

            >>> break_ = abjad.LineBreak()
            >>> break_.context
            'Score'

        Returns context or string.
        '''
        return self._context

    @property
    def format_slot(self):
        r'''Gets format slot.

        ..  container:: example

            Defaults to closing:

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> break_ = abjad.LineBreak()
            >>> abjad.attach(break_, staff[-1])
            >>> abjad.show(staff) # doctest: +SKIP

            >>> abjad.f(staff)
            \new Staff {
                c'4
                d'4
                e'4
                f'4
                \break
            }

        ..  container:: example

            Formats before leaf like this:

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> break_ = abjad.LineBreak(format_slot='before')
            >>> abjad.attach(break_, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            >>> abjad.f(staff)
            \new Staff {
                \break
                c'4
                d'4
                e'4
                f'4
            }

        '''
        return self._format_slot
