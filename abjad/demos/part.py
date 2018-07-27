#! /usr/bin/env python
import abjad
import copy


class PartCantusScoreTemplate:
    """
    Pärt Cantus score template.
    """

    ### SPECIAL METHODS ###

    def __call__(self):
        """
        Calls score template.

        Returns LilyPond file.
        """
        # make bell voice and staff
        bell_voice = abjad.Voice(name='Bell Voice')
        bell_staff = abjad.Staff([bell_voice], name='Bell Staff')
        # make first violin voice and staff
        first_violin_voice = abjad.Voice(name='First Violin Voice')
        first_violin_staff = abjad.Staff(
            [first_violin_voice],
            name='First Violin Staff',
            )
        # make second violin voice and staff
        second_violin_voice = abjad.Voice(name='Second Violin Voice')
        second_violin_staff = abjad.Staff(
            [second_violin_voice],
            name='Second Violin Staff',
            )
        # make viola voice and staff
        viola_voice = abjad.Voice(name='Viola Voice')
        viola_staff = abjad.Staff([viola_voice], name='Viola Staff')
        # make cello voice and staff
        cello_voice = abjad.Voice(name='Cello Voice')
        cello_staff = abjad.Staff([cello_voice], name='Cello Staff')
        # make bass voice and staff
        bass_voice = abjad.Voice(name='Bass Voice')
        bass_staff = abjad.Staff([bass_voice], name='Bass Staff')
        # make strings staff group
        strings_staff_group = abjad.StaffGroup([
            first_violin_staff,
            second_violin_staff,
            viola_staff,
            cello_staff,
            bass_staff,
            ],
            name='Strings Staff Group',
            )
        # make score
        score = abjad.Score([
            bell_staff,
            strings_staff_group,
            ],
            name='Pärt Cantus Score'
            )
        # return Pärt Cantus score
        return score


def create_pitch_contour_reservoir():
    """
    Creates pitch contour reservoir.
    """
    import abjadext.tonality
    scale = abjadext.tonality.Scale(('a', 'minor'))
    pitch_ranges = {
        'First Violin': abjad.PitchRange('[C4, A6]'),
        'Second Violin': abjad.PitchRange('[A3, A5]'),
        'Viola': abjad.PitchRange('[E3, A4]'),
        'Cello': abjad.PitchRange('[A2, A3]'),
        'Bass': abjad.PitchRange('[C3, A3]'),
    }
    reservoir = {}
    for name, pitch_range in pitch_ranges.items():
        pitch_set = scale.create_named_pitch_set_in_pitch_range(pitch_range)
        pitches = sorted(pitch_set, reverse=True)
        pitch_descents = []
        for i in range(len(pitches)):
            descent = tuple(pitches[:i + 1])
            pitch_descents.append(descent)
        reservoir[name] = tuple(pitch_descents)
    return reservoir


def durate_pitch_contour_reservoir(pitch_contour_reservoir):
    """
    Durates pitch contour reservoir.
    """
    names = [
        'First Violin',
        'Second Violin',
        'Viola',
        'Cello',
        'Bass',
        ]
    durated_reservoir = {}
    for i, name in enumerate(names):
        long_duration = abjad.Duration(1, 2) * pow(2, i)
        short_duration = long_duration / 2
        rest_duration = long_duration * abjad.Multiplier(3, 2)
        div = rest_duration // abjad.Duration(3, 2)
        mod = rest_duration % abjad.Duration(3, 2)
        initial_rest = abjad.MultimeasureRest((3, 2)) * div
        maker = abjad.LeafMaker()
        if mod:
            initial_rest += maker([None], mod)
        durated_contours = [tuple(initial_rest)]
        pitch_contours = pitch_contour_reservoir[name]
        durations = [long_duration, short_duration]
        counter = 0
        maker = abjad.LeafMaker()
        for pitch_contour in pitch_contours:
            contour = []
            for pitch in pitch_contour:
                leaves = maker([pitch], [durations[counter]])
                contour.extend(leaves)
                counter = (counter + 1) % 2
            durated_contours.append(tuple(contour))
        durated_reservoir[name] = tuple(durated_contours)
    return durated_reservoir


