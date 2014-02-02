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
__all__.append('dotted_eighths')


talea = rhythmmakertools.Talea(
    counts=(3, 1), 
    denominator=32, 
    )
dotted_sixteenths = rhythmmakertools.TaleaRhythmMaker(
    talea=talea,
    )
__all__.append('dotted_sixteenths')


talea = rhythmmakertools.Talea(
    counts=(3, 1), 
    denominator=64, 
    )
dotted_thirty_seconds = rhythmmakertools.TaleaRhythmMaker(
    talea=talea,
    )
__all__.append('dotted_thirty_seconds')


talea = rhythmmakertools.Talea(
    counts=(1,), 
    denominator=8, 
    )
eighths = rhythmmakertools.TaleaRhythmMaker(
    talea=talea,
    tie_specifier=do_not_tie_split_notes,
    )
__all__.append('eighths')


even_runs = rhythmmakertools.EvenRunRhythmMaker
__all__.append('even_runs')


talea = rhythmmakertools.Talea(
    counts=(1,), 
    denominator=2, 
    )
halves = rhythmmakertools.TaleaRhythmMaker(
    talea=talea,
    tie_specifier=do_not_tie_split_notes,
    )
__all__.append('halves')


talea = rhythmmakertools.Talea(
    counts=(3, 1), 
    denominator=32, 
    )
joined_dotted_sixteenths = rhythmmakertools.TaleaRhythmMaker(
    talea=talea,
    beam_specifier=join_specifier,
    )
__all__.append('joined_dotted_sixteenths')


talea = rhythmmakertools.Talea(
    counts=(1,), 
    denominator=8, 
    )
joined_eighths = rhythmmakertools.TaleaRhythmMaker(
    talea=talea,
    beam_specifier=join_specifier,
    )
__all__.append('joined_eighths')


joined_note_tokens = rhythmmakertools.NoteRhythmMaker(
    beam_specifier=join_specifier,
    )
__all__.append('joined_note_tokens')


talea = rhythmmakertools.Talea(
    counts=(1,), 
    denominator=16, 
    )
joined_sixteenths = rhythmmakertools.TaleaRhythmMaker(
    talea=talea,
    beam_specifier=join_specifier,
    )
__all__.append('joined_sixteenths')


talea = rhythmmakertools.Talea(
    counts=(1,), 
    denominator=32, 
    )
joined_thirty_seconds = rhythmmakertools.TaleaRhythmMaker(
    talea=talea,
    beam_specifier=join_specifier,
    )
__all__.append('joined_thirty_seconds')


note_tokens = rhythmmakertools.NoteRhythmMaker()
__all__.append('note_tokens')


talea = rhythmmakertools.Talea(
    counts=(1,), 
    denominator=4, 
    )
quarters = rhythmmakertools.TaleaRhythmMaker(
    talea=talea,
    tie_specifier=do_not_tie_split_notes,
    )
__all__.append('quarters')


rest_tokens = rhythmmakertools.RestRhythmMaker()
__all__.append('rest_tokens')


talea = rhythmmakertools.Talea(
    counts=(1,), 
    denominator=16, 
    )
sixteenths = rhythmmakertools.TaleaRhythmMaker(
    talea=talea,
    tie_specifier=do_not_tie_split_notes,
    )
__all__.append('sixteenths')


talea = rhythmmakertools.Talea(
    counts=(1,), 
    denominator=64, 
    )
sixty_fourths = rhythmmakertools.TaleaRhythmMaker(
    talea=talea,
    tie_specifier=do_not_tie_split_notes,
    )
__all__.append('sixty_fourths')


skip_tokens = rhythmmakertools.SkipRhythmMaker()
__all__.append('skip_tokens')


talea = rhythmmakertools.Talea(
    counts=(1,), 
    denominator=32,
    )
thirty_seconds = rhythmmakertools.TaleaRhythmMaker(
    talea=talea,
    tie_specifier=do_not_tie_split_notes,
    )
__all__.append('thirty_seconds')


tuplet_monads = rhythmmakertools.TupletRhythmMaker(
    tuplet_ratios=[(1,)],
    )
__all__.append('tuplet_monads')


unbeamed_note_tokens = rhythmmakertools.NoteRhythmMaker(
    beam_specifier=unbeam_specifier,
    )
__all__.append('unbeamed_note_tokens')
