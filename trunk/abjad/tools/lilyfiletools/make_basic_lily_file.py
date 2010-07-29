from abjad.tools.lilyfiletools.HeaderBlock import HeaderBlock
from abjad.tools.lilyfiletools.LayoutBlock import LayoutBlock
from abjad.tools.lilyfiletools.LilyFile import LilyFile
from abjad.tools.lilyfiletools.PaperBlock import PaperBlock


def make_basic_lily_file(music = None):
   r'''.. versionadded:: 1.1.2

   Make basic LilyPond file with `music`::

      abjad> score = Score([Staff(macros.scale(4))])
      abjad> lily_file = lilyfiletools.make_basic_lily_file(score)
      abjad> lily_file.header.composer = Markup('Josquin')
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
   lily_file.append(HeaderBlock( ))
   lily_file.append(LayoutBlock( ))
   lily_file.append(PaperBlock( ))
   lily_file.append(music)

   if music is not None:
      music._lily_file = lily_file

   lily_file.header = lily_file[0]
   lily_file.layout = lily_file[1]
   lily_file.paper = lily_file[2]
   lily_file.music = lily_file[3]

   return lily_file
