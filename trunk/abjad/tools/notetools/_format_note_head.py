def _format_note_head(note_head):
   from abjad.tools.lilyfiletools._format_lilypond_attribute import _format_lilypond_attribute 
   from abjad.tools.lilyfiletools._format_lilypond_value import _format_lilypond_value
   from abjad.components.Chord import Chord

   ## make sure note head has pitch
   assert note_head.pitch
   result = [ ]

   ## format chord note head with optional tweaks
   if isinstance(note_head._client, Chord):
      for key, value in vars(note_head.tweak).iteritems( ):
         if not key.startswith('_'):
            result.append(r'\tweak %s %s' % (
               _format_lilypond_attribute(key),
               _format_lilypond_value(value)))

   ## format note head pitch
   result.append(note_head.pitch.format)
   result = '\n'.join(result)

   ## return formatted note head
   return result
