from abjad.tools.componenttools._report_component_format_contributions import \
   _report_component_format_contributions


def report_component_format_contributions_to_screen(component, verbose = False):
   r'''Report `component` format contributions to screen::

      abjad> note = Note(0, (1, 4))
      abjad> note.note_head.style = 'cross'
      abjad> note.note_head.color = 'red'
      abjad> note.stem.color = 'red'
      abjad> note.articulations.append('staccato')
      abjad> note.articulations.append('tenuto')
      abjad> note.markup.down.append(r'\italic { ben. marcato }')
      abjad> note.comments.before.append('textual information before')
      abjad> note.comments.after.append('textual information after')   
      abjad> componenttools.report_component_format_contributions_to_screen(note)
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
   '''

   return _report_component_format_contributions(
      component, verbose = verbose, output = 'screen')
