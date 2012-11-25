from abjad.tools import sequencetools
from abjad.tools import rhythmmakertools
__all__ = []


dotted_eighths = rhythmmakertools.TaleaRhythmMaker([3, 1], 16, beam_cells_together=True)
dotted_eighths.name = 'dotted_eighths'
__all__.append(dotted_eighths.name)


dotted_sixteenths = rhythmmakertools.TaleaRhythmMaker([3, 1], 32, beam_cells_together=True)
dotted_sixteenths.name = 'dotted_sixteenths'
__all__.append(dotted_sixteenths.name)


dotted_thirty_seconds = rhythmmakertools.TaleaRhythmMaker([3, 1], 64, beam_cells_together=True)
dotted_thirty_seconds.name = 'dotted_thirty_seconds'
__all__.append(dotted_thirty_seconds.name)


eighths = rhythmmakertools.TaleaRhythmMaker([1], 8, beam_cells_together=True)
eighths.name = 'eighths'
__all__.append(eighths.name)


# this isn't the best pattern because initializaation of the rhythm-maker resets beam_cells_together
equal_divisions = rhythmmakertools.EqualDivisionRhythmMaker
equal_divisions.beam_cells_together = True
equal_divisions.name = 'equal_divisions'
__all__.append(equal_divisions.name)


even_runs = rhythmmakertools.EvenRunRhythmMaker
even_runs.beam_cells_together = True
even_runs.name = 'even_runs'
__all__.append(even_runs.name)


halves = rhythmmakertools.TaleaRhythmMaker([1], 2, beam_cells_together=False)
halves.name = 'halves'
__all__.append(halves.name)


note_filled_tokens = rhythmmakertools.NoteRhythmMaker()
note_filled_tokens.name = 'note_filled_tokens'
__all__.append(note_filled_tokens.name)


quarters = rhythmmakertools.TaleaRhythmMaker([1], 4, beam_cells_together=False)
quarters.name = 'quarters'
__all__.append(quarters.name)


rest_filled_tokens = rhythmmakertools.RestRhythmMaker()
rest_filled_tokens.name = 'rest_filled_tokens'
__all__.append(rest_filled_tokens.name)


sixteenths = rhythmmakertools.TaleaRhythmMaker([1], 16, beam_cells_together=True)
sixteenths.name = 'sixteenths'
__all__.append(sixteenths.name)


sixty_fourths = rhythmmakertools.TaleaRhythmMaker([1], 64, beam_cells_together=True)
sixty_fourths.name = 'sixty_fourths'
__all__.append(sixty_fourths.name)


skip_filled_tokens = rhythmmakertools.SkipRhythmMaker()
skip_filled_tokens.name = 'skip_filled_tokens'
__all__.append(skip_filled_tokens.name)


thirty_seconds = rhythmmakertools.TaleaRhythmMaker([1], 32, beam_cells_together=True)
thirty_seconds.name = 'thirty_seconds'
__all__.append(thirty_seconds.name)


tuplet_monads = rhythmmakertools.TupletMonadRhythmMaker()
tuplet_monads.name = 'tuplet_monads'
__all__.append(tuplet_monads.name)
