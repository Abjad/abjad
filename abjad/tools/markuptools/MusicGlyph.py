# -*- encoding: utf-8 -*-
from abjad.tools import schemetools
from abjad.tools.markuptools.MarkupCommand import MarkupCommand


class MusicGlyph(MarkupCommand):
    r'''A LilyPond music glyph.

    ::

        >>> markuptools.MusicGlyph('accidentals.sharp')
        MusicGlyph('accidentals.sharp')
        >>> print _
        \musicglyph #"accidentals.sharp"

    '''

    ### CLASS VARIABLES ###

    __slots__ = (
        )

    ### INITIALIZER ###

    def __init__(self, glyph_name=None):
        from abjad.ly import music_glyphs
        glyph_name = glyph_name or 'accidentals.sharp'
        message = 'not a valid LilyPond glyph name.'
        assert glyph_name in music_glyphs, message
        glyph_scheme = schemetools.Scheme(glyph_name, force_quotes=True)
        MarkupCommand.__init__(self, 'musicglyph', glyph_scheme)

    ### PRIVATE PROPERTIES ###

    @property
    def _storage_format_specification(self):
        from abjad.tools import systemtools
        positional_argument_values = (
            self.args[0]._value,
            )
        return systemtools.StorageFormatSpecification(
            self,
            is_indented=False,
            keyword_argument_names=(),
            positional_argument_values=positional_argument_values,
            )
