def _initialize_rest(client, _Leaf, *args): 
   from abjad.components.Chord import Chord
   from abjad.tools.scoretools._transfer_all_attributes import _transfer_all_attributes
   from abjad.components.Note import Note
   from abjad.components.Rest import Rest
   from abjad.tools.skiptools.Skip import Skip
   if len(args) == 1 and isinstance(args[0], _Leaf):
      if isinstance(args[0], Note):
         note = args[0]
         _Leaf.__init__(client, note.duration.written)
         _transfer_all_attributes(note, client)
         del client._note_head
      if isinstance(args[0], Rest):
         rest = args[0]
         _Leaf.__init__(client, rest.duration.written)
         _transfer_all_attributes(rest, client)
      elif isinstance(args[0], Chord):
         chord = args[0]
         _Leaf.__init__(client, chord.duration.written)
         _transfer_all_attributes(chord, client)
         del client._note_heads
      elif isinstance(args[0], Skip):
         skip = args[0]
         _Leaf.__init__(client, skip.duration.written)
         _transfer_all_attributes(skip, client)
   elif len(args) == 1:
      if isinstance(args[0], str):
         duration = args[0].strip('r')
      else:
         duration = args[0]
      _Leaf.__init__(client, duration)
   else:
      raise ValueError('can not initialize rest.')
