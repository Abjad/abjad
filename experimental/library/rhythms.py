from abjad.tools import sequencetools
from abjad.tools import timetokentools
__all__ = []


pattern, denominator, prolation_addenda  = [3, 1], 16, []
lefts, middles, rights = [0], [0], [0]
left_lengths, right_lengths = [0], [0]
dotted_eighths = timetokentools.OutputBurnishedSignalFilledTimeTokenMaker(
   pattern, denominator, prolation_addenda,
   lefts, middles, rights,
   left_lengths, right_lengths)
dotted_eighths.beam = True
dotted_eighths.name = 'dotted_eighths'
__all__.append(dotted_eighths.name)


pattern, denominator, prolation_addenda  = [3, 1], 32, []
lefts, middles, rights = [0], [0], [0]
left_lengths, right_lengths = [0], [0]
dotted_sixteenths = timetokentools.OutputBurnishedSignalFilledTimeTokenMaker(
   pattern, denominator, prolation_addenda,
   lefts, middles, rights,
   left_lengths, right_lengths)
dotted_sixteenths.beam = True
dotted_sixteenths.name = 'dotted_sixteenths'
__all__.append(dotted_sixteenths.name)


pattern, denominator, prolation_addenda  = [3, 1], 64, []
lefts, middles, rights = [0], [0], [0]
left_lengths, right_lengths = [0], [0]
dotted_thirty_seconds = timetokentools.OutputBurnishedSignalFilledTimeTokenMaker(
   pattern, denominator, prolation_addenda,
   lefts, middles, rights,
   left_lengths, right_lengths)
dotted_thirty_seconds.beam = True
dotted_thirty_seconds.name = 'dotted_thirty_seconds'
__all__.append(dotted_thirty_seconds.name)


pattern, denominator, prolation_addenda  = [1], 8, []
lefts, middles, rights = [0], [0], [0]
left_lengths, right_lengths = [0], [0]
eighths = timetokentools.OutputBurnishedSignalFilledTimeTokenMaker(
   pattern, denominator, prolation_addenda,
   lefts, middles, rights,
   left_lengths, right_lengths)
eighths.beam = True
eighths.name = 'eighths'
__all__.append(eighths.name)


pattern, denominator, prolation_addenda  = [1], 2, []
lefts, middles, rights = [0], [0], [0]
left_lengths, right_lengths = [0], [0]
halves = timetokentools.OutputBurnishedSignalFilledTimeTokenMaker(
   pattern, denominator, prolation_addenda,
   lefts, middles, rights,
   left_lengths, right_lengths)
halves.beam = False
halves.name = 'halves'
__all__.append(halves.name)


note_filled_tokens = timetokentools.NoteFilledTimeTokenMaker()
note_filled_tokens.name = 'note_filled_tokens'
__all__.append(note_filled_tokens.name)


pattern, denominator, prolation_addenda  = [1], 4, []
lefts, middles, rights = [0], [0], [0]
left_lengths, right_lengths = [0], [0]
quarters = timetokentools.OutputBurnishedSignalFilledTimeTokenMaker(
   pattern, denominator, prolation_addenda,
   lefts, middles, rights,
   left_lengths, right_lengths)
quarters.beam = False
quarters.name = 'quarters'
__all__.append(quarters.name)


rest_filled_tokens = timetokentools.RestFilledTimeTokenMaker()
rest_filled_tokens.name = 'rest_filled_tokens'
__all__.append(rest_filled_tokens.name)


pattern, denominator, prolation_addenda  = [1], 16, []
lefts, middles, rights = [0], [0], [0]
left_lengths, right_lengths = [0], [0]
sixteenths = timetokentools.OutputBurnishedSignalFilledTimeTokenMaker(
   pattern, denominator, prolation_addenda,
   lefts, middles, rights,
   left_lengths, right_lengths)
sixteenths.beam = True
sixteenths.name = 'sixteenths'
__all__.append(sixteenths.name)


pattern, denominator, prolation_addenda  = [1], 64, []
lefts, middles, rights = [0], [0], [0]
left_lengths, right_lengths = [0], [0]
sixty_fourths = timetokentools.OutputBurnishedSignalFilledTimeTokenMaker(
   pattern, denominator, prolation_addenda,
   lefts, middles, rights,
   left_lengths, right_lengths)
sixty_fourths.beam = True
sixty_fourths.name = 'sixty_fourths'
__all__.append(sixty_fourths.name)


skip_filled_tokens = timetokentools.SkipFilledTimeTokenMaker()
skip_filled_tokens.name = 'skip_filled_tokens'
__all__.append(skip_filled_tokens.name)


pattern, denominator, prolation_addenda  = [1], 32, []
lefts, middles, rights = [0], [0], [0]
left_lengths, right_lengths = [0], [0]
thirty_seconds = timetokentools.OutputBurnishedSignalFilledTimeTokenMaker(
   pattern, denominator, prolation_addenda,
   lefts, middles, rights,
   left_lengths, right_lengths)
thirty_seconds.beam = True
thirty_seconds.name = 'thirty_seconds'
__all__.append(thirty_seconds.name)


tuplet_monads = timetokentools.TupletMonadTimeTokenMaker()
tuplet_monads.name = 'tuplet_monads'
__all__.append(tuplet_monads.name)
