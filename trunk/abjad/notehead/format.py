from abjad.core.format import _FormatInterface


class _NoteHeadFormatInterface(_FormatInterface):

   def __init__(self, _note_head):
      _FormatInterface.__init__(self, _note_head)

   ## PRIVATE ATTRIBUTES ##

   ## DEPRECATED: In modern versions of LilyPond (2.12.x and later) ##
   ##             just use \override NoteHead #'style = #'do        ##

#   _abjadLilyStyles = {
#      'triangle' : 'do',         'semicircle' : 're',    'diamond' : 'mi',
#      'tiltedtriangle' : 'fa',   'square' : 'la',        'wedge' : 'ti' }
#
#   @property
#   def _abjad_to_lily_style(self):
#      style = self._abjadLilyStyles.get(self.note_head.style)
#      if style:
#         return style
#      else:
#         return self.note_head.style

   @property
   def _chord_format(self):
      result = [ ]
      #for key, value in vars(self.note_head).items( ):
      for key, value in self.note_head._key_value_pairs:
         if not key.startswith('_'):
            result.append(r'\tweak %s %s' % (
               self.note_head._parser.format_attribute(key),
               self.note_head._parser.format_value(value)))
#      if self.note_head.style:
#         if self.note_head.style in self.stylesSupported:
#            result.append(r'\tweak %s %s' % (
#                  self.note_head._parser.format_attribute('style'),
#                  self.note_head._parser.format_value(
#                     self._abjad_to_lily_style)))
#         else:
#            result.append(r"\%s" % self.note_head.style)
      return result

   @property
   def _note_format(self):
      result = [ ]
#      if self.note_head.style:
#         if self.note_head.style in self.stylesSupported:
#            result.append(r"\once \override NoteHead #'style = #'%s" \
#               % self._abjad_to_lily_style)
#         else:
#            result.append(r"\%s" % self.note_head.style)
      return result

   ## PUBLIC ATTRIBUTES ##

   @property
   def _before(self):
      from abjad.chord import Chord
      result = [ ]
      #client = self.note_head.client
      client = self.note_head._client
      if client and isinstance(client, Chord):
         result.extend(self._chord_format)
      else:
         result.extend(self._note_format)
      return result

   @property
   def format(self):
      result = [ ]
      note_head = self.note_head
      assert note_head.pitch
      result.extend(self._before)
      result.append(note_head.pitch.format)
      result = '\n'.join(result)
      return result

   @property
   def note_head(self):
      return self.interface

#   stylesSupported = (
#      'cross', 'parallelogram', 'concavetriangle', 'slash', 'xcircle',
#      'neomensural', 'harmonic', 'mensural', 'petruccidiamond',
#      'triangle',  'semicircle',  'diamond', 'tiltedtriangle',
#      'square', 'wedge', )
