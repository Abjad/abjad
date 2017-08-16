import abjad


def test_spannertools_DuratedComplexBeam___init___01():
    r'''Initialize empty durated complex beam spanner.
    '''

    beam = abjad.DuratedComplexBeam()
    assert isinstance(beam, abjad.DuratedComplexBeam)
