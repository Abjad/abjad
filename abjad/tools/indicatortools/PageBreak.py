from abjad import Right
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from abjad.tools.systemtools.LilyPondFormatBundle import LilyPondFormatBundle


class PageBreak(AbjadValueObject):
    r'''
    Page break.

    ..  container:: example

        Formats in closing slot by default:

        >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
        >>> page_break = abjad.PageBreak()
        >>> abjad.attach(page_break, staff[-1])
        >>> abjad.show(staff) # doctest: +SKIP

        >>> page_break
        PageBreak(format_slot='closing')

        ..  docs::

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                d'4
                e'4
                f'4
                \pageBreak
            }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_format_slot',
        )

    _context = 'Score'

    _time_orientation = Right

    ### INITIALIZER ##

    def __init__(self, format_slot: str = 'closing') -> None:
        assert isinstance(format_slot, str), repr(format_slot)
        self._format_slot = format_slot

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        return r'\pageBreak'

    def _get_lilypond_format_bundle(self, component=None):
        bundle = LilyPondFormatBundle()
        slot = bundle.get(self.format_slot)
        slot.commands.append(self._get_lilypond_format())
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def context(self) -> str:
        '''
        Is ``'Score'``.

        ..  container:: example

            >>> abjad.PageBreak().context
            'Score'

        '''
        return self._context

    @property
    def format_slot(self) -> str:
        r'''
        Gets format slot.

        ..  container:: example

            Defaults to closing:

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> page_break = abjad.PageBreak()
            >>> abjad.attach(page_break, staff[-1])
            >>> abjad.show(staff) # doctest: +SKIP

            >>> page_break
            PageBreak(format_slot='closing')

            >>> abjad.f(staff)
            \new Staff
            {
                c'4
                d'4
                e'4
                f'4
                \pageBreak
            }

        ..  container:: example

            Formats before leaf like this:

            >>> staff = abjad.Staff("c'4 d'4 e'4 f'4")
            >>> page_break = abjad.PageBreak(format_slot='before')
            >>> abjad.attach(page_break, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            >>> abjad.f(staff)
            \new Staff
            {
                \pageBreak
                c'4
                d'4
                e'4
                f'4
            }

        '''
        return self._format_slot
