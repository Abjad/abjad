from abjad.tools.componenttools._report_component_format_contributions import \
   _report_component_format_contributions


def report_component_format_contributions_as_string(component, verbose = False):
   r'''.. versionadded:: 1.1.1

   Report `component` format contributions as string::

      abjad> note = Note(0, (1, 4))
      abjad> note.note_head.style = 'cross'
      abjad> note.note_head.color = 'red'
      abjad> note.stem.color = 'red'
      abjad> note.articulations.append('staccato')
      abjad> note.articulations.append('tenuto')
      abjad> note.markup.down.append(r'\italic { ben. marcato }')
      abjad> note.comments.before.append('textual information before')
      abjad> note.comments.after.append('textual information after')  
      abjad> componenttools.report_component_format_contributions_as_string(note)
      "slot_1\n\tCommentsInterface.before\n\t\t% textual information before\n\tInterfaceAg
      gregator.overrides\n\t\t\\once \\override NoteHead #'color = #red\n\t\t\\once \\over
      ride NoteHead #'style = #'cross\n\t\t\\once \\override Stem #'color = #red\nslot_2\n
      slot_3\nslot_4\n\t_LeafFormatter._leaf_body\n\t\tc'4 -\\staccato -\\tenuto _ \\marku
      p { \\italic { ben. marcato } }\nslot_5\nslot_6\nslot_7\n\tCommentsInterface.after\n
      \t\t% textual information after\n"

   Set `verbose` to True or False.
   '''

   return _report_component_format_contributions(
      component, verbose = verbose, output = 'string')