def shadow_pitch_contour_reservoir(pitch_contour_reservoir):
    """
    Shadows pitch contour reservoir.
    """
    shadow_pitch_lookup = {
        abjad.NamedPitchClass('a'): -5,  # add a P4 below
        abjad.NamedPitchClass('g'): -3,  # add a m3 below
        abjad.NamedPitchClass('f'): -1,  # add a m2 below
        abjad.NamedPitchClass('e'): -4,  # add a M3 below
        abjad.NamedPitchClass('d'): -2,  # add a M2 below
        abjad.NamedPitchClass('c'): -3,  # add a m3 below
        abjad.NamedPitchClass('b'): -2,  # add a M2 below
    }
    shadowed_reservoir = {}
    for name, pitch_contours in pitch_contour_reservoir.items():
        # The viola does not receive any diads
        if name == 'Viola':
            shadowed_reservoir['Viola'] = pitch_contours
            continue
        shadowed_pitch_contours = []
        for pitch_contour in pitch_contours[:-1]:
            shadowed_pitch_contour = []
            for pitch in pitch_contour:
                pitch_class = pitch.pitch_class
                shadow_pitch = pitch + shadow_pitch_lookup[pitch_class]
                diad = (shadow_pitch, pitch)
                shadowed_pitch_contour.append(diad)
            shadowed_pitch_contours.append(tuple(shadowed_pitch_contour))
        # treat the final contour differently: the last note does not become a diad
        final_shadowed_pitch_contour = []
        for pitch in pitch_contours[-1][:-1]:
            pitch_class = pitch.pitch_class
            shadow_pitch = pitch + shadow_pitch_lookup[pitch_class]
            diad = (shadow_pitch, pitch)
            final_shadowed_pitch_contour.append(diad)
        final_shadowed_pitch_contour.append(pitch_contours[-1][-1])
        shadowed_pitch_contours.append(tuple(final_shadowed_pitch_contour))
        shadowed_reservoir[name] = tuple(shadowed_pitch_contours)
    return shadowed_reservoir


def add_bell_music_to_score(score):
    """
    Adds bell music to score.
    """
    def make_bell_phrase():
        phrase = []
        for _ in range(3):
            measure = abjad.Measure((6, 4), r"r2. a'2.")
            abjad.attach(abjad.LaissezVibrer(), measure[-1])
            phrase.append(measure)
            phrase.append(abjad.Measure((6, 4), 'R1.'))
        for _ in range(2):
            phrase.append(abjad.Measure((6, 4), 'R1.'))
        return phrase
    bell_voice = score['Bell Voice']
    for _ in range(11):
        bell_voice.extend(make_bell_phrase())
    for _ in range(19):
        bell_voice.append(abjad.Measure((6, 4), 'R1.'))
    measure = abjad.Measure((6, 4), r"a'1.")
    abjad.attach(abjad.LaissezVibrer(), measure[-1])
    bell_voice.append(measure)


def add_string_music_to_score(score):
    """
    Adds string music to score.
    """
    # generate some pitch and rhythm information
    pitch_contour_reservoir = create_pitch_contour_reservoir()
    shadowed_contour_reservoir = shadow_pitch_contour_reservoir(
        pitch_contour_reservoir)
    durated_reservoir = durate_pitch_contour_reservoir(
        shadowed_contour_reservoir)
    # add six dotted-whole notes and the durated contours to each string voice
    for name, descents in durated_reservoir.items():
        instrument_voice = score['%s Voice' % name]
        instrument_voice.extend("R1. R1. R1. R1. R1. R1.")
        for descent in descents:
            instrument_voice.extend(descent)
    # apply instrument-specific edits
    edit_first_violin_voice(score, durated_reservoir)
    edit_second_violin_voice(score, durated_reservoir)
    edit_viola_voice(score, durated_reservoir)
    edit_cello_voice(score, durated_reservoir)
    edit_bass_voice(score, durated_reservoir)
    # chop all string parts into 6/4 measures
    strings_staff_group = score['Strings Staff Group']
    with abjad.ForbidUpdate(score):
        for voice in abjad.iterate(strings_staff_group).components(abjad.Voice):
            shards = abjad.mutate(voice[:]).split([(6, 4)], cyclic=True)
            for shard in shards:
                measure = abjad.Measure((6, 4), [])
                abjad.mutate(shard).wrap(measure)


