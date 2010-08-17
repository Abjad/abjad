from abjad.core import _FormatInterface


class _NoteHeadFormatInterface(_FormatInterface):

   def __init__(self, _note_head):
      _FormatInterface.__init__(self, _note_head)

   ## PRIVATE ATTRIBUTES ##

   @property
   def _before(self):
      from abjad.components.Chord import Chord
      result = [ ]
      client = self._client._client
      if client and isinstance(client, Chord):
         result.extend(self._chord_format)
      else:
         result.extend(self._note_format)
      return result

   @property
   def _chord_format(self):
      from abjad.tools.lilyfiletools._format_lilypond_attribute import _format_lilypond_attribute
      from abjad.tools.lilyfiletools._format_lilypond_value import _format_lilypond_value
      result = [ ]
      #for key, value in self._client._key_value_pairs:
      for key, value in vars(self._client.tweak).iteritems( ):
         if not key.startswith('_'):
            result.append(r'\tweak %s %s' % (
               _format_lilypond_attribute(key),
               _format_lilypond_value(value)))
      return result

   @property
   def _note_format(self):
      result = [ ]
      return result

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      result = [ ]
      note_head = self._client
      assert note_head.pitch
      result.extend(self._before)
      result.append(note_head.pitch.format)
      result = '\n'.join(result)
      return result
