import copy
import re


def _initialize_note(client, _Leaf, *args): 
   from abjad.components import Rest
   from abjad.components import Chord
   from abjad.components import Note
   from abjad.tools import componenttools
   from abjad.tools.skiptools import Skip
   if len(args) == 1 and isinstance(args[0], (Note, Rest, Chord, Skip)):
      _Leaf.__init__(client, args[0].duration.written, args[0].duration.multiplier)
      if hasattr(args[0], 'pitch'):
         pitch = args[0].pitch
      elif hasattr(args[0], 'pitches'):
         pitch = args[0].pitches[0]
      else:
         pitch = None
      client.note_head = pitch
      if getattr(args[0], '_override', None) is not None:
         client._override = copy.copy(args[0].override)
      if getattr(args[0], '_set', None) is not None:
         client._set = copy.copy(args[0].set)
   elif len(args) == 1 and isinstance(args[0], str):
      from abjad.tools.lilyfiletools._lilypond_leaf_regex import _lilypond_leaf_regex
      match = re.match(_lilypond_leaf_regex, args[0])
      name, ticks, duration_body, dots = match.groups( )
      pitch_string = name + ticks
      duration_string = duration_body + dots
      _Leaf.__init__(client, duration_string)
      client.note_head = pitch_string
   elif len(args) == 2:
      pitch, duration = args
      _Leaf.__init__(client, duration)
      client.note_head = pitch
   elif len(args) == 3:
      pitch, written_duration, lilypond_multiplier = args
      _Leaf.__init__(client, written_duration)
      client.duration.multiplier = lilypond_multiplier
      client.note_head = pitch
   else:
      raise ValueError('can not initialize note from "%s".' % str(args))
