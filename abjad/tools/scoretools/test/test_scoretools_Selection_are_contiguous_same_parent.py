import abjad


def test_scoretools_Selection_are_contiguous_same_parent_01():
    r'''Is true for strictly contiguous leaves in voice.
    Is false for other time orderings of leaves in voice.
    '''

    voice = abjad.Voice("c'8 d'8 e'8 f'8")

    assert voice[:].are_contiguous_same_parent()

    assert not abjad.select(reversed(voice[:])).are_contiguous_same_parent()

    components = []
    components.extend(voice[2:])
    components.extend(voice[:2])
    assert not abjad.select(components).are_contiguous_same_parent()

    components = []
    components.extend(voice[3:4])
    components.extend(voice[:1])
    assert not abjad.select(components).are_contiguous_same_parent()
    components = [voice]
    components.extend(voice[:])
    assert not abjad.select(components).are_contiguous_same_parent()


def test_scoretools_Selection_are_contiguous_same_parent_02():
    r'''Is true for unincorporated components when orphans allowed.
    Is false for unincorporated components when orphans not allowed.
    '''

    voice = abjad.Voice(r'''
        {
            c'8
            d'8
        }
        {
            e'8
            f'8
        }
        ''')

    assert format(voice) == abjad.String.normalize(
        r'''
        \new Voice {
            {
                c'8
                d'8
            }
            {
                e'8
                f'8
            }
        }
        '''
        )

    assert abjad.select(voice).are_contiguous_same_parent()
    assert not abjad.select(voice).are_contiguous_same_parent(allow_orphans=False)

    assert voice[:].are_contiguous_same_parent()

    assert voice[0][:].are_contiguous_same_parent()
    assert voice[1][:].are_contiguous_same_parent()

    leaves = abjad.select(voice).leaves()
    assert not leaves.are_contiguous_same_parent()


def test_scoretools_Selection_are_contiguous_same_parent_03():
    r'''Is true for orphan leaves when allow_orphans is true.
    Is false for orphan leaves when allow_orphans is false.
    '''

    notes = [
        abjad.Note("c'8"),
        abjad.Note("d'8"), abjad.Note("e'8"), abjad.Note("f'8")]

    assert abjad.select(notes).are_contiguous_same_parent()
    assert not abjad.select(notes).are_contiguous_same_parent(allow_orphans=False)


def test_scoretools_Selection_are_contiguous_same_parent_04():
    r'''Empty selection returns true.
    '''

    assert abjad.Selection().are_contiguous_same_parent()
