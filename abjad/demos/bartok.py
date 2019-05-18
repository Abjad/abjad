#! /usr/bin/env python
import abjad
import copy

__documentation_section__ = "demos"


def make_bartok_score():
    """
    make the Bartok example score.
    """

    # make score skeleton
    score = abjad.Score()
    piano_staff = abjad.StaffGroup(lilypond_type="PianoStaff")
    upper_staff = abjad.Staff([])
    lower_staff = abjad.Staff([])
    piano_staff.append(upper_staff)
    piano_staff.append(lower_staff)
    score.append(piano_staff)

    # make upper measures
    upper_measures = []
    upper_measures.append(abjad.Container())
    upper_measures.append(abjad.Container())
    upper_measures.append(abjad.Container())
    upper_measures.append(abjad.Container())
    upper_measures.append(abjad.Container())
    lower_measures = copy.deepcopy(upper_measures)
    upper_staff.extend(upper_measures)
    lower_staff.extend(lower_measures)

    # add leaves to upper measures
    upper_measures[0].extend("a'8 g'8 f'8 e'8")
    abjad.attach(abjad.TimeSignature((2, 4)), upper_measures[0][0])
    upper_measures[1].extend("d'4 g'8 f'8 e'8 d'8")
    abjad.attach(abjad.TimeSignature((3, 4)), upper_measures[1][0])
    upper_measures[2].extend("c'8 d'16 e'16 f'8 e'8")
    abjad.attach(abjad.TimeSignature((2, 4)), upper_measures[2][0])
    upper_measures[3].append("d'2")
    upper_measures[4].append("d'2")

    # add leaves to lower measures
    lower_measures[0].extend("b4 d'8 c'8")
    lower_measures[1].extend("b8 a8 af4 c'8 bf8")
    lower_measures[2].extend("a8 g8 fs8 g16 a16")

    # make parallel music for measure 4
    upper_voice = abjad.Voice("b2", name="upper voice")
    command = abjad.LilyPondLiteral(r"\voiceOne")
    abjad.attach(command, upper_voice)
    lower_voice = abjad.Voice("b4 a4", name="lower voice")
    command = abjad.LilyPondLiteral(r"\voiceTwo")
    abjad.attach(command, lower_voice)
    lower_measures[3].extend([upper_voice, lower_voice])
    lower_measures[3].is_simultaneous = True

    # make parallel music for measure 5
    upper_voice = abjad.Voice("b2", name="upper voice")
    command = abjad.LilyPondLiteral(r"\voiceOne")
    abjad.attach(command, upper_voice)
    lower_voice = abjad.Voice("g2", name="lower voice")
    command = abjad.LilyPondLiteral(r"\voiceTwo")
    abjad.attach(command, lower_voice)
    lower_measures[4].extend([upper_voice, lower_voice])
    lower_measures[4].is_simultaneous = True

    # add bass clef
    clef = abjad.Clef("bass")
    leaf = abjad.inspect(lower_staff).leaf(0)
    abjad.attach(clef, leaf)

    # add dynamics
    dynamic = abjad.Dynamic("pp")
    abjad.attach(dynamic, upper_measures[0][0])
    dynamic = abjad.Dynamic("mp")
    abjad.attach(dynamic, upper_measures[1][1])
    dynamic = abjad.Dynamic("pp")
    abjad.attach(dynamic, lower_measures[0][1])
    dynamic = abjad.Dynamic("mp")
    abjad.attach(dynamic, lower_measures[1][3])

    # add final bar line
    score.add_final_bar_line()

    # select leaves for attaching spanners to
    upper_leaves = abjad.select(upper_staff).leaves()
    lower_leaves = abjad.select(lower_staff).leaves()

    # attach beams
    abjad.beam(upper_leaves[:4])
    abjad.beam(lower_leaves[1:5])
    abjad.beam(lower_leaves[6:10])

    # attach slurs
    abjad.slur(upper_leaves[:5])
    abjad.slur(upper_leaves[5:])
    abjad.slur(lower_leaves[1:6])

    # attach hairpins
    abjad.hairpin("<", upper_leaves[-7:-2])
    abjad.hairpin(">", upper_leaves[-2:])

    # attach a ritardando with markup
    start_text_span = abjad.StartTextSpan(left_text=abjad.Markup("ritard."))
    abjad.text_spanner(upper_leaves[-7:], start_text_span=start_text_span)

    # tie notes
    abjad.tie(upper_leaves[-2:])

    # tie more notes
    note_1 = lower_staff[-2]["upper voice"][0]
    note_2 = lower_staff[-1]["upper voice"][0]
    notes = abjad.select([note_1, note_2])
    abjad.tie(notes)

    # return the score
    return score


if __name__ == "__main__":
    # for mypy
    from abjad import show

    lilypond_file = make_bartok_score()
    show(lilypond_file)
