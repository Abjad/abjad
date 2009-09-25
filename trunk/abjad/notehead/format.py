from abjad.core.format import _FormatInterface


class _NoteHeadFormatInterface(_FormatInterface):

   def __init__(self, _notehead):
      _FormatInterface.__init__(self, _notehead)

   ## PRIVATE ATTRIBUTES ##

   ## DEPRECATED: In modern versions of LilyPond (2.12.x and later) ##
   ##             just use \override NoteHead #'style = #'do        ##

#   _abjadLilyStyles = {
#      'triangle' : 'do',         'semicircle' : 're',    'diamond' : 'mi',
#      'tiltedtriangle' : 'fa',   'square' : 'la',        'wedge' : 'ti' }
#
#   @property
#   def _abjadToLilyStyle(self):
#      style = self._abjadLilyStyles.get(self.notehead.style)
#      if style:
#         return style
#      else:
#         return self.notehead.style

   @property
   def _chordFormat(self):
      result = [ ]
      #for key, value in vars(self.notehead).items( ):
      for key, value in self.notehead._key_value_pairs:
         if not key.startswith('_'):
            result.append(r'\tweak %s %s' % (
               self.notehead._parser.formatAttribute(key),
               self.notehead._parser.formatValue(value)))
#      if self.notehead.style:
#         if self.notehead.style in self.stylesSupported:
#            result.append(r'\tweak %s %s' % (
#                  self.notehead._parser.formatAttribute('style'),
#                  self.notehead._parser.formatValue(
#                     self._abjadToLilyStyle)))
#         else:
#            result.append(r"\%s" % self.notehead.style)
      return result

   @property
   def _noteFormat(self):
      result = [ ]
#      if self.notehead.style:
#         if self.notehead.style in self.stylesSupported:
#            result.append(r"\once \override NoteHead #'style = #'%s" \
#               % self._abjadToLilyStyle)
#         else:
#            result.append(r"\%s" % self.notehead.style)
      return result

   ## PUBLIC ATTRIBUTES ##

   @property
   def _before(self):
      from abjad.chord import Chord
      result = [ ]
      #client = self.notehead.client
      client = self.notehead._client
      if client and isinstance(client, Chord):
         result.extend(self._chordFormat)
      else:
         result.extend(self._noteFormat)
      return result

   @property
   def format(self):
      result = [ ]
      notehead = self.notehead
      assert notehead.pitch
      result.extend(self._before)
      result.append(notehead.pitch.format)
      result = '\n'.join(result)
      return result

   @property
   def notehead(self):
      return self.interface

#   stylesSupported = (
#      'cross', 'parallelogram', 'concavetriangle', 'slash', 'xcircle',
#      'neomensural', 'harmonic', 'mensural', 'petruccidiamond',
#      'triangle',  'semicircle',  'diamond', 'tiltedtriangle',
#      'square', 'wedge', )
