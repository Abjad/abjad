import abjad
import copy


def apply_bowing_marks(score):
    r'''Applies bowing marks to score.
    '''

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
