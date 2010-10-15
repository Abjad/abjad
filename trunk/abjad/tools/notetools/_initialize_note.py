import re


def _initialize_note(client, _Leaf, *args): 
   from abjad.components import Rest
   from abjad.components import Chord
   from abjad.components import Note
   from abjad.tools import componenttools
   from abjad.tools.scoretools._transfer_all_attributes import _transfer_all_attributes
   from abjad.tools.skiptools import Skip
   client.note_head = None
   if isinstance(args[0], Note):
      note = args[0]
      _Leaf.__init__(client, note.duration.written)
      _transfer_all_attributes(note, client)
   elif isinstance(args[0], Rest):
      rest = args[0]
      _Leaf.__init__(client, rest.duration.written)
      _transfer_all_attributes(rest, client)
   elif isinstance(args[0], Chord):
      chord = args[0]
      _Leaf.__init__(client, chord.duration.written)
      # must copy chord BEFORE _transfer_all_attributes
      if 0 < len(chord):
         copy = componenttools.clone_components_and_fracture_crossing_spanners([chord])[0]
      _transfer_all_attributes(chord, client)
      del client._note_heads
      if 0 < len(chord):
         client.note_head = copy.note_heads[0]
   elif isinstance(args[0], Skip):
      skip = args[0]
      _Leaf.__init__(client, skip.duration.written)
      _transfer_all_attributes(skip, client)
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
