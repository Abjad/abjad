from abjad import *


def test_LilyPondComment_before_01():
    '''Test context comments before.'''

    t = Voice("c'8 d'8 e'8 f'8")
    beam = spannertools.BeamSpanner(t[:])
    beam.override.beam.thickness = 3
    marktools.LilyPondComment('Voice before comments here.', 'before')(t)
    marktools.LilyPondComment('More voice before comments.', 'before')(t)

    r'''
    % Voice before comments here.
    % More voice before comments.
    \new Voice {
        \override Beam #'thickness = #3
        c'8 [
        d'8
        e'8
        f'8 ]
        \revert Beam #'thickness
    }
    '''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "% Voice before comments here.\n% More voice before comments.\n\\new Voice {\n\t\\override Beam #'thickness = #3\n\tc'8 [\n\td'8\n\te'8\n\tf'8 ]\n\t\\revert Beam #'thickness\n}"


def test_LilyPondComment_before_02():
    '''Leaf comments before.'''

    t = Note(0, (1, 8))
    t.override.beam.thickness = 3
    marktools.LilyPondComment('Leaf comments before here.', 'before')(t)
    marktools.LilyPondComment('More comments before.', 'before')(t)

    r'''
    % Leaf comments before here.
    % More comments before.
    \once \override Beam #'thickness = #3
    c'8'''

    assert componenttools.is_well_formed_component(t)
    assert t.format == "% Leaf comments before here.\n% More comments before.\n\\once \\override Beam #'thickness = #3\nc'8"
