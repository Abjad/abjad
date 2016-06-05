# -*- coding: utf-8 -*-
import pytest
from abjad import *


def test_datastructuretools_TreeContainer_name_01():

    foo = datastructuretools.TreeContainer(name='foo')
    bar = datastructuretools.TreeContainer(name='bar')
    baz = datastructuretools.TreeContainer(name='baz')
    quux = datastructuretools.TreeContainer(name='quux')
    quux2 = datastructuretools.TreeContainer(name='quux')

    foo.append(bar)
    bar.extend([baz, quux])
    baz.append(quux2)

    assert format(foo, 'lilypond') == stringtools.normalize(
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
