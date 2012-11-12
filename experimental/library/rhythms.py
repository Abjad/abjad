from abjad.tools import sequencetools
from abjad.tools import rhythmmakertools
__all__ = []


dotted_eighths = rhythmmakertools.TaleaFilledRhythmMaker([3, 1], 16, beam_cells_together=True)
dotted_eighths.name = 'dotted_eighths'
__all__.append(dotted_eighths.name)


dotted_sixteenths = rhythmmakertools.TaleaFilledRhythmMaker([3, 1], 32, beam_cells_together=True)
dotted_sixteenths.name = 'dotted_sixteenths'
__all__.append(dotted_sixteenths.name)


dotted_thirty_seconds = rhythmmakertools.TaleaFilledRhythmMaker([3, 1], 64, beam_cells_together=True)
dotted_thirty_seconds.name = 'dotted_thirty_seconds'
__all__.append(dotted_thirty_seconds.name)


eighths = rhythmmakertools.TaleaFilledRhythmMaker([1], 8, beam_cells_together=True)
eighths.name = 'eighths'
__all__.append(eighths.name)


# this isn't the best pattern because initializaation of the rhythm-maker resets beam_cells_together
equal_divisions = rhythmmakertools.EqualDivisionRhythmMaker
equal_divisions.beam_cells_together = True
equal_divisions.name = 'equal_divisions'
__all__.append(equal_divisions.name)


halves = rhythmmakertools.TaleaFilledRhythmMaker([1], 2, beam_cells_together=False)
halves.name = 'halves'
__all__.append(halves.name)


note_filled_tokens = rhythmmakertools.NoteFilledRhythmMaker()
note_filled_tokens.name = 'note_filled_tokens'
__all__.append(note_filled_tokens.name)


quarters = rhythmmakertools.TaleaFilledRhythmMaker([1], 4, beam_cells_together=False)
quarters.name = 'quarters'
__all__.append(quarters.name)


rest_filled_tokens = rhythmmakertools.RestFilledRhythmMaker()
rest_filled_tokens.name = 'rest_filled_tokens'
__all__.append(rest_filled_tokens.name)


sixteenths = rhythmmakertools.TaleaFilledRhythmMaker([1], 16, beam_cells_together=True)
sixteenths.name = 'sixteenths'
__all__.append(sixteenths.name)


sixty_fourths = rhythmmakertools.TaleaFilledRhythmMaker([1], 64, beam_cells_together=True)
sixty_fourths.name = 'sixty_fourths'
__all__.append(sixty_fourths.name)


skip_filled_tokens = rhythmmakertools.SkipFilledRhythmMaker()
skip_filled_tokens.name = 'skip_filled_tokens'
__all__.append(skip_filled_tokens.name)


thirty_seconds = rhythmmakertools.TaleaFilledRhythmMaker([1], 32, beam_cells_together=True)
thirty_seconds.name = 'thirty_seconds'
__all__.append(thirty_seconds.name)


tuplet_monads = rhythmmakertools.TupletMonadRhythmMaker()
tuplet_monads.name = 'tuplet_monads'
__all__.append(tuplet_monads.name)
