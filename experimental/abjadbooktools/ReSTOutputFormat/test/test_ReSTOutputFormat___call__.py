from abjad.tools import *
from experimental import *
import os


def test_ReSTOutputFormat___call___01():

    filepath = os.path.join(os.path.dirname(__file__), 'text.rst.raw')
    f = open(filepath, 'r')
    lines = f.read().split('\n')
    f.close()

    pipe = documentationtools.Pipe()

    pipe.read_wait()
    pipe.write('from abjad import *\n')
    pipe.read_wait()

    code_blocks = abjadbooktools.extract_code_blocks(lines)

    directory = os.path.dirname(__file__)
    directory = os.path.curdir
    image_count = 0
    for code_block in code_blocks:
        image_count = code_block(pipe, image_count, directory)

    for code_block in code_blocks:
        for result in code_block.processed_results:
            if isinstance(result, str):
                lypath = os.path.join(os.path.dirname(__file__), '{}.ly'.format(result))
                os.remove(lypath)

    output_format = abjadbooktools.ReSTOutputFormat()

    assert output_format(code_blocks[0]) == (
        '::\n\n   >>> voice = Voice("c\'8 d\'8 e\'8")\n   >>> beamtools.BeamSpanner(voice)\n   BeamSpanner({c\'8, d\'8, e\'8})\n   >>> beam = _\n   >>> show(voice)\n',
        '.. image:: images/image-1.png\n',
        '::\n\n   >>> len(beam)\n   1\n   >>> show(voice)\n',
        '.. image:: images/image-2.png\n'
        )

    assert output_format(code_blocks[1]) == (
        '::\n\n   >>> spannertools.TrillSpanner(voice[4:])\n   TrillSpanner()\n   >>> show(voice)\n',
        '.. image:: images/image-3.png\n'
        )

    assert output_format(code_blocks[2]) == (
        "::\n\n   def apply_articulations(components):\n       for i, component in enumerate(components):\n           if i % 2 == 0:\n               marktools.Articulation('.')(component)\n           else:\n               marktools.Articulation('legato')(component)\n",
        )

    assert output_format(code_blocks[3]) == (
        '::\n\n   >>> apply_articulations(voice)\n   >>> show(voice)\n', '.. image:: images/image-4.png\n'
        )

    return code_blocks
