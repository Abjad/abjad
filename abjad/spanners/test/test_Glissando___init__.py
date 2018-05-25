import abjad


def test_Glissando___init___01():
    """
    Initialize empty glissando spanner.
    """

    glissando = abjad.Glissando()
    assert isinstance(glissando, abjad.Glissando)