def edit_first_violin_voice(score, durated_reservoir):
    """
    Edits first violin voice.
    """
    voice = score['First Violin Voice']
    descents = durated_reservoir['First Violin']
    last_descent = abjad.Selection(descents[-1])
    copied_descent = abjad.mutate(last_descent).copy()
    voice.extend(copied_descent)
    final_sustain_rhythm = [(6, 4)] * 43 + [(1, 2)]
    maker = abjad.NoteMaker()
    final_sustain_notes = maker(["c'"], final_sustain_rhythm)
    voice.extend(final_sustain_notes)
    tie = abjad.Tie()
    abjad.attach(tie, final_sustain_notes)
    voice.extend('r4 r2.')


def edit_second_violin_voice(score, durated_reservoir):
    """
    Edits second violin voice.
    """
    voice = score['Second Violin Voice']
    descents = durated_reservoir['Second Violin']
    last_descent = abjad.Selection(descents[-1])
    copied_descent = abjad.mutate(last_descent).copy()
    copied_descent = list(copied_descent)
    copied_descent[-1].written_duration = abjad.Duration(1, 1)
    copied_descent.append(abjad.Note('a2'))
    for leaf in copied_descent:
        articulation = abjad.Articulation('accent')
        abjad.attach(articulation, leaf)
        articulation = abjad.Articulation('tenuto')
        abjad.attach(articulation, leaf)
    voice.extend(copied_descent)
    final_sustain = []
    for _ in range(32):
        final_sustain.append(abjad.Note('a1.'))
    final_sustain.append(abjad.Note('a2'))
    final_sustain = abjad.Selection(final_sustain)
    articulation = abjad.Articulation('accent')
    abjad.attach(articulation, final_sustain[0])
    articulation = abjad.Articulation('tenuto')
    abjad.attach(articulation, final_sustain[0])
    voice.extend(final_sustain)
    tie = abjad.Tie()
    abjad.attach(tie, final_sustain)
    voice.extend('r4 r2.')


def edit_viola_voice(score, durated_reservoir):
    """
    Edits viola voice.
    """
    voice = score['Viola Voice']
    descents = durated_reservoir['Viola']
    for leaf in descents[-1]:
        articulation = abjad.Articulation('accent')
        abjad.attach(articulation, leaf)
        articulation = abjad.Articulation('tenuto')
        abjad.attach(articulation, leaf)
    last_descent = abjad.Selection(descents[-1])
    copied_descent = abjad.mutate(last_descent).copy()
    for leaf in copied_descent:
        if leaf.written_duration == abjad.Duration(4, 4):
            leaf.written_duration = abjad.Duration(8, 4)
        else:
            leaf.written_duration = abjad.Duration(4, 4)
    voice.extend(copied_descent)
    bridge = abjad.Note('e1')
    articulation = abjad.Articulation('tenuto')
    abjad.attach(articulation, bridge)
    articulation = abjad.Articulation('accent')
    abjad.attach(articulation, bridge)
    voice.append(bridge)
    final_sustain_rhythm = [(6, 4)] * 21 + [(1, 2)]
    maker = abjad.NoteMaker()
    final_sustain_notes = maker(['e'], final_sustain_rhythm)
    articulation = abjad.Articulation('accent')
    abjad.attach(articulation, final_sustain_notes[0])
    articulation = abjad.Articulation('tenuto')
    abjad.attach(articulation, final_sustain_notes[0])
    voice.extend(final_sustain_notes)
    tie = abjad.Tie()
    abjad.attach(tie, final_sustain_notes)
    voice.extend('r4 r2.')


