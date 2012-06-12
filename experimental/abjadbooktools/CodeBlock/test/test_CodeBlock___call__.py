from abjad.tools import *
from experimental import *
import os


def test_CodeBlock___call___01():

    filepath = os.path.join(os.path.dirname(__file__), 'text.rst.raw')
    f = open(filepath, 'r')
    lines = f.read().split('\n')
    f.close()    

    pipe = documentationtools.Pipe()

    pipe.read_wait()
    pipe.write('from abjad import *\n')
    pipe.read_wait()

    code_blocks = abjadbooktools.extract_code_blocks(lines)

    assert len(code_blocks) == 4

    directory = os.path.dirname(__file__)
    image_count = 0
    for code_block in code_blocks:
        image_count = code_block(pipe, image_count, directory)

    assert image_count == 4

    assert code_blocks[0].processed_results == (
        (
            '>>> voice = Voice("c\'8 d\'8 e\'8")',
            '>>> beamtools.BeamSpanner(voice)',
            "BeamSpanner({c'8, d'8, e'8})",
            '>>> beam = _', '>>> show(voice)'
        ),
        'image-1',
        (
            '>>> len(beam)',
            '1',
            '>>> show(voice)'
        ),
        'image-2',
    )

    assert code_blocks[1].processed_results == (
        (
            '>>> spannertools.TrillSpanner(voice[4:])',
            'TrillSpanner()',
            '>>> show(voice)'
        ),
        'image-3'
    )

    assert code_blocks[2].processed_results == (
        (
            'def apply_articulations(components):',
            '    for i, component in enumerate(components):',
            '        if i % 2 == 0:',
            "            marktools.Articulation('.')(component)",
            '        else:',
            "            marktools.Articulation('legato')(component)",
        ),
    )

    assert code_blocks[3].processed_results == (
        (
            '>>> apply_articulations(voice)',
            '>>> show(voice)'
        ),
        'image-4'
    )

    for code_block in code_blocks:
        for result in code_block.processed_results:
            if isinstance(result, str):
                lypath = os.path.join(os.path.dirname(__file__), '{}.ly'.format(result))
                assert os.path.exists(lypath)
                os.remove(lypath)

    return code_blocks, image_count
