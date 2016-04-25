# -*- coding: utf-8 -*-
import collections
import os
from abjad import *
from abjad.tools.rhythmmakertools import *


gallery_division_lists = (
    [
        (4, 16), (5, 16), (1, 2), (2, 12),
        (1, 2), (2, 12), (4, 16), (5, 16),
    ],
    [
        (1, 11), (3, 8), (3, 8), (3, 8),
        (3, 8), (3, 8), (1, 11), (3, 8),
    ],
    [
        (3, 15), (3, 15), (3, 16),
        (5, 24), (5, 24), (5, 16),
        (2, 12), (2, 12), (2, 8),
        (3, 28), (3, 28), (3, 16),
        (1, 9), (1, 9), (1, 8),
    ],
    [
        (9, 16), (1, 5), (9, 16),
        (1, 5), (9, 16), (9, 16),
    ],
    )


def make_configurations_by_class():
    r'''Makes configurations by class.
    '''

    configurations_by_class = collections.OrderedDict()
    pairs = []

    ### NoteRhythmMaker ###

    maker = NoteRhythmMaker()
    pair = (maker, gallery_division_lists)
    pairs.append(pair)

    maker = NoteRhythmMaker(
        tie_specifier=TieSpecifier(
            tie_across_divisions=True,
            ),
        )
    pair = (maker, gallery_division_lists)
    pairs.append(pair)

    maker = NoteRhythmMaker(
        beam_specifier=BeamSpecifier(
            beam_divisions_together=True,
            ),
        )
    pair = (maker, gallery_division_lists)
    pairs.append(pair)

    maker = NoteRhythmMaker(
        duration_spelling_specifier=DurationSpellingSpecifier(
            decrease_durations_monotonically=False,
            ),
        )
    pair = (maker, gallery_division_lists)
    pairs.append(pair)

    maker = NoteRhythmMaker(
        duration_spelling_specifier=DurationSpellingSpecifier(
            decrease_durations_monotonically=False,
            ),
        tie_specifier=TieSpecifier(
            tie_across_divisions=True,
            ),
        )
    pair = (maker, gallery_division_lists)
    pairs.append(pair)

    maker = NoteRhythmMaker(
        duration_spelling_specifier=DurationSpellingSpecifier(
            decrease_durations_monotonically=False,
            ),
        beam_specifier=BeamSpecifier(
            beam_divisions_together=True,
            ),
        )
    pair = (maker, gallery_division_lists)
    pairs.append(pair)

    maker = NoteRhythmMaker(
        duration_spelling_specifier=DurationSpellingSpecifier(
            forbidden_written_duration=Duration(1, 4),
            ),
        )
    pair = (maker, gallery_division_lists)
    pairs.append(pair)

    maker = NoteRhythmMaker(
        duration_spelling_specifier=DurationSpellingSpecifier(
            forbidden_written_duration=Duration(1, 4),
            ),
        tie_specifier=TieSpecifier(
            tie_across_divisions=True,
            ),
        )
    pair = (maker, gallery_division_lists)
    pairs.append(pair)

    maker = NoteRhythmMaker(
        duration_spelling_specifier=DurationSpellingSpecifier(
            forbidden_written_duration=Duration(1, 4),
            decrease_durations_monotonically=False,
            ),
        )
    pair = (maker, gallery_division_lists)
    pairs.append(pair)

    maker = NoteRhythmMaker(
        duration_spelling_specifier=DurationSpellingSpecifier(
            forbidden_written_duration=Duration(1, 4),
            decrease_durations_monotonically=False,
            ),
        tie_specifier=TieSpecifier(
            tie_across_divisions=True,
            ),
        )
    pair = (maker, gallery_division_lists)
    pairs.append(pair)

    maker = NoteRhythmMaker(
        beam_specifier=BeamSpecifier(
            beam_each_division=False,
            ),
        duration_spelling_specifier=DurationSpellingSpecifier(
            forbidden_written_duration=Duration(1, 4),
            ),
        )
    pair = (maker, gallery_division_lists)
    pairs.append(pair)

    maker = NoteRhythmMaker(
        beam_specifier=BeamSpecifier(
            beam_each_division=False,
            ),
        duration_spelling_specifier=DurationSpellingSpecifier(
            forbidden_written_duration=Duration(1, 4),
            ),
        tie_specifier=TieSpecifier(
            tie_across_divisions=True,
            ),
        )
    pair = (maker, gallery_division_lists)
    pairs.append(pair)

    maker = NoteRhythmMaker(
        beam_specifier=BeamSpecifier(
            beam_each_division=False,
            ),
        duration_spelling_specifier=DurationSpellingSpecifier(
            forbidden_written_duration=Duration(1, 4),
            decrease_durations_monotonically=False,
            ),
        )
    pair = (maker, gallery_division_lists)
    pairs.append(pair)

    maker = NoteRhythmMaker(
        beam_specifier=BeamSpecifier(
            beam_each_division=False,
            ),
        duration_spelling_specifier=DurationSpellingSpecifier(
            forbidden_written_duration=Duration(1, 4),
            decrease_durations_monotonically=False,
            ),
        tie_specifier=TieSpecifier(
            tie_across_divisions=True,
            ),
        )
    pair = (maker, gallery_division_lists)
    pairs.append(pair)

    ### RestRhythmMaker ###

    maker = RestRhythmMaker()
    pair = (maker, gallery_division_lists)
    pairs.append(pair)

    maker = RestRhythmMaker(
        duration_spelling_specifier=DurationSpellingSpecifier(
            decrease_durations_monotonically=False,
            ),
        )
    pair = (maker, gallery_division_lists)
    pairs.append(pair)

    maker = RestRhythmMaker(
        duration_spelling_specifier=DurationSpellingSpecifier(
            forbidden_written_duration=Duration(1, 4),
            ),
        )
    pair = (maker, gallery_division_lists)
    pairs.append(pair)

    maker = RestRhythmMaker(
        duration_spelling_specifier=DurationSpellingSpecifier(
            decrease_durations_monotonically=False,
            forbidden_written_duration=Duration(1, 4),
            ),
        )
    pair = (maker, gallery_division_lists)
    pairs.append(pair)

    ### EvenRunRhythmMaker ###

    maker = EvenRunRhythmMaker()
    pair = (maker, gallery_division_lists)
    pairs.append(pair)

    maker = EvenRunRhythmMaker(
        beam_specifier=BeamSpecifier(
            beam_divisions_together=True,
            ),
        )
    pair = (maker, gallery_division_lists)
    pairs.append(pair)

    maker = EvenRunRhythmMaker(
        beam_specifier=BeamSpecifier(
            beam_each_division=False,
            ),
        )
    pair = (maker, gallery_division_lists)
    pairs.append(pair)

    maker = EvenRunRhythmMaker(
        tie_specifier=TieSpecifier(
            tie_across_divisions=True,
            ),
        )
    pair = (maker, gallery_division_lists)
    pairs.append(pair)

    maker = EvenRunRhythmMaker(
        duration_spelling_specifier=DurationSpellingSpecifier(
            forbidden_written_duration=Duration(1, 4),
            ),
        )
    pair = (maker, gallery_division_lists)
    pairs.append(pair)

    maker = EvenRunRhythmMaker(
        exponent=1,
        )
    pair = (maker, gallery_division_lists)
    pairs.append(pair)

    for pair in pairs:
        maker = pair[0]
        if type(maker) not in configurations_by_class:
            configurations_by_class[type(maker)] = []
        configurations_by_class[type(maker)].append(pair)

    return configurations_by_class


if __name__ == '__main__':
    maker = GalleryMaker()
    configurations_by_class = make_configurations_by_class()
    lilypond_file = maker(configurations_by_class)
    file_path = __file__
    directory = os.path.dirname(file_path)
    file_name = 'gallery.pdf'
    file_path = os.path.join(directory, file_name)
    persist(lilypond_file).as_pdf(file_path, remove_ly=False)