def edit_cello_voice(score, durated_reservoir):
    """
    Edits cello voice.
    """
    voice = score['Cello Voice']
    descents = durated_reservoir['Cello']
    logical_tie = abjad.inspect(voice[-1]).logical_tie()
    for leaf in logical_tie.leaves:
        parent = abjad.inspect(leaf).parentage().parent
        index = parent.index(leaf)
        parent[index] = abjad.Chord(['e,', 'a,'], leaf.written_duration)
    selection = voice[-len(descents[-1]):]
    unison_descent = abjad.mutate(selection).copy()
    voice.extend(unison_descent)
    for chord in unison_descent:
        index = abjad.inspect(chord).parentage().parent.index(chord)
        parent[index] = abjad.Note(
            chord.written_pitches[1], chord.written_duration)
        articulation = abjad.Articulation('accent')
        abjad.attach(articulation, parent[index])
        articulation = abjad.Articulation('tenuto')
        abjad.attach(articulation, parent[index])
    voice.extend('a,1. ~ a,2')
    voice.extend('b,1 ~ b,1. ~ b,1.')
    voice.extend('a,1. ~ a,1. ~ a,1. ~ a,1. ~ a,1. ~ a,2')
    voice.extend('r4 r2.')


def edit_bass_voice(score, durated_reservoir):
    """
    Edits bass voice.
    """
    voice = score['Bass Voice']
    voice[-3:] = '<e, e>\maxima <d, d>\longa <c, c>\maxima <b,>\longa <a,>\maxima r4 r2.'


def apply_bowing_marks(score):
    """
    Applies bowing marks to score.
    """
    # apply alternating upbow and downbow for first two sounding bars
    # of the first violin
    for measure in score['First Violin Voice'][6:8]:
        for i, chord in enumerate(abjad.iterate(measure).components(abjad.Chord)):
            if i % 2 == 0:
                articulation = abjad.Articulation('downbow')
                abjad.attach(articulation, chord)
            else:
                articulation = abjad.Articulation('upbow')
                abjad.attach(articulation, chord)

    # create and apply rebowing markup
    rebow_markup = abjad.Markup.concat([
        abjad.Markup.musicglyph('scripts.downbow'),
        abjad.Markup.hspace(1),
        abjad.Markup.musicglyph('scripts.upbow'),
        ])
    markup = copy.copy(rebow_markup)
    abjad.attach(markup, score['First Violin Voice'][64][0])
    markup = copy.copy(rebow_markup)
    abjad.attach(markup, score['Second Violin Voice'][75][0])
    markup = copy.copy(rebow_markup)
    abjad.attach(markup, score['Viola Voice'][86][0])


