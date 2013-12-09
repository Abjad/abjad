# -*- encoding: utf-8 -*-
import os
import pytest
import shutil
from abjad.tools import *


@pytest.skip('Test runs slowly.')
def test_abjadbooktools_AbjadBookProcessor___call___01():

    if __name__ == '__main__':
        directory = os.path.curdir
    else:
        directory = os.path.dirname(__file__)

    file_path = os.path.join(directory, 'text.rst.raw')

    with open(file_path, 'r') as f:
        lines = f.read().split('\n')

    book = abjadbooktools.AbjadBookProcessor(
        directory, lines, abjadbooktools.ReSTOutputFormat())

    result = book(directory)

    assert systemtools.TestManager.compare(
        result,
        r'''
        This is **paragraph 1**.
        Now comes some Abjad code

        ::

        >>> voice = Voice("c'8 d'8 e'8")
        >>> Beam(voice)
        Beam({c'8, d'8, e'8})
        >>> beam = _
        >>> show(voice)

        .. image:: images/image-1.png

        ::

        >>> len(beam)
        1
        >>> show(voice)

        .. image:: images/image-2.png


        Here is **paragraph 2**, and more Abjad code.
        Notice that in the second block of abjad code I can reference objects and variables created in previous blocks:

        ::

        >>> spannertools.TrillSpanner(voice[4:])
        TrillSpanner()
        >>> print format(voice)
        \new Voice {
            c'8 [
            d'8
            e'8 ]
        }
        >>> show(voice)

        .. image:: images/image-3.png


        Here is **paragraph 3**, and now a function definition.
        Note that this function definition can be used later.
        The **strip_prompt=true** option tells abjad-book to print the code block as though it wasn't passed to the interpreter.

        ::

        def apply_articulations(components):
            for i, component in enumerate(components):
                if i % 2 == 0:
                    Articulation('.')(component)
                else:
                    Articulation('^')(component)


        Here is **paragraph** 4, where we use the previous function to change the Voice we previously instantiated.

        ::

        >>> apply_articulations(voice)
        >>> show(voice)

        .. image:: images/image-4.png


        And a final paragraph.

        '''
        )

    assert os.path.exists(os.path.join(directory, 'images'))
    shutil.rmtree(os.path.join(directory, 'images'))

    return result
