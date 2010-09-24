from abjad.tools.lilyfiletools._BlockAttributed import _BlockAttributed


class HeaderBlock(_BlockAttributed):
   r'''.. versionadded:: 1.1.2

   Abjad model of LilyPond input file header block::

      abjad> header_block = lilyfiletools.HeaderBlock( )
      abjad> header_block.composer = markuptools.Markup('Josquin')
      abjad> header_block.title = markuptools.Markup('Missa sexti tonus')
      
   ::
      
      abjad> f(header_block)
      \header {
         composer = \markup { Josquin }
         title = \markup { Missa sexti tonus }
      }
   '''

   def __init__(self):
      _BlockAttributed.__init__(self)
      self._escaped_name = r'\header'
