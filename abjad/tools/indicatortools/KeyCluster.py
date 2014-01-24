# -*- encoding: utf-8 -*-
from abjad.tools.abctools.AbjadObject import AbjadObject


class KeyCluster(AbjadObject):
    r'''A key cluster indication.

    ::

        >>> chord = Chord("<c' e' g' b' d'' f''>8")
        >>> key_cluster = indicatortools.KeyCluster()
        >>> attach(key_cluster, chord)
        >>> show(chord) # doctest: +SKIP

    ..  doctest::

        >>> print format(chord)
        \once \override Accidental.stencil = ##f
        \once \override Arpeggio.X-offset = #-2
        \once \override NoteHead.stencil = #ly:text-interface::print
        \once \override NoteHead.text = \markup {
            \filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25
        }
        <c' e' g' b' d'' f''>8
            ^ \markup {
                \center-align
                    \concat
                        {
                            \natural
                            \flat
                        }
                }

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        '_include_black_keys',
        '_include_white_keys',
        '_suppress_markup',
        )

    ### INITIALIZER ###

    def __init__(
        self,
        include_black_keys=True,
        include_white_keys=True,
        suppress_markup=False,
        ):
        assert include_black_keys or include_white_keys
        self._include_black_keys = bool(include_black_keys)
        self._include_white_keys = bool(include_white_keys)
        self._suppress_markup = bool(suppress_markup)

    ### SPECIAL METHODS ###

    def __eq__(self, expr):
        r'''Is true when `expr` is a key cluster indication with black-key and
        white-key inclusion equal to that of this key cluster indication.
        Otherwise false.

        Returns boolean.
        '''
        if isinstance(expr, type(self)):
            if expr.include_black_keys == self.include_black_keys:
                if expr.include_white_keys == self.include_white_keys:
                    if expr.suppress_markup == self.suppress_markup:
                        return True
        return False

    ### PRIVATE PROPERTIES ###

    @property
    def _lilypond_format_bundle(self):
        from abjad.tools import markuptools
        from abjad.tools import systemtools
        lilypond_format_bundle = systemtools.LilyPondFormatBundle()
        lilypond_format_bundle.grob_overrides.append(
            '\\once \\override Accidental.stencil = ##f\n'
            '\\once \\override Arpeggio.X-offset = #-2\n'
            '\\once \\override NoteHead.stencil = #ly:text-interface::print\n'
            '\\once \\override NoteHead.text = \markup {\n'
            "\t\\filled-box #'(-0.6 . 0.6) #'(-0.7 . 0.7) #0.25\n"
            '}'
            )
        if not self.suppress_markup:
            if self.include_black_keys and self.include_white_keys:
                string = r'\center-align \concat { \natural \flat }'
            elif self.include_black_keys:
                string = r'\center-align \flat'
            else:
                string = r'\center-align \natural'
            markup = markuptools.Markup(string, direction=Up)
            markup_format_pieces = markup._get_format_pieces()
            lilypond_format_bundle.right.markup.extend(markup_format_pieces)
        return lilypond_format_bundle

    ### PUBLIC PROPERTIES ###

    @property
    def include_black_keys(self):
        r'''Is true if key cluster includes black keys.

        Returns boolean.
        '''
        return self._include_black_keys

    @property
    def include_white_keys(self):
        r'''Is true if key cluster includes white keys.

        Returns boolean.
        '''
        return self._include_white_keys

    @property
    def suppress_markup(self):
        r'''Is true if key cluster suppresses key markup.

        Returns boolean.
        '''
        return self._suppress_markup
