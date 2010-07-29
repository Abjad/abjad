from abjad.core.initializer import _Initializer
from abjad.notehead import NoteHead
import re


class _NoteInitializer(_Initializer):
   
   def __init__(self, client, _Leaf, *args): 
      from abjad.tools.scoretools._transfer_all_attributes import _transfer_all_attributes
      from abjad.rest import Rest
      from abjad.chord import Chord
      from abjad.note import Note
      from abjad.skip import Skip
      from abjad.tools import componenttools
      client.note_head = None
      if len(args) == 1 and isinstance(args[0], _Leaf):
         if isinstance(args[0], Note):
            note = args[0]
            _Leaf.__init__(client, note.duration.written)
            _transfer_all_attributes(note, client)
         if isinstance(args[0], Rest):
            rest = args[0]
            _Leaf.__init__(client, rest.duration.written)
            _transfer_all_attributes(rest, client)
            del client._pitch
         elif isinstance(args[0], Chord):
            chord = args[0]
            _Leaf.__init__(client, chord.duration.written)
            # must copy chord BEFORE _transfer_all_attributes
            if len(chord) > 0:
               copy = componenttools.clone_components_and_fracture_crossing_spanners([chord])[0]
            _transfer_all_attributes(chord, client)
            del client._note_heads
            if len(chord) > 0:
               client.note_head = copy.note_heads[0]
         elif isinstance(args[0], Skip):
            skip = args[0]
            _Leaf.__init__(client, skip.duration.written)
            _transfer_all_attributes(skip, client)
      elif len(args) == 1 and isinstance(args[0], str):
         from abjad.tools.lilyfiletools._lilypond_leaf_regex import \
            _lilypond_leaf_regex
         match = re.match(_lilypond_leaf_regex, args[0])
         name, ticks, duration_body, dots = match.groups( )
         pitch_string = name + ticks
         duration_string = duration_body + dots
         _Leaf.__init__(client, duration_string)
         client.note_head = pitch_string
      elif len(args) == 2:
         pitch, duration = args
         #print pitch, duration, type(pitch)
         _Leaf.__init__(client, duration)
         client.note_head = pitch
         #client.pitch = pitch
      else:
         raise ValueError('can not initialize note.')