def apply_dynamics(score):
    """
    Applies dynamics to score.
    """

    voice = score['Bell Voice']
    dynamic = abjad.Dynamic('ppp')
    abjad.attach(dynamic, voice[0][1])
    dynamic = abjad.Dynamic('pp')
    abjad.attach(dynamic, voice[8][1])
    dynamic = abjad.Dynamic('p')
    abjad.attach(dynamic, voice[18][1])
    dynamic = abjad.Dynamic('mp')
    abjad.attach(dynamic, voice[26][1])
    dynamic = abjad.Dynamic('mf')
    abjad.attach(dynamic, voice[34][1])
    dynamic = abjad.Dynamic('f')
    abjad.attach(dynamic, voice[42][1])
    dynamic = abjad.Dynamic('ff')
    abjad.attach(dynamic, voice[52][1])
    dynamic = abjad.Dynamic('fff')
    abjad.attach(dynamic, voice[60][1])
    dynamic = abjad.Dynamic('ff')
    abjad.attach(dynamic, voice[68][1])
    dynamic = abjad.Dynamic('f')
    abjad.attach(dynamic, voice[76][1])
    dynamic = abjad.Dynamic('mf')
    abjad.attach(dynamic, voice[84][1])
    dynamic = abjad.Dynamic('pp')
    abjad.attach(dynamic, voice[-1][0])

    voice = score['First Violin Voice']
    dynamic = abjad.Dynamic('ppp')
    abjad.attach(dynamic, voice[6][1])
    dynamic = abjad.Dynamic('pp')
    abjad.attach(dynamic, voice[15][0])
    dynamic = abjad.Dynamic('p')
    abjad.attach(dynamic, voice[22][3])
    dynamic = abjad.Dynamic('mp')
    abjad.attach(dynamic, voice[31][0])
    dynamic = abjad.Dynamic('mf')
    abjad.attach(dynamic, voice[38][3])
    dynamic = abjad.Dynamic('f')
    abjad.attach(dynamic, voice[47][0])
    dynamic = abjad.Dynamic('ff')
    abjad.attach(dynamic, voice[55][2])
    dynamic = abjad.Dynamic('fff')
    abjad.attach(dynamic, voice[62][2])

    voice = score['Second Violin Voice']
    dynamic = abjad.Dynamic('pp')
    abjad.attach(dynamic, voice[7][0])
    dynamic = abjad.Dynamic('p')
    abjad.attach(dynamic, voice[12][0])
    dynamic = abjad.Dynamic('p')
    abjad.attach(dynamic, voice[16][0])
    dynamic = abjad.Dynamic('mp')
    abjad.attach(dynamic, voice[25][1])
    dynamic = abjad.Dynamic('mf')
    abjad.attach(dynamic, voice[34][1])
    dynamic = abjad.Dynamic('f')
    abjad.attach(dynamic, voice[44][1])
    dynamic = abjad.Dynamic('ff')
    abjad.attach(dynamic, voice[54][0])
    dynamic = abjad.Dynamic('fff')
    abjad.attach(dynamic, voice[62][1])

    voice = score['Viola Voice']
    dynamic = abjad.Dynamic('p')
    abjad.attach(dynamic, voice[8][0])
    dynamic = abjad.Dynamic('mp')
    abjad.attach(dynamic, voice[19][1])
    dynamic = abjad.Dynamic('mf')
    abjad.attach(dynamic, voice[30][0])
    dynamic = abjad.Dynamic('f')
    abjad.attach(dynamic, voice[36][0])
    dynamic = abjad.Dynamic('f')
    abjad.attach(dynamic, voice[42][0])
    dynamic = abjad.Dynamic('ff')
    abjad.attach(dynamic, voice[52][0])
    dynamic = abjad.Dynamic('fff')
    abjad.attach(dynamic, voice[62][0])

    voice = score['Cello Voice']
    dynamic = abjad.Dynamic('p')
    abjad.attach(dynamic, voice[10][0])
    dynamic = abjad.Dynamic('mp')
    abjad.attach(dynamic, voice[21][0])
    dynamic = abjad.Dynamic('mf')
    abjad.attach(dynamic, voice[31][0])
    dynamic = abjad.Dynamic('f')
    abjad.attach(dynamic, voice[43][0])
    dynamic = abjad.Dynamic('ff')
    abjad.attach(dynamic, voice[52][1])
    dynamic = abjad.Dynamic('fff')
    abjad.attach(dynamic, voice[62][0])

    voice = score['Bass Voice']
    dynamic = abjad.Dynamic('mp')
    abjad.attach(dynamic, voice[14][0])
    dynamic = abjad.Dynamic('mf')
    abjad.attach(dynamic, voice[27][0])
    dynamic = abjad.Dynamic('f')
    abjad.attach(dynamic, voice[39][0])
    dynamic = abjad.Dynamic('ff')
    abjad.attach(dynamic, voice[51][0])
    dynamic = abjad.Dynamic('fff')
    abjad.attach(dynamic, voice[62][0])


