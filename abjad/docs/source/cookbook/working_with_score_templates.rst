Working with score templates and LilyPond concatentation
========================================================

..  abjad::

    template = templatetools.TwoStaffPianoScoreTemplate()
    score = template()
    print(format(score))

Creating a basic score template
-------------------------------

..  abjad::
    :strip-prompt:

    class StringTrioScoreTemplate(abctools.AbjadObject):

        def __call__(self):

            violin_voice = scoretools.Voice(name='Violin Voice')
            violin_staff = scoretools.Staff([violin_voice], name='Violin Staff')
            clef = indicatortools.Clef('treble')
            attach(clef, violin_staff)
            instrument = instrumenttools.Violin()
            attach(instrument, violin_staff)

            viola_voice = scoretools.Voice(name='Viola Voice')
            viola_staff = scoretools.Staff([viola_voice], name='Viola Staff')
            clef = indicatortools.Clef('alto')
            attach(clef, viola_staff)
            instrument = instrumenttools.Viola()
            attach(instrument, viola_staff)

            cello_voice = scoretools.Voice(name='Cello Voice')
            cello_staff = scoretools.Staff([cello_voice], name='Cello Staff')
            clef = indicatortools.Clef('bass')
            attach(clef, cello_staff)
            instrument = instrumenttools.Cello()
            attach(instrument, cello_staff)

            staff_group = scoretools.StaffGroup(
                [violin_staff, viola_staff, cello_staff],
                name='String Trio Staff Group',
                )

            score = scoretools.Score(
                [staff_group],
                name='String Trio Score',
                )

            return score

..  abjad::

    template = StringTrioScoreTemplate()
    score = template()
    print(format(score))
    score['Violin Voice'].extend("c'2 d'2 e'2 f'2")
    score['Viola Voice'].extend("c'2 d'2 e'2 f'2")
    score['Cello Voice'].extend("c'2 d'2 e'2 f'2")
    show(score)

Context concatenation
---------------------

..  abjad::

    score_one = template()
    score_two = template()

..  abjad::

    score_one['Violin Voice'].extend("c'8 d'8 e'8 f'8")
    score_one['Viola Voice'].extend("c8 d8 e8 f8")
    score_one['Cello Voice'].extend("c,8 d,8 e,8 f,8")
    show(score_one)

..  abjad::

    score_two['Violin Voice'].extend("g'8 a'8 b'8 c''8")
    score_two['Viola Voice'].extend("g8 a8 b8 c'8")
    score_two['Cello Voice'].extend("g,8 a,8 b,8 c8")
    show(score_two)

..  abjad::

    lilypond_file = lilypondfiletools.make_basic_lilypond_file()
    both_scores = [score_one, score_two]
    lilypond_file.score_block.items.append(both_scores)
    show(lilypond_file)
    print(format(lilypond_file))
