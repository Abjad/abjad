import copy
import re


def _initialize_chord(client, _Leaf, *args): 
   from abjad.components import Chord
   from abjad.components import Note
   from abjad.components import Rest
   from abjad.tools import componenttools
   from abjad.tools.skiptools.Skip import Skip
   if len(args) == 1 and isinstance(args[0], (Note, Rest, Chord, Skip)):
      _Leaf.__init__(client, args[0].duration.written, args[0].duration.multiplier)
      if hasattr(args[0], 'pitch'):
         pitches = [args[0].pitch]
      elif hasattr(args[0], 'pitches'):
         pitches = args[0].pitches
      else:
         pitches = [ ]
      client.note_heads = pitches
      if getattr(args[0], '_override', None) is not None:
         client._override = copy.copy(args[0].override)
      if getattr(args[0], '_set', None) is not None:
         client._set = copy.copy(args[0].set)
   elif len(args) == 1 and isinstance(args[0], str):
      pattern = '^<(.+)>\s*(.+)'
      match = re.match(pattern, args[0])
      pitch_string, duration_string = match.groups( )
      _Leaf.__init__(client, duration_string)
      client.pitches = pitch_string
   elif len(args) == 2:
      pitches, duration = args
      _Leaf.__init__(client, duration)
      client.pitches = pitches
   elif len(args) == 3:
      pitches, written_duration, lilypond_multiplier = args
      _Leaf.__init__(client, written_duration)
      client.duration.multiplier = lilypond_multiplier
      client.pitches = pitches
   else:
      raise ValueError('can not initialize chord from "%s".' % str(args))
