from abjad.notehead.format import _NoteHeadFormatInterface
#from abjad.notehead.interface import NoteHeadInterface
from abjad.interfaces.notehead.interface import NoteHeadInterface
from abjad.pitch import Pitch
import types


class NoteHead(NoteHeadInterface):
   r'''The head of a single note or one of the heads in a chord.  

   ::

      abjad> note = Note(1, (1, 4))
      abjad> note.note_head
      NoteHead(cs')

   The Abjad NoteHead overrides the LilyPond NoteHead grob. ::

      abjad> note.note_head.color = 'red'
      abjad> print note.format
      \once \override NoteHead #'color = #red
      cs'4
   '''

   def __init__(self, client, pitch = None):
      NoteHeadInterface.__init__(self, client)
      self._formatter = _NoteHeadFormatInterface(self)
      self._style = None
      #self.pitch = pitch
      self.pitch = pitch
      self._unregister_if_necessary( )

   ## OVERLOADS ##

   def __eq__(self, expr):
      if isinstance(expr, NoteHead):
         if self.pitch == expr.pitch:
            return True
      return False

   def __ne__(self, expr):
      return not self == expr

   def __repr__(self):
      if self.pitch:
         return 'NoteHead(%s)' % self.pitch
      else:
         return 'NoteHead( )'

   def __str__(self):
      if self.pitch:
         return str(self.pitch)
      else:
         return ''

   ## PRIVATE ATTRIBUTES ##

   @property
   def _dynamic_key_value_pairs(self):
      result = [ ]
      if self.style is not None:
         result.append(('style', self.style))
      return result

   ## PRIVATE METHODS ##

   def _unregister_if_necessary(self):
      '''Note note_heads should register as format contributors.
      Chord note_heads should not register as format contributors.'''
      from abjad.chord import Chord
      client = getattr(self, '_client', None)
      if client is not None:
         if isinstance(client, Chord):
            client.interfaces._contributors.remove(self)

   ## PUBLIC ATTRIBUTES ##

   @property
   def format(self):
      '''Read-only format string of note_head.

      .. todo:: appears to not currently be working, or necessary.

      ::
      
         abjad> note = Note(1, (1, 4))
         abjad> note.nothead.format
         "cs'"
      '''
      return self.formatter.format

   @property
   def formatter(self):
      '''Read-only reference to note head formatter.

      ::

         abjad> note = Note(1, (1, 4))
         abjad> note.note_head.formatter
         <_NoteHeadFormatInterface>
      '''
      return self._formatter

   @apply
   def pitch( ):
      def fget(self):
         '''Read / write pitch of note_head.

         ::

            abjad> note = Note(1, (1, 4))
            abjad> note.note_head.pitch = 2
            abjad> print note.format
            d'4
         '''
         return self._pitch
      def fset(self, arg):
         if arg is None:
            self._pitch = None
         elif isinstance(arg, (int, float, long)):
            self._pitch = Pitch(arg)
         elif isinstance(arg, tuple):
            self._pitch = Pitch(*arg) 
         elif isinstance(arg, Pitch):
            self._pitch = Pitch(arg)
         elif isinstance(arg, NoteHead):
            self._pitch = arg.pitch
         else:
            raise ValueError('Can not set _NoteHead.pitch = %s' % arg)
      return property(**locals( ))

   @apply
   def style( ):
      def fget(self):
         '''Read / write note_head style.
            Assign a string to override default nothead style.
            Assign None to remove the override.'''
         if self._style is not None:
            return self._style
         ## TODO: This is a hack. 
         ##       Implement HarmonicNaturalNoteheadInterface instead.
         if self._client.__class__.__name__ == 'HarmonicNatural':
            return 'harmonic'
      def fset(self, arg):
         if not isinstance(arg, (str, types.NoneType)):
            raise TypeError
         self._style = arg
      return property(**locals( ))      
