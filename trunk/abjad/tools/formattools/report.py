from abjad.component import _Component
from abjad.spanners import Spanner


def report(system_element, verbose = False, output = 'screen'):
   r'''Read-only string report of all format-time contributions
   made to `system_element` by all the different parts of the Abjad
   system plumbing. ::

      abjad> t = Note(0, (1, 4))
      abjad> t.note_head.style = 'cross'
      abjad> t.note_head.color = 'red'
      abjad> t.stem.color = 'red'
      abjad> t.articulations.append('staccato')
      abjad> t.articulations.append('tenuto')
      abjad> t.markup.down.append(r'\italic { ben. marcato }')
      abjad> t.comments.before.append('textual information before')
      abjad> t.comments.after.append('textual information after')      

   ::

      abjad> print formattools.report(t)
      slot_1
              CommentsInterface.before
                      % textual information before
              InterfaceAggregator.overrides
                      \once \override NoteHead #'color = #red
                      \once \override NoteHead #'style = #'cross
                      \once \override Stem #'color = #red
      slot_2
      slot_3
      slot_4
              _LeafFormatter._leaf_body
                      c'4 -\staccato -\tenuto _ \markup { \italic { ben. marcato } }
      slot_5
      slot_6
      slot_7
              CommentsInterface.after
                      % textual information after

   Set `verbose` to True or False.
   
   Set `output` to 'screen' or 'string'.
   '''

   if isinstance(system_element, _Component): 
      return system_element._formatter.report(
         verbose = verbose, output = output)
   elif isinstance(system_element, Spanner):
      return system_element._format.report(output = output)
   else:
      raise TypeError
