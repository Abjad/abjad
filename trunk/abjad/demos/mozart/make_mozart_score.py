from abjad import *
from abjad.demos.mozart.choose_mozart_measures import choose_mozart_measures
from abjad.demos.mozart.make_mozart_measure import make_mozart_measure


def make_mozart_score():

    score_template = scoretemplatetools.TwoStaffPianoScoreTemplate()
    score = score_template()

    # select the measures to use
    choices = choose_mozart_measures()

    # create and populate the volta containers
    treble_volta = Container()
    bass_volta = Container()
    for choice in choices[:7]:
        treble, bass = make_mozart_measure(choice)
        treble_volta.append(treble)
        bass_volta.append(bass)

    # add marks to the volta containers
    marktools.LilyPondCommandMark(
        'repeat volta 2', 'before'
        )(treble_volta)
    marktools.LilyPondCommandMark(
        'repeat volta 2', 'before'
        )(bass_volta)

    # add the volta containers to our staves
    score['RH Voice'].append(treble_volta)
    score['LH Voice'].append(bass_volta)

    # create and populate the alternative ending containers
    treble_alternative = Container()
    bass_alternative = Container()
    for choice in choices[7:9]:
        treble, bass = make_mozart_measure(choice)
        treble_alternative.append(treble)
        bass_alternative.append(bass)

    # add marks to the alternative containers
    marktools.LilyPondCommandMark(
        'alternative', 'before'
        )(treble_alternative)
    marktools.LilyPondCommandMark(
        'alternative', 'before'
        )(bass_alternative)

    # add the alternative containers to our staves
    score['RH Voice'].append(treble_alternative)
    score['LH Voice'].append(bass_alternative)

    # create the remaining measures
    for choice in choices[9:]:
        treble, bass = make_mozart_measure(choice)
        score['RH Voice'].append(treble)
        score['LH Voice'].append(bass)

    # add marks
    contexttools.TimeSignatureMark((3, 8))(score['RH Staff'])
    marktools.BarLine('|.')(score['RH Voice'][-1])
    marktools.BarLine('|.')(score['LH Voice'][-1])

    # remove the old, default Piano InstrumentMark attached to the PianoStaff
    # and add a custom instrument mark
    contexttools.detach_instrument_marks_attached_to_component(score['Piano Staff'])
    contexttools.InstrumentMark(
        'Katzenklavier', 'kk.',
        target_context = scoretools.PianoStaff
        )(score['Piano Staff'])

    return score
