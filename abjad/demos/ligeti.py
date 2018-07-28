import abjad
import math


def make_desordre_pitches():
    """
    Makes Désordre pitches.
    """

    right_hand = [
        [[-1, 4, 5], [-1, 4, 5, 7, 9]],
        [[0, 7, 9], [-1, 4, 5, 7, 9]],
        [[2, 4, 5, 7, 9], [0, 5, 7]],
        [[-3, -1, 0, 2, 4, 5, 7]],
        [[-3, 2, 4], [-3, 2, 4, 5, 7]],
        [[2, 5, 7], [-3, 9, 11, 12, 14]],
        [[4, 5, 7, 9, 11], [2, 4, 5]],
        [[-5, 4, 5, 7, 9, 11, 12]],
        [[2, 9, 11], [2, 9, 11, 12, 14]],
        ]

    left_hand = [
        [[-9, -4, -2], [-9, -4, -2, 1, 3]],
        [[-6, -2, 1], [-9, -4, -2, 1, 3]],
        [[-4, -2, 1, 3, 6], [-4, -2, 1]],
        [[-9, -6, -4, -2, 1, 3, 6, 1]],
        [[-6, -2, 1], [-6, -2, 1, 3, -2]],
        [[-4, 1, 3], [-6, 3, 6, -6, -4]],
        [[-14, -11, -9, -6, -4], [-14, -11, -9]],
        [[-11, -2, 1, -6, -4, -2, 1, 3]],
        [[-6, 1, 3], [-6, -4, -2, 1, 3]],
        ]

    return [right_hand, left_hand]


def make_desordre_cell(pitches):
    """
    Makes a Désordre cell.
    """

    notes = [abjad.Note(pitch, (1, 8)) for pitch in pitches]
    notes = abjad.Selection(notes)
    beam = abjad.Beam()
    abjad.attach(beam, notes)
    slur = abjad.Slur()
    abjad.attach(slur, notes)
    clef = abjad.Dynamic('f')
    abjad.attach(clef, notes[0])
    dynamic = abjad.Dynamic('p')
    abjad.attach(dynamic, notes[1])

    # make the lower voice
    lower_voice = abjad.Voice(notes)
    lower_voice.name = 'RH Lower Voice'
    command = abjad.LilyPondLiteral(r'\voiceTwo')
    abjad.attach(command, lower_voice)
    n = int(math.ceil(len(pitches) / 2.))
    chord = abjad.Chord([pitches[0], pitches[0] + 12], (n, 8))
    articulation = abjad.Articulation('>')
    abjad.attach(articulation, chord)

    # make the upper voice
    upper_voice = abjad.Voice([chord])
    upper_voice.name = 'RH Upper Voice'
    command = abjad.LilyPondLiteral(r'\voiceOne')
    abjad.attach(command, upper_voice)

    # combine them together
    container = abjad.Container([lower_voice, upper_voice])
    container.is_simultaneous = True

    # make all 1/8 beats breakable
    leaves = abjad.select(lower_voice).leaves()
    for leaf in leaves[:-1]:
        bar_line = abjad.BarLine('')
        abjad.attach(bar_line, leaf)

    return container


def make_desordre_measure(pitches):
    """
    Makes a measure composed of *Désordre cells*.

    ``pitches`` is a list of lists of number (e.g., [[1, 2, 3], [2, 3, 4]])

    Returns a measure.
    """
    for sequence in pitches:
        container = make_desordre_cell(sequence)
        time_signature = abjad.inspect(container).duration()
        time_signature = abjad.NonreducedFraction(time_signature)
        time_signature = time_signature.with_denominator(8)
        measure = abjad.Measure(time_signature, [container])
    return measure


def make_desordre_staff(pitches):
    """
    Makes Désordre staff.
    """

    staff = abjad.Staff()
    for sequence in pitches:
        measure = make_desordre_measure(sequence)
        staff.append(measure)
    return staff


