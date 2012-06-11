from experimental import *


def test_abjadbooktools_extract_code_blocks_01():

    f = open('text.rst.raw', 'r')
    lines = f.read().split('\n')
    f.close()

    code_blocks = abjadbooktools.extract_code_blocks(lines)

    assert code_blocks == (
        abjadbooktools.CodeBlock((
            'voice = Voice("c\'8 d\'8 e\'8")',
            'spannertools.BeamSpanner(voice)',
            'show(voice)',
            'len(beam)',
            'show(voice)'),
            3, 9, hide=False, strip_prompt=False),
        abjadbooktools.CodeBlock((
            'spannertools.TrillSpanner(voice[4:])',
            'show(voice)'),
            14, 17, hide=False, strip_prompt=False),
        abjadbooktools.CodeBlock((
            'def apply_articulations(components):',
            '    for i, component in enumerate(components):',
            '        if i % 2 == 0:',
            "            marktools.Articulation('.')(component)",
            '        else:',
            "            marktools.Articulation('legato')(component)"),
            23, 30, hide=False, strip_prompt=True),
        abjadbooktools.CodeBlock((
            'apply_articulations(voice)',
            'show(voice)'),
            34, 37, hide=False, strip_prompt=False),
    )

    return code_blocks
