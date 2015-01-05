# -*- encoding: utf-8 -*-
from abjad.tools import mathtools
from abjad.tools.abctools.AbjadValueObject import AbjadValueObject


class RehearsalMark(AbjadValueObject):
    r'''A rehearsal mark.

    ..  container:: example

        ::

            >>> staff = Staff("c'4 d' e' f'")
            >>> score = Score([staff])
            >>> mark = indicatortools.RehearsalMark(number=2)
            >>> attach(mark, staff[0])
            >>> scheme = schemetools.Scheme('format-mark-box-alphabet')
            >>> set_(score).markFormatter = scheme

        ::

            >>> show(score) # doctest: +SKIP

        ..  doctest::

            >>> print(format(score))
            \new Score \with {
                markFormatter = #format-mark-box-alphabet
            } <<
                \new Staff {
                    \mark #2
                    c'4
                    d'4
                    e'4
                    f'4
                }
            >>

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_default_scope',
        '_markup',
        '_number',
        )

    ### INITIALIZER ###

    def __init__(self, number=None, markup=None):
        from abjad.tools import markuptools
        # TODO: make default scope work
        #self._default_scope = scoretools.Score
        if markup is not None:
            assert isinstance(markup, markuptools.Markup)
        self._markup = markup
        if number is not None:
            assert mathtools.is_positive_integer(number)
        self._number = number

    ### SPECIAL METHODS ###

    def __str__(self):
        r'''Gets string representation of rehearsal mark.

        ..  container:: example

            ::

                >>> mark = indicatortools.RehearsalMark()
                >>> print(str(mark))
                \mark \default

        Returns string.
        '''
        return self._lilypond_format

    ### PRIVATE METHODS ###

    def _get_lilypond_format_bundle(self, component=None):
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        lilypond_format_bundle.opening.commands.append(str(self))
        return lilypond_format_bundle
        
    ### PRIVATE PROPERTIES ###

    @property
    def _attribute_manifest(self):
        from abjad.tools import systemtools
        from ide import idetools
        return systemtools.AttributeManifest(
            systemtools.AttributeDetail(
                name='number',
                command='n',
                editor=idetools.getters.get_positive_integer,
                ),
            systemtools.AttributeDetail(
                name='markup',
                command='m',
                editor=idetools.getters.get_markup,
                ),
            )

    @property
    def _contents_repr_string(self):
        return str(self)

    @property
    def _lilypond_format(self):
        if self.markup is not None:
            result = r'\mark {}'.format(self.markup)
        elif self.number is not None:
            result = r'\mark #{}'.format(self.number)
        else:
            result = r'\mark \default'
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def markup(self):
        r'''Gets markup of rehearsal mark.

        ..  container:: example

            ::

                >>> markup = Markup(r'\bold { \italic { B } }')
                >>> mark = indicatortools.RehearsalMark(markup=markup)
                >>> print(str(mark.markup))
                \markup {
                    \bold
                        {
                            \italic
                                {
                                    B
                                }
                        }
                    }

        Returns markup or none.
        '''
        return self._markup

    @property
    def number(self):
        r'''Gets number of rehearsal mark.

        ..  container:: example

            ::

                >>> mark = indicatortools.RehearsalMark()
                >>> mark.number is None
                True

        Returns positive integer or none.
        '''
        return self._number