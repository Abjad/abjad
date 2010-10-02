from abjad.components._Leaf import _Leaf


class Chord(_Leaf):
   '''The Abjad model of a chord:

   ::

      abjad> Chord([4, 13, 17], (1, 4))
      Chord(e' cs'' f'', 4)
   '''

   def __init__(self, *args, **kwargs):
      from abjad.tools.chordtools._initialize_chord import _initialize_chord
      _initialize_chord(self, _Leaf, *args)
      self._initialize_keyword_values(**kwargs)

   ## OVERLOADS ##

   def __contains__(self, arg):
      from abjad.tools import pitchtools
      from abjad.tools.notetools.NoteHead import NoteHead
      if isinstance(arg, (int, float, long)):
         return pitchtools.NamedPitch(arg) in self.pitches
      elif isinstance(arg, pitchtools.NamedPitch):
         return arg in self.pitches
      elif isinstance(arg, NoteHead):
         return arg in self.note_heads
      else:
         return False

   def __delitem__(self, i):
      del(self._note_heads[i])

   def __eq__(self, arg):
      if isinstance(arg, type(self)):
         if self.duration.written == arg.duration.written:
            if self.duration.multiplier == arg.duration.multiplier:
               if self.pitches == arg.pitches:
                  return True
      return False

   def __getitem__(self, i):
      return self._note_heads[i]

   def __len__(self):
      return len(self._note_heads)

   def __repr__(self):
      return '%s(%s, %s)' % (self.__class__.__name__, self._summary, self.duration)

   def __setitem__(self, i, arg):
      from abjad.tools import pitchtools
      from abjad.tools.notetools.NoteHead import NoteHead
      if isinstance(arg, (int, long, float)):
         self._note_heads[i] = NoteHead(self, pitch = arg)
      elif isinstance(arg, pitchtools.NamedPitch):
         self._note_heads[i] = NoteHead(self, pitch = arg)
      elif isinstance(arg, NoteHead):
         self._note_heads[i] = arg
         arg._client = self
      self._sort( )

   ## PRIVATE ATTRIBUTES ##

   @property
   def _compact_representation(self):
      return '<%s>%s' % (self._summary, self.duration)

   ## PRIVATE METHODS ##

   def _sort(self):
      '''Sort note heads in chord by pitch altitude.
      '''
      def _helper(nh1, nh2):
         altitude_cmp = cmp(nh1.pitch.altitude, nh2.pitch.altitude)
         if altitude_cmp == 0:
            return cmp(nh1.pitch.number, nh2.pitch.number)
         else:
            return altitude_cmp
      self._note_heads.sort(_helper)

   @property
   def _summary(self):
      '''Read-only string summary of noteh eads in chord.
      '''
      return ' '.join([str(x) for x in self._note_heads])

   ## PUBLIC ATTRIBUTES ## 

   @apply
   def note_heads( ):
      def fget(self):
         '''Get read-only tuple of note heads in chord::

            abjad> chord = Chord([7, 12, 16], (1, 4))
            abjad> chord.note_heads
            (NoteHead(g'), NoteHead(c''), NoteHead(e''))
   
         Set chord note heads from any iterable::

            abjad> chord = Chord([7, 12, 16], (1, 4))
            abjad> chord.note_heads = [0, 2, 6]
            abjad> chord
            Chord(c' d' fs', 4)
         '''
         result = [ ]
         for note_head in self._note_heads:
            result.append(note_head)
         return tuple(result)
      def fset(self, arglist):
         from abjad.tools.notetools.NoteHead import NoteHead
         assert isinstance(arglist, (list, tuple, set, str))
         self._note_heads = [ ]
         if isinstance(arglist, str):
            arglist = arglist.split( )
         for arg in arglist:
            note_head = NoteHead(self, pitch = arg)
            self._note_heads.append(note_head)
         self._sort( )
      return property(**locals( ))

   @apply
   def pitches( ):
      def fget(self):
         '''Get read-only tuple of pitches in chord::

            abjad> chord = Chord([7, 12, 16], (1, 4))
            abjad> chord.pitches
            (NamedPitch(g, 4), NamedPitch(c, 5), NamedPitch(e, 5))

         Set chord pitches from any iterable::

            abjad> chord = Chord([7, 12, 16], (1, 4))
            abjad> chord.pitches = [0, 2, 6]
            abjad> chord
            Chord(c' d' fs', 4)
         '''
         result = [ ]
         for note_head in self._note_heads:
            if note_head.pitch:
               result.append(note_head.pitch)   
         return tuple(result)
      def fset(self, arglist):
         self.note_heads = arglist
      return property(**locals( ))

   ## PUBLIC METHODS ## 

   def append(self, note_head_token):
      '''Append `note_head_token` to chord::

         abjad> chord = Chord([4, 13, 17], (1, 4))
         abjad> chord
         Chord(e' cs'' f'', 4)

      ::

         abjad> chord.append(19)
         abjad> chord
         Chord(e' cs'' f'' g'', 4)

      Sort chord note heads automatically after append and return none.
      '''
      from abjad.tools import pitchtools
      from abjad.tools.notetools.NoteHead import NoteHead
      from abjad.exceptions import NoteHeadError
      if isinstance(note_head_token, (int, float, long)):
         self._note_heads.append(NoteHead(self, pitch = note_head_token))
      elif isinstance(note_head_token, pitchtools.NamedPitch):
         self._note_heads.append(NoteHead(self, pitch = note_head_token))
      elif isinstance(note_head_token, NoteHead):
         self._note_heads.append(note_head_token)
         note_head_token._client = self
      else:
         raise NoteHeadError('\n\tCan not append to chord: "%s"' % note_head_token)
      self._sort( )

   def extend(self, note_head_tokens):
      '''Extend chord with `note_head_tokens`::

         abjad> chord = Chord([4, 13, 17], (1, 4))
         abjad> chord
         Chord(e' cs'' f'', 4)

      ::

         abjad> chord.extend([2, 12, 18])
         abjad> chord
         Chord(d' e' c'' cs'' f'' fs'', 4)

      Sort chord note heads automatically after extend and return none.
      '''
      assert isinstance(arglist, (tuple, list))
      for arg in arglist:
         self.append(arg)
      self._sort( )

   def pop(self, i = -1):
      '''Remove note head at index `i` in chord::

         abjad> chord = Chord([4, 13, 17], (1, 4))
         abjad> chord
         Chord(e' cs'' f'', 4)

      ::

         abjad> chord.pop(1)
         NoteHead(cs'')

      ::

         abjad> chord
         Chord(e' f'', 4)

      Return note head.
      '''
      note_head = self._note_heads.pop(i)
      note_head._client = None
      return note_head

   def remove(self, note_head):
      '''Remove `note_head` from chord::

         abjad> chord = Chord([4, 13, 17], (1, 4))
         abjad> chord
         Chord(e' cs'' f'', 4)

      ::

         abjad> chord.remove(chord[1])
         abjad> chord
         Chord(e' f'', 4)

      Return none.
      '''
      note_head._client = None
      self._note_heads.remove(note_head)
