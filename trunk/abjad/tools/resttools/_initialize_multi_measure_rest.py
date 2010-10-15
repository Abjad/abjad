import copy


def _initialize_multi_measure_rest(client, _Leaf, *args): 
   from abjad.components import Chord
   from abjad.components import Note
   from abjad.components import Rest
   from abjad.tools.skiptools import Skip
   if len(args) == 1 and isinstance(args[0], (Note, Rest, Chord, Skip)):
      _Leaf.__init__(client, args[0].duration.written, args[0].duration.multiplier)
      if getattr(args[0], '_override', None) is not None:
         client._override = copy.copy(args[0].override)
      if getattr(args[0], '_set', None) is not None:
         client._set = copy.copy(args[0].set)
   elif len(args) == 1:
      duration = args[0]
      _Leaf.__init__(client, duration)
   else:
      raise ValueError('can not initialize multimeasure rest from "%s".' % str(args))
