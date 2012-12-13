from abjad.tools import schemetools
from abjad.tools.markuptools.MarkupCommand import MarkupCommand


class MusicGlyph(MarkupCommand):
    '''Abjad model of a LilyPond \musicglyph command:

    ::

        >>> markuptools.MusicGlyph('accidentals.sharp')
        MusicGlyph('accidentals.sharp')
        >>> print _
        \musicglyph #"accidentals.sharp"

    Return `MusicGlyph` instance.
    '''

    ### CLASS ATTRIBUTES ###

    __slots__ = ()

    ### INITIALIZER ###

    def __init__(self, glyph_name):
        from abjad.ly import music_glyphs
        assert glyph_name in music_glyphs, 'Not a valid LilyPond glyph name.'
        glyph_scheme = schemetools.Scheme(glyph_name, force_quotes=True)
        MarkupCommand.__init__(self, 'musicglyph', glyph_scheme)

    ### SPECIAL METHODS ### 

    def __repr__(self):
        return '{}({!r})'.format(self._class_name, self.args[0]._value)