def apply_expressive_marks(score):
    """
    Applies expressive marks to score.
    """
    voice = score['First Violin Voice']
    markup = abjad.Markup(
        r'\left-column { div. \line { con sord. } }', direction=abjad.Up)
    abjad.attach(markup, voice[6][1])
    markup = abjad.Markup('sim.', direction=abjad.Up)
    abjad.attach(markup, voice[8][0])
    markup = abjad.Markup('uniti', direction=abjad.Up)
    abjad.attach(markup, voice[58][3])
    markup = abjad.Markup('div.', direction=abjad.Up)
    abjad.attach(markup, voice[59][0])
    markup = abjad.Markup('uniti', direction=abjad.Up)
    abjad.attach(markup, voice[63][3])

    voice = score['Second Violin Voice']
    markup = abjad.Markup('div.', direction=abjad.Up)
    abjad.attach(markup, voice[7][0])
    markup = abjad.Markup('uniti', direction=abjad.Up)
    abjad.attach(markup, voice[66][1])
    markup = abjad.Markup('div.', direction=abjad.Up)
    abjad.attach(markup, voice[67][0])
    markup = abjad.Markup('uniti', direction=abjad.Up)
    abjad.attach(markup, voice[74][0])

    voice = score['Viola Voice']
    markup = abjad.Markup('sole', direction=abjad.Up)
    abjad.attach(markup, voice[8][0])

    voice = score['Cello Voice']
    markup = abjad.Markup('div.', direction=abjad.Up)
    abjad.attach(markup, voice[10][0])
    markup = abjad.Markup('uniti', direction=abjad.Up)
    abjad.attach(markup, voice[74][0])
    markup = abjad.Markup('uniti', direction=abjad.Up)
    abjad.attach(markup, voice[84][1])
    markup = abjad.Markup(r'\italic { espr. }', direction=abjad.Down)
    abjad.attach(markup, voice[86][0])
    markup = abjad.Markup(r'\italic { molto espr. }', direction=abjad.Down)
    abjad.attach(markup, voice[88][1])

    voice = score['Bass Voice']
    markup = abjad.Markup('div.', direction=abjad.Up)
    abjad.attach(markup, voice[14][0])
    markup = abjad.Markup(r'\italic { espr. }', direction=abjad.Down)
    abjad.attach(markup, voice[86][0])
    abjad.mutate(voice[88][:]).split(
        [abjad.Duration(1, 1), abjad.Duration(1, 2)]
        )
    markup = abjad.Markup(r'\italic { molto espr. }', direction=abjad.Down)
    abjad.attach(markup, voice[88][1])
    markup = abjad.Markup('uniti', direction=abjad.Up)
    abjad.attach(markup, voice[99][1])

    strings_staff_group = score['Strings Staff Group']
    for voice in abjad.iterate(strings_staff_group).components(abjad.Voice):
        markup = abjad.Markup(r'\italic { (non dim.) }', direction=abjad.Down)
        abjad.attach(markup, voice[102][0])


def apply_final_bar_lines(score):
    """
    Applies final bar lines to score.
    """
    for voice in abjad.iterate(score).components(abjad.Voice):
        bar_line = abjad.BarLine('|.')
        leaf = abjad.inspect(voice).leaf(-1)
        abjad.attach(bar_line, leaf)


def apply_page_breaks(score):
    """
    Applies page breaks to score.
    """
    bell_voice = score['Bell Voice']
    measure_indices = [
        5, 10, 15, 20,
        25, 30, 35, 40,
        45, 50, 55, 60,
        65, 72, 79, 86,
        93, 100,
        ]
    for measure_index in measure_indices:
        command = abjad.LilyPondLiteral(r'\break', 'after')
        abjad.attach(command, bell_voice[measure_index])


def apply_rehearsal_marks(score):
    """
    Applies rehearsal marks to score.
    """
    bell_voice = score['Bell Voice']
    measure_indices = [
        6, 12, 18, 24,
        30, 36, 42, 48,
        54, 60, 66, 72,
        78, 84, 90, 96,
        102,
        ]
    for measure_index in measure_indices:
        command = abjad.LilyPondLiteral(r'\mark \default', 'before')
        abjad.attach(command, bell_voice[measure_index])