def make_desordre_score(pitches):
    """
    Makes Désordre score.
    """

    assert len(pitches) == 2
    staff_group = abjad.StaffGroup()
    staff_group.lilypond_type = 'PianoStaff'

    # build the music
    for hand in pitches:
        staff = make_desordre_staff(hand)
        staff_group.append(staff)

    # set clef and key signature to left hand staff
    leaf = abjad.inspect(staff_group[1]).leaf(0)
    clef = abjad.Clef('bass')
    abjad.attach(clef, leaf)
    key_signature = abjad.KeySignature('b', 'major')
    abjad.attach(key_signature, leaf)

    # wrap the piano staff in a score
    score = abjad.Score([staff_group])

    return score


def make_desordre_lilypond_file(score):
    """
    Makes Désordre LilyPond file.
    """
    lilypond_file = abjad.LilyPondFile.new(
        music=score,
        default_paper_size=('a4', 'letter'),
        global_staff_size=14,
        )

    lilypond_file.layout_block.indent = 0
    lilypond_file.layout_block.ragged_right = True
    lilypond_file.layout_block.merge_differently_dotted = True
    lilypond_file.layout_block.merge_differently_headed = True

    context_block = abjad.ContextBlock(
        source_lilypond_type='Score',
        )
    lilypond_file.layout_block.items.append(context_block)
    context_block.remove_commands.append('Bar_number_engraver')
    context_block.remove_commands.append('Default_bar_line_engraver')
    context_block.remove_commands.append('Timing_translator')
    abjad.override(context_block).beam.breakable = True
    abjad.override(context_block).glissando.breakable = True
    abjad.override(context_block).note_column.ignore_collision = True
    abjad.override(context_block).spacing_spanner.uniform_stretching = True
    abjad.override(context_block).text_script.staff_padding = 4
    abjad.override(context_block).text_spanner.breakable = True
    abjad.override(context_block).tuplet_bracket.bracket_visibility = True
    abjad.override(context_block).tuplet_bracket.minimum_length = 3
    abjad.override(context_block).tuplet_bracket.padding = 2
    scheme = abjad.Scheme('ly:spanner::set-spacing-rods')
    abjad.override(context_block).tuplet_bracket.springs_and_rods = scheme
    scheme = abjad.Scheme('tuplet-number::calc-fraction-text')
    abjad.override(context_block).tuplet_number.text = scheme
    abjad.setting(context_block).autoBeaming = False
    moment = abjad.SchemeMoment((1, 12))
    abjad.setting(context_block).proportionalNotationDuration = moment
    abjad.setting(context_block).tupletFullLength = True

    context_block = abjad.ContextBlock(
        source_lilypond_type='Staff',
        )
    lilypond_file.layout_block.items.append(context_block)
    # LilyPond CAUTION: Timing_translator must appear
    #                   before Default_bar_line_engraver!
    context_block.consists_commands.append('Timing_translator')
    context_block.consists_commands.append('Default_bar_line_engraver')
    scheme = abjad.Scheme("'numbered")
    abjad.override(context_block).time_signature.style = scheme

    context_block = abjad.ContextBlock(
        source_lilypond_type='RhythmicStaff',
        )
    lilypond_file.layout_block.items.append(context_block)
    # LilyPond CAUTION: Timing_translator must appear
    #                   before Default_bar_line_engraver!
    context_block.consists_commands.append('Timing_translator')
    context_block.consists_commands.append('Default_bar_line_engraver')
    scheme = abjad.Scheme("'numbered")
    abjad.override(context_block).time_signature.style = scheme
    abjad.override(context_block).vertical_axis_group.minimum_Y_extent = (-2, 4)

    context_block = abjad.ContextBlock(
        source_lilypond_type='Voice',
        )
    lilypond_file.layout_block.items.append(context_block)
    context_block.remove_commands.append('Forbid_line_break_engraver')

    return lilypond_file


if __name__ == '__main__':
    from abjad import show
    pitches = make_desordre_pitches()
    score = make_desordre_score(pitches)
    lilypond_file = make_desordre_lilypond_file(score)
    show(lilypond_file)
