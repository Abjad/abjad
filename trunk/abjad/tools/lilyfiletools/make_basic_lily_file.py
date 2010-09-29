from abjad.tools.lilyfiletools.HeaderBlock import HeaderBlock
from abjad.tools.lilyfiletools.LayoutBlock import LayoutBlock
from abjad.tools.lilyfiletools.LilyFile import LilyFile
from abjad.tools.lilyfiletools.PaperBlock import PaperBlock
from abjad.tools.lilyfiletools.ScoreBlock import ScoreBlock


def make_basic_lily_file(music = None):
   r'''.. versionadded:: 1.1.2

   Make basic LilyPond file with `music`::

      abjad> score = Score([Staff(macros.scale(4))])
      abjad> lily_file = lilyfiletools.make_basic_lily_file(score)
      abjad> lily_file.header.composer = markuptools.Markup('Josquin')
      abjad> lily_file.layout.indent = 0
      abjad> lily_file.paper.top_margin = 15
      abjad> lily_file.paper.left_margin = 15
      abjad> f(lily_file)
      \header {
              composer = \markup { Josquin }
      }

      \layout {
              indent = #0
      }

      \paper {
              left-margin = #15
              top-margin = #15
      }

      \new Score <<
              \new Staff {
                      c'8
                      d'8
                      e'8
                      f'8
              }
      >>

   Equip LilyPond file with header, layout and paper blocks.

   Return LilyPond file.
   '''

   lily_file = LilyFile( )

   header_block = HeaderBlock( )
   layout_block = LayoutBlock( )
   paper_block = PaperBlock( )
   score_block = ScoreBlock( )

   lily_file.extend([header_block, layout_block, paper_block, score_block])

   lily_file.header_block = header_block
   lily_file.layout_block = layout_block
   lily_file.paper_block = paper_block
   lily_file.score_block = score_block

   if music is not None:
      score_block.append(music)
      music.lily_file = lily_file

   return lily_file
