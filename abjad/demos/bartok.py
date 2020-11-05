#! /usr/bin/env python
import abjad

__documentation_section__ = "demos"


def make_bartok_score():
    """
    Makes Bartók score.
    """

    # makes empty score
    score = abjad.Score()
    piano_staff = abjad.StaffGroup(lilypond_type="PianoStaff")
    upper_staff = abjad.Staff(name="Upper_Staff")
    upper_staff_voice = abjad.Voice(name="Upper_Staff_Voice")
    upper_staff.append(upper_staff_voice)
    lower_staff = abjad.Staff(name="Lower_Staff")
    lower_staff_voice_2 = abjad.Voice(name="Lower_Staff_Voice_II")
    lower_staff.append(lower_staff_voice_2)
    piano_staff.append(upper_staff)
    piano_staff.append(lower_staff)
    score.append(piano_staff)

    # populates upper measures
    upper_staff_voice.append(r"{ \time 2/4 a'8 g'8 f'8 e'8 }")
    upper_staff_voice.append(r"{ \time 3/4 d'4 g'8 f'8 e'8 d'8 }")
    upper_staff_voice.append(r"{ \time 2/4 c'8 d'16 e'16 f'8 e'8 }")
    upper_staff_voice.append("{ d'2 }")
    upper_staff_voice.append("{ d'2 }")

    # populates lower measures
    lower_staff_voice_2.append("{ b4 d'8 c'8 }")
    lower_staff_voice_2.append("{ b8 a8 af4 c'8 bf8 }")
    lower_staff_voice_2.append("{ a8 g8 fs8 g16 a16 }")

    # makes simultaneous music for measure 4
    container = abjad.Container(
        [
            abjad.Voice(name="Lower_Staff_Voice_I"),
            abjad.Voice(name="Lower_Staff_Voice_II"),
        ],
        simultaneous=True,
    )
    literal = abjad.LilyPondLiteral(r"\voiceOne")
    abjad.attach(literal, container["Lower_Staff_Voice_I"])
    container["Lower_Staff_Voice_I"].append("b2")
    literal = abjad.LilyPondLiteral(r"\voiceTwo")
    abjad.attach(literal, container["Lower_Staff_Voice_II"])
    container["Lower_Staff_Voice_II"].extend("b4 a4")
    lower_staff.append(container)

    # measure 5
    container = abjad.Container(
        [
            abjad.Voice(name="Lower_Staff_Voice_I"),
            abjad.Voice(name="Lower_Staff_Voice_II"),
        ],
        simultaneous=True,
    )
    literal = abjad.LilyPondLiteral(r"\voiceOne")
    abjad.attach(literal, container["Lower_Staff_Voice_I"])
    container["Lower_Staff_Voice_I"].append("b2")
    literal = abjad.LilyPondLiteral(r"\voiceTwo")
    abjad.attach(literal, container["Lower_Staff_Voice_II"])
    container["Lower_Staff_Voice_II"].append("g2")
    lower_staff.append(container)

    # get leaves
    upper_staff_leaves = abjad.select(upper_staff).leaves()
    lower_staff_voice_1_leaves = []
    for leaf in abjad.select(lower_staff).leaves():
        voice = abjad.get.parentage(leaf).get(abjad.Voice)
        if voice.name == "Lower_Staff_Voice_I":
            lower_staff_voice_1_leaves.append(leaf)
    lower_staff_voice_2_leaves = []
    for leaf in abjad.select(lower_staff).leaves():
        voice = abjad.get.parentage(leaf).get(abjad.Voice)
        if voice.name == "Lower_Staff_Voice_II":
            lower_staff_voice_2_leaves.append(leaf)

    # adds bass clef and final bar line
    clef = abjad.Clef("bass")
    leaf = lower_staff_voice_2_leaves[0]
    abjad.attach(clef, leaf)
    abjad.deprecated.add_final_bar_line(score)

    # adds dynamics
    abjad.attach(abjad.Dynamic("pp"), upper_staff_leaves[0])
    abjad.attach(abjad.Dynamic("mp"), upper_staff_leaves[5])
    abjad.attach(abjad.Dynamic("pp"), lower_staff_voice_2_leaves[1])
    abjad.attach(abjad.Dynamic("mp"), lower_staff_voice_2_leaves[6])
    abjad.override(upper_staff).dynamic_line_spanner.staff_padding = 2
    abjad.override(lower_staff).dynamic_line_spanner.staff_padding = 3

    # attaches beams
    abjad.beam(upper_staff_leaves[:4])
    abjad.beam(lower_staff_voice_2_leaves[1:5])
    abjad.beam(lower_staff_voice_2_leaves[6:10])

    # attaches slurs
    abjad.slur(upper_staff_leaves[:5])
    abjad.slur(upper_staff_leaves[5:])
    abjad.slur(lower_staff_voice_2_leaves[1:6])
    abjad.slur(lower_staff_voice_2_leaves[-10:])
    leaf = lower_staff_voice_2_leaves[-10]
    abjad.override(leaf).slur.direction = abjad.Down

    # attaches hairpins
    abjad.hairpin("< !", upper_staff_leaves[-7:-2])
    abjad.hairpin("> !", upper_staff_leaves[-2:])
    leaf = upper_staff_leaves[-2]
    abjad.override(leaf).hairpin.to_barline = False

    # attaches text spanner with ritardando markup
    markup = abjad.Markup("ritard.")
    start_text_span = abjad.StartTextSpan(left_text=markup)
    abjad.text_spanner(upper_staff_leaves[-7:], start_text_span=start_text_span)
    abjad.override(upper_staff_leaves[-7]).text_spanner.staff_padding = 2

    # ties notes
    abjad.tie(upper_staff_leaves[-2:])
    abjad.tie(lower_staff_voice_1_leaves)

    # returns score
    return score


if __name__ == "__main__":
    lilypond_file = make_bartok_score()
    abjad.show(lilypond_file)
