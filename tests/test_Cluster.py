import abjad


def test_Cluster___init___01():
    """
    Cluster can be empty.
    """
    cluster = abjad.Cluster([])
    assert not cluster.simultaneous
    assert len(cluster) == 0
    assert abjad.lilypond(cluster) == abjad.string.normalize(
        r"""
        \makeClusters {
        }
        """
    )


def test_Cluster___init___02():
    cluster = abjad.Cluster("cs'4 cs'4 cs'4 cs'4")
    assert isinstance(cluster, abjad.Cluster)
    assert not cluster.simultaneous
    assert len(cluster) == 4
    assert abjad.lilypond(cluster) == abjad.string.normalize(
        r"""
        \makeClusters {
            cs'4
            cs'4
            cs'4
            cs'4
        }
        """
    )
