import pytest
import abjad


def test_datastructuretools_TreeContainer_name_01():

    foo = abjad.TreeContainer(name='foo')
    bar = abjad.TreeContainer(name='bar')
    baz = abjad.TreeContainer(name='baz')
    quux = abjad.TreeContainer(name='quux')
    quux2 = abjad.TreeContainer(name='quux')

    foo.append(bar)
    bar.extend([baz, quux])
    baz.append(quux2)

    assert format(foo, 'lilypond') == abjad.String.normalize(
        r'''
        TreeContainer(
            children=(
                TreeContainer(
                    children=(
                        TreeContainer(
                            children=(
                                TreeContainer(
                                    name='quux'
                                    ),
                                ),
                            name='baz'
                            ),
                        TreeContainer(
                            name='quux'
                            ),
                        ),
                    name='bar'
                    ),
                ),
            name='foo'
            )
        '''
        )

    assert foo['bar'] is bar
    assert foo['baz'] is baz
    assert pytest.raises(ValueError, "foo['quux']")

    quux2.name = 'wux'

    assert foo['quux'] is quux
    assert foo['wux'] is quux2