def configure_score(score):
    """
    Configures score.
    """
    # configure bell staff
    bell_staff = score['Bell Staff']
    leaf = abjad.inspect(bell_staff).leaf(0)
    clef = abjad.Clef('treble')
    abjad.attach(clef, leaf)
    bells = abjad.Instrument(
        name='Campana in La',
        short_name='Camp.',
        pitch_range='[C4, C6]',
        )
    abjad.attach(bells, leaf)
    mark = abjad.MetronomeMark((1, 4), (112, 120))
    abjad.attach(mark, leaf)
    time_signature = abjad.TimeSignature((6, 4))
    abjad.attach(time_signature, leaf)
    # configure first violin staff
    first_violin_staff = score['First Violin Staff']
    leaf = abjad.inspect(first_violin_staff).leaf(0)
    clef = abjad.Clef('treble')
    abjad.attach(clef, leaf)
    violin = abjad.Violin(
        markup=abjad.Markup('Violin I'),
        short_markup=abjad.Markup('Vl. I'),
        )
    abjad.attach(violin, leaf)
    # configure second violin staff
    second_violin_staff = score['Second Violin Staff']
    leaf = abjad.inspect(second_violin_staff).leaf(0)
    clef = abjad.Clef('treble')
    abjad.attach(clef, leaf)
    violin = abjad.Violin(
        markup=abjad.Markup('Violin II'),
        short_markup=abjad.Markup('Vl. II'),
        )
    abjad.attach(violin, leaf)
    # configure viola staff
    leaf = abjad.inspect(score['Viola Staff']).leaf(0)
    clef = abjad.Clef('alto')
    abjad.attach(clef, leaf)
    viola = abjad.Viola()
    abjad.attach(viola, leaf)
    # configure cello staff
    leaf = abjad.inspect(score['Cello Staff']).leaf(0)
    clef = abjad.Clef('bass')
    abjad.attach(clef, leaf)
    cello = abjad.Cello()
    abjad.attach(cello, leaf)
    # configure bass staff
    leaf = abjad.inspect(score['Bass Staff']).leaf(0)
    clef = abjad.Clef('bass')
    abjad.attach(clef, leaf)
    contrabass = abjad.Contrabass(
        short_markup=abjad.Markup('Cb.'),
        )
    abjad.attach(contrabass, leaf)
    # configure score
    vector = abjad.SpacingVector(0, 0, 8, 0)
    abjad.override(score).vertical_axis_group.staff_staff_spacing = vector
    abjad.override(score).staff_grouper.staff_staff_spacing = vector
    abjad.override(score).staff_symbol.thickness = 0.5
    scheme = abjad.Scheme('format-mark-box-numbers')
    abjad.setting(score).mark_formatter = scheme


def configure_lilypond_file(lilypond_file):
    """
    Configures LilyPond file.
    """
    lilypond_file._global_staff_size = 8
    context_block = abjad.ContextBlock(
        source_lilypond_type=r'Staff \RemoveEmptyStaves',
        )
    abjad.override(context_block).vertical_axis_group.remove_first = True
    lilypond_file.layout_block.items.append(context_block)
    lilypond_file.paper_block.system_separator_markup = 'slashSeparator'
    bottom_margin = abjad.LilyPondDimension(0.5, 'in')
    lilypond_file.paper_block.bottom_margin = bottom_margin
    top_margin = abjad.LilyPondDimension(0.5, 'in')
    lilypond_file.paper_block.top_margin = top_margin
    left_margin = abjad.LilyPondDimension(0.75, 'in')
    lilypond_file.paper_block.left_margin = left_margin
    right_margin = abjad.LilyPondDimension(0.5, 'in')
    lilypond_file.paper_block.right_margin = right_margin
    paper_width = abjad.LilyPondDimension(5.25, 'in')
    lilypond_file.paper_block.paper_width = paper_width
    paper_height = abjad.LilyPondDimension(7.25, 'in')
    lilypond_file.paper_block.paper_height = paper_height
    lilypond_file.header_block.composer = abjad.Markup('Arvo Pärt')
    title = 'Cantus in Memory of Benjamin Britten (1980)'
    lilypond_file.header_block.title = abjad.Markup(title)


def make_part_lilypond_file():
    """
    Makes Pärt LilyPond file.
    """
    score_template = PartCantusScoreTemplate()
    score = score_template()
    add_bell_music_to_score(score)
    add_string_music_to_score(score)
    apply_bowing_marks(score)
    apply_dynamics(score)
    apply_expressive_marks(score)
    apply_page_breaks(score)
    apply_rehearsal_marks(score)
    apply_final_bar_lines(score)
    configure_score(score)
    lilypond_file = abjad.LilyPondFile.new(score)
    configure_lilypond_file(lilypond_file)
    return lilypond_file


if __name__ == '__main__':
    from abjad import show
    lilypond_file = make_part_lilypond_file()
    show(lilypond_file)
