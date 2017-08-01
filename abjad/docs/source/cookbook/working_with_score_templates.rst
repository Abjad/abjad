Working with score templates and LilyPond concatentation
========================================================

..  abjad::

    import abjad
    template = abjad.templatetools.TwoStaffPianoScoreTemplate()
    score = template()
    f(score)

Creating a basic score template
-------------------------------

..  abjad::
    :strip-prompt:

    class StringTrioScoreTemplate(abctools.AbjadObject):

        def __call__(self):

            violin_voice = abjad.Voice(name='Violin Voice')
            violin_staff = abjad.Staff([violin_voice], name='Violin Staff')
            skip = abjad.Skip(1)
            violin_voice.append(skip)
            clef = abjad.Clef('treble')
            attach(clef, skip)
            instrument = abjad.instrumenttools.Violin()
            abjad.attach(instrument, skip)

            viola_voice = abjad.Voice(name='Viola Voice')
            viola_staff = abjad.Staff([viola_voice], name='Viola Staff')
            skip = abjad.Skip(1)
            viola_voice.append(skip)
            clef = abjad.Clef('alto')
            attach(clef, skip)
            instrument = abjad.instrumenttools.Viola()
            abjad.attach(instrument, skip)

            cello_voice = abjad.Voice(name='Cello Voice')
            cello_staff = abjad.Staff([cello_voice], name='Cello Staff')
            skip = abjad.Skip(1)
            cello_voice.append(skip)
            clef = abjad.Clef('bass')
            abjad.attach(clef, skip)
            instrument = abjad.instrumenttools.Cello()
            abjad.attach(instrument, skip)

            staff_group = abjad.StaffGroup(
                [violin_staff, viola_staff, cello_staff],
                name='String Trio Staff Group',
                )

            score = abjad.Score(
                [staff_group],
                name='String Trio Score',
                )

            return score

..  abjad::

    template = StringTrioScoreTemplate()
    score = template()
    f(score)
    show(score)

Context concatenation
---------------------

..  abjad::

    score_one = template()
    score_two = template()

..  abjad::

    score_one['Violin Voice'][:] = "c'8 d'8 e'8 f'8"
    score_one['Viola Voice'][:] = "c8 d8 e8 f8"
    score_one['Cello Voice'][:] = "c,8 d,8 e,8 f,8"
    show(score_one)

..  abjad::

    score_two['Violin Voice'][:] = "g'8 a'8 b'8 c''8"
    score_two['Viola Voice'][:] = "g8 a8 b8 c'8"
    score_two['Cello Voice'][:] = "g,8 a,8 b,8 c8"
    show(score_two)

..  abjad::

    lilypond_file = abjad.LilyPondFile.new()
    both_scores = [score_one, score_two]
    lilypond_file.score_block.items.append(both_scores)
    show(lilypond_file)
    print(format(lilypond_file))
