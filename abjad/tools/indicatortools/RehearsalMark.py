import typing
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject
from abjad.tools.markuptools.Markup import Markup


class RehearsalMark(AbjadValueObject):
    r'''Rehearsal mark.

    ..  container:: example

        >>> staff = abjad.Staff("c'4 d' e' f'")
        >>> score = abjad.Score([staff])
        >>> mark = abjad.RehearsalMark(number=1)
        >>> abjad.attach(mark, staff[0])
        >>> scheme = abjad.Scheme('format-mark-box-alphabet')
        >>> abjad.setting(score).markFormatter = scheme
        >>> abjad.show(score) # doctest: +SKIP

        ..  docs::

            >>> abjad.f(score)
            \new Score
            \with
            {
                markFormatter = #format-mark-box-alphabet
            }
            <<
                \new Staff
                {
                    \mark #1
                    c'4
                    d'4
                    e'4
                    f'4
                }
            >>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_markup',
        '_number',
        )

    _context = 'Score'

    ### INITIALIZER ###

    def __init__(
        self,
        number: int = None,
        markup: Markup = None,
        ) -> None:
        self._markup: Markup = markup
        self._number: int = number

    ### SPECIAL METHODS ###

    def __str__(self) -> str:
        r'''Gets string representation of rehearsal mark.

        ..  container:: example

            >>> mark = abjad.RehearsalMark(number=1)
            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(mark, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::
            
                >>> abjad.f(staff)
                \new Staff
                {
                    \mark #1
                    c'4
                    d'4
                    e'4
                    f'4
                }

        '''
        return self._get_lilypond_format()

    ### PRIVATE PROPERTIES ###

    @property
    def _contents_repr_string(self):
        return str(self)

    ### PRIVATE METHODS ###

    def _get_lilypond_format(self):
        if self.markup is not None:
            result = r'\mark {}'.format(self.markup)
        elif self.number is not None:
            result = r'\mark #{}'.format(self.number)
        else:
            result = r'\mark \default'
        return result

    def _get_lilypond_format_bundle(self, component=None):
        import abjad
        bundle = abjad.LilyPondFormatBundle()
        bundle.opening.commands.append(self._get_lilypond_format())
        return bundle

    ### PUBLIC PROPERTIES ###

    @property
    def context(self) -> str:
        r'''Returns ``'Score'``.

        ..  container:: example

            >>> abjad.RehearsalMark(number=1).context
            'Score'

        '''
        return self._context

    @property
    def markup(self) -> typing.Optional[Markup]:
        r'''Gets rehearsal mark markup.

        ..  container:: example

            >>> markup = abjad.Markup(r'\bold { \italic { A } }')
            >>> mark = abjad.RehearsalMark(markup=markup)
            >>> staff = abjad.Staff("c'4 d' e' f'")
            >>> abjad.attach(mark, staff[0])
            >>> abjad.show(staff) # doctest: +SKIP

            ..  docs::

                >>> abjad.f(staff)
                \new Staff
                {
                    \mark \markup {
                        \bold
                            {
                                \italic
                                    {
                                        A
                                    }
                            }
                        }
                    c'4
                    d'4
                    e'4
                    f'4
                }

        '''
        return self._markup

    @property
    def number(self) -> typing.Optional[int]:
        r'''Gets rehearsal mark number.

        ..  container:: example

            >>> abjad.RehearsalMark(number=1).number
            1

        '''
        return self._number

    ### PUBLIC METHODS ###

    @staticmethod
    def from_string(string) -> 'RehearsalMark':
        r'''Makes rehearsal mark from `string`.

        ..  container:: example

            >>> abjad.RehearsalMark.from_string('A')
            RehearsalMark(number=1)

        ..  container:: example

            >>> abjad.RehearsalMark.from_string('AA')
            RehearsalMark(number=27)

        ..  container:: example

            >>> abjad.RehearsalMark.from_string('AB')
            RehearsalMark(number=28)

        ..  container:: example

            >>> abjad.RehearsalMark.from_string('BA')
            RehearsalMark(number=53)

        ..  container:: example

            >>> abjad.RehearsalMark.from_string('BB')
            RehearsalMark(number=54)

        '''
        number = 0
        for place, letter in enumerate(reversed(string)):
            integer = ord(letter) - ord('A') + 1
            multiplier = 26 ** place 
            integer *= multiplier
            number += integer
        return RehearsalMark(number=number)
