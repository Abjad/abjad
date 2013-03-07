from experimental import *


def test_ReiteratedArticulationHandler___call___01():

    handler = handlertools.articulations.ReiteratedArticulationHandler(['^', '.'])
    staff = Staff("c'8 d'8 r8 e'8 f'8 r8 g'8 r8")
    handler(staff)

    r'''
    \new Staff {
        c'8 -\marcato -\staccato
        d'8 -\marcato -\staccato
        r8
        e'8 -\marcato -\staccato
        f'8 -\marcato -\staccato
        r8
        g'8 -\marcato -\staccato
        r8
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\tc'8 -\\marcato -\\staccato\n\td'8 -\\marcato -\\staccato\n\tr8\n\te'8 -\\marcato -\\staccato\n\tf'8 -\\marcato -\\staccato\n\tr8\n\tg'8 -\\marcato -\\staccato\n\tr8\n}"


def test_ReiteratedArticulationHandler___call___02():

    handler = handlertools.articulations.ReiteratedArticulationHandler('.')
    staff = Staff("c'8 d'8 r8 e'8 f'8 r8 g'8 r8")
    handler(staff)

    r'''
    \new Staff {
        c'8 -\staccato
        d'8 -\staccato
        r8
        e'8 -\staccato
        f'8 -\staccato
        r8
        g'8 -\staccato
        r8
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\tc'8 -\\staccato\n\td'8 -\\staccato\n\tr8\n\te'8 -\\staccato\n\tf'8 -\\staccato\n\tr8\n\tg'8 -\\staccato\n\tr8\n}"
