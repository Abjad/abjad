from experimental import *


def test_PatternedArticulationsHandler___call___01():

    handler = handlertools.articulations.PatternedArticulationsHandler([['>', '-'], ['.']])
    staff = Staff("c'8 d'8 r8 e'8 f'8 r8 g'8 r8")
    handler(staff)

    r'''
    \new Staff {
        c'8 -\accent -\tenuto
        d'8 -\staccato
        r8
        e'8 -\accent -\tenuto
        f'8 -\staccato
        r8
        g'8 -\accent -\tenuto
        r8
    }
    '''

    assert staff.lilypond_format == "\\new Staff {\n\tc'8 -\\accent -\\tenuto\n\td'8 -\\staccato\n\tr8\n\te'8 -\\accent -\\tenuto\n\tf'8 -\\staccato\n\tr8\n\tg'8 -\\accent -\\tenuto\n\tr8\n}"
