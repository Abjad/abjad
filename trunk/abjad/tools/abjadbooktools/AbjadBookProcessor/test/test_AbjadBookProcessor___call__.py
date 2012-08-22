from abjad.tools import *
import os
import shutil
import py


def test_AbjadBookProcessor___call___01():

    if __name__ == '__main__':
        directory = os.path.curdir
    else:
        directory = os.path.dirname(__file__)

    filepath = os.path.join(directory, 'text.rst.raw')

    with open(filepath, 'r') as f:
        lines = f.read().split('\n')

    book = abjadbooktools.AbjadBookProcessor(directory, lines, abjadbooktools.ReSTOutputFormat())

    result = book(directory)

    assert result == 'This is **paragraph 1**.\nNow comes some Abjad code\n\n::\n\n   >>> voice = Voice("c\'8 d\'8 e\'8")\n   >>> beamtools.BeamSpanner(voice)\n   BeamSpanner({c\'8, d\'8, e\'8})\n   >>> beam = _\n   >>> show(voice)\n\n.. image:: images/image-1.png\n\n::\n\n   >>> len(beam)\n   1\n   >>> show(voice)\n\n.. image:: images/image-2.png\n\n\nHere is **paragraph 2**, and more Abjad code.\nNotice that in the second block of abjad code I can reference objects and variables created in previous blocks:\n\n::\n\n   >>> spannertools.TrillSpanner(voice[4:])\n   TrillSpanner()\n   >>> f(voice)\n   \\new Voice {\n       c\'8 [\n       d\'8\n       e\'8 ]\n   }\n   >>> show(voice)\n\n.. image:: images/image-3.png\n\n\nHere is **paragraph 3**, and now a function definition.\nNote that this function definition can be used later.\nThe **strip_prompt=true** option tells abjad-book to print the code block as though it wasn\'t passed to the interpreter.\n\n::\n\n   def apply_articulations(components):\n       for i, component in enumerate(components):\n           if i % 2 == 0:\n               marktools.Articulation(\'.\')(component)\n           else:\n               marktools.Articulation(\'^\')(component)\n\n\nHere is **paragraph** 4, where we use the previous function to change the Voice we previously instantiated.\n\n::\n\n   >>> apply_articulations(voice)\n   >>> show(voice)\n\n.. image:: images/image-4.png\n\n\nAnd a final paragraph.\n'
    assert os.path.exists(os.path.join(directory, 'images'))
    shutil.rmtree(os.path.join(directory, 'images'))

    return result
