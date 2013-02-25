# -*- encoding: utf-8 -*-
import os
from abjad import *


def make_nested_tuplet(tuplet_duration, outer_tuplet_proportions, inner_tuplet_subdivision_count):
    outer_tuplet = tuplettools.make_tuplet_from_duration_and_ratio(
        tuplet_duration, outer_tuplet_proportions)
    inner_tuplet_proportions = inner_tuplet_subdivision_count * [1]
    right_tie_chain = tietools.get_tie_chain(outer_tuplet.leaves[-2])
    tietools.tie_chain_to_tuplet_with_ratio(right_tie_chain, inner_tuplet_proportions)
    return outer_tuplet

def make_row_of_nested_tuplets(tuplet_duration, outer_tuplet_proportions, column_count):
    row_of_nested_tuplets = []
    for n in range(column_count):
        inner_tuplet_subdivision_count = n + 1
        nested_tuplet = make_nested_tuplet(
            tuplet_duration, outer_tuplet_proportions, inner_tuplet_subdivision_count)
        row_of_nested_tuplets.append(nested_tuplet)
    return row_of_nested_tuplets

def make_rows_of_nested_tuplets(tuplet_duration, row_count, column_count):
    rows_of_nested_tuplets = []
    for n in range(row_count):
        outer_tuplet_proportions = (1, n + 1, 1)
        row_of_nested_tuplets = make_row_of_nested_tuplets(
            tuplet_duration, outer_tuplet_proportions, column_count)
        rows_of_nested_tuplets.append(row_of_nested_tuplets)
    return rows_of_nested_tuplets

def make_lilypond_file(tuplet_duration, row_count, column_count):
    rows_of_nested_tuplets = make_rows_of_nested_tuplets(tuplet_duration, row_count, column_count)
    all_nested_tuplets = sequencetools.flatten_sequence(rows_of_nested_tuplets)
    staff = stafftools.Staff(all_nested_tuplets)
    #staff = stafftools.RhythmicStaff(all_nested_tuplets)
    time_signature  = contexttools.TimeSignatureMark((1, 4))
    time_signature.attach(staff)
    lets_get_crazy(staff)
    score = Score([staff])
    configure_score(score)
    lilypond_file = lilypondfiletools.make_basic_lilypond_file(score)
    configure_lilypond_file(lilypond_file)
    return lilypond_file

def configure_score(score):
    score.set.proportional_notation_duration = schemetools.SchemeMoment(1, 56)
    score.set.tuplet_full_length = True
    score.override.bar_line.stencil = False
    score.override.bar_number.transparent = True
    score.override.spacing_spanner.uniform_stretching = True
    score.override.spacing_spanner.strict_note_spacing = True
    score.override.time_signature.stencil = False
    score.override.tuplet_bracket.padding = 1.5
    score.override.tuplet_bracket.staff_padding = 2
    score.override.tuplet_number.text = schemetools.Scheme('tuplet-number::calc-fraction-text')
    pass

def configure_lilypond_file(lilypond_file):
    lilypond_file.default_paper_size = '11x17', 'portrait'
    lilypond_file.global_staff_size = 12
    lilypond_file.layout_block.indent = 0
    lilypond_file.layout_block.ragged_right = True
    lilypond_file.paper_block.ragged_bottom = True
    lilypond_file.paper_block.system_system_spacing = layouttools.make_spacing_vector(0, 0, 8, 0)
    pass

def lets_get_crazy(staff):
    for i, tie_chain in enumerate(tietools.iterate_tie_chains_in_expr(staff)):
        if i % 5 == 4:
            for note in tie_chain:
                parent = note.parent
                index = parent.index(note)
                parent[index] = Rest(note)
        else:
            pitch = i % 11
            for note in tie_chain:
                note.written_pitch = pitch
    # add slurs and accents
    notes = []
    for leaf in iterationtools.iterate_leaves_in_expr(staff):
        if isinstance(leaf, Note):
            notes.append(leaf)
        else:
            spannertools.SlurSpanner(notes)
            marktools.Articulation('accent')(notes[0])
            notes = []

if __name__ == '__main__':
    os.system('clear')
    lilypond_file = make_lilypond_file(Duration(1, 4), 10, 6)
    show(lilypond_file)
