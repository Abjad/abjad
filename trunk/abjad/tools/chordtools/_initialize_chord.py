import re


## NOTE - order of steps must be 
##
##        1. _Leaf.__init__
##        2. _transfer_all_attributes

def _initialize_chord(client, _Leaf, *args): 
   from abjad.components import Chord
   from abjad.components import Note
   from abjad.components import Rest
   from abjad.tools import componenttools
   from abjad.tools.scoretools._transfer_all_attributes import _transfer_all_attributes
   from abjad.tools.skiptools.Skip import Skip
   client.pitches = [ ]
   if isinstance(args[0], Note):
      note = args[0]
      _Leaf.__init__(client, note.duration.written)
      # must copy note_head (if required) BEFORE
      # _transfer_all_attributes;
      # otherwise note copy will fail to fracture spanners
      if note.note_head is not None:
         copy = componenttools.clone_components_and_fracture_crossing_spanners([note])[0]
      _transfer_all_attributes(note, client)
      del client._note_head
      if note.note_head is not None:
         client.append(copy.note_head)
   elif isinstance(args[0], Rest):
      rest = args[0]
      _Leaf.__init__(client, rest.duration.written)
      _transfer_all_attributes(rest, client)
   elif isinstance(args[0], Chord):
      chord = args[0]
      _Leaf.__init__(client, chord.duration.written)
      _transfer_all_attributes(chord, client)
   elif isinstance(args[0], Skip):
      skip = args[0]
      _Leaf.__init__(client, skip.duration.written)
      _transfer_all_attributes(skip, client)
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
