from abjad import *
__all__ = []


### SPECIFIERS ###

join_specifier = rhythmmakertools.BeamSpecifier(
    beam_each_division=True,
    beam_divisions_together=True,
    )
__all__.append('join_specifier')


do_not_tie_split_notes = rhythmmakertools.TieSpecifier(
    tie_split_notes=False,
    )


unbeam_specifier = rhythmmakertools.BeamSpecifier(
    beam_each_division=False,
    beam_divisions_together=False,
    )
__all__.append('unbeam_specifier')



### MAKERS ###

talea = rhythmmakertools.Talea(
    counts=(3, 1), 
    denominator=16, 
    )
dotted_eighths = rhythmmakertools.TaleaRhythmMaker(
    talea=talea,
    )
dotted_eighths.name = 'dotted_eighths'
__all__.append(dotted_eighths.name)


talea = rhythmmakertools.Talea(
    counts=(3, 1), 
    denominator=32, 
    )
dotted_sixteenths = rhythmmakertools.TaleaRhythmMaker(
    talea=talea,
    )
dotted_sixteenths.name = 'dotted_sixteenths'
__all__.append(dotted_sixteenths.name)


talea = rhythmmakertools.Talea(
    counts=(3, 1), 
    denominator=64, 
    )
dotted_thirty_seconds = rhythmmakertools.TaleaRhythmMaker(
    talea=talea,
    )
dotted_thirty_seconds.name = 'dotted_thirty_seconds'
__all__.append(dotted_thirty_seconds.name)


talea = rhythmmakertools.Talea(
    counts=(1,), 
    denominator=8, 
    )
eighths = rhythmmakertools.TaleaRhythmMaker(
    talea=talea,
    tie_specifier=do_not_tie_split_notes,
    )
eighths.name = 'eighths'
__all__.append(eighths.name)


even_runs = rhythmmakertools.EvenRunRhythmMaker
even_runs.name = 'even_runs'
__all__.append(even_runs.name)


talea = rhythmmakertools.Talea(
    counts=(1,), 
    denominator=2, 
    )
halves = rhythmmakertools.TaleaRhythmMaker(
    talea=talea,
    tie_specifier=do_not_tie_split_notes,
    )
halves.name = 'halves'
__all__.append(halves.name)


talea = rhythmmakertools.Talea(
    counts=(3, 1), 
    denominator=32, 
    )
joined_dotted_sixteenths = rhythmmakertools.TaleaRhythmMaker(
    talea=talea,
    beam_specifier=join_specifier,
    )
joined_dotted_sixteenths.name = 'joined_dotted_sixteenths'
__all__.append(joined_dotted_sixteenths.name)


talea = rhythmmakertools.Talea(
    counts=(1,), 
    denominator=8, 
    )
joined_eighths = rhythmmakertools.TaleaRhythmMaker(
    talea=talea,
    beam_specifier=join_specifier,
    )
joined_eighths.name = 'joined_eighths'
__all__.append(joined_eighths.name)


joined_note_tokens = rhythmmakertools.NoteRhythmMaker(
    beam_specifier=join_specifier,
    )
joined_note_tokens.name = 'joined_note_tokens'
__all__.append(joined_note_tokens.name)


talea = rhythmmakertools.Talea(
    counts=(1,), 
    denominator=16, 
    )
joined_sixteenths = rhythmmakertools.TaleaRhythmMaker(
    talea=talea,
    beam_specifier=join_specifier,
    )
joined_sixteenths.name = 'joined_sixteenths'
__all__.append(joined_sixteenths.name)


talea = rhythmmakertools.Talea(
    counts=(1,), 
    denominator=32, 
    )
joined_thirty_seconds = rhythmmakertools.TaleaRhythmMaker(
    talea=talea,
    beam_specifier=join_specifier,
    )
joined_thirty_seconds.name = 'joined_thirty_seconds'
__all__.append(joined_thirty_seconds.name)


note_tokens = rhythmmakertools.NoteRhythmMaker()
note_tokens.name = 'note_tokens'
__all__.append(note_tokens.name)


talea = rhythmmakertools.Talea(
    counts=(1,), 
    denominator=4, 
    )
quarters = rhythmmakertools.TaleaRhythmMaker(
    talea=talea,
    tie_specifier=do_not_tie_split_notes,
    )
quarters.name = 'quarters'
__all__.append(quarters.name)


rest_tokens = rhythmmakertools.RestRhythmMaker()
rest_tokens.name = 'rest_tokens'
__all__.append(rest_tokens.name)


talea = rhythmmakertools.Talea(
    counts=(1,), 
    denominator=16, 
    )
sixteenths = rhythmmakertools.TaleaRhythmMaker(
    talea=talea,
    tie_specifier=do_not_tie_split_notes,
    )
sixteenths.name = 'sixteenths'
__all__.append(sixteenths.name)


talea = rhythmmakertools.Talea(
    counts=(1,), 
    denominator=64, 
    )
sixty_fourths = rhythmmakertools.TaleaRhythmMaker(
    talea=talea,
    tie_specifier=do_not_tie_split_notes,
    )
sixty_fourths.name = 'sixty_fourths'
__all__.append(sixty_fourths.name)


skip_tokens = rhythmmakertools.SkipRhythmMaker()
skip_tokens.name = 'skip_tokens'
__all__.append(skip_tokens.name)


talea = rhythmmakertools.Talea(
    counts=(1,), 
    denominator=32,
    )
thirty_seconds = rhythmmakertools.TaleaRhythmMaker(
    talea=talea,
    tie_specifier=do_not_tie_split_notes,
    )
thirty_seconds.name = 'thirty_seconds'
__all__.append(thirty_seconds.name)


tuplet_monads = rhythmmakertools.TupletRhythmMaker(
    tuplet_ratios=[(1,)],
    )
tuplet_monads.name = 'tuplet_monads'
__all__.append(tuplet_monads.name)


unbeamed_note_tokens = rhythmmakertools.NoteRhythmMaker(
    beam_specifier=unbeam_specifier,
    )
unbeamed_note_tokens.name = 'unbeamed_note_tokens'
__all__.append(unbeamed_note_tokens.name)
