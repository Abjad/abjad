from experimental import *


def extract_code_blocks(lines):
    '''Extract code blocks from `lines`.

    Return a list of abjadbooktools.CodeBlock instances.
    '''

    blocks = []
    block = []
    starting_line_number = 0
    in_block = False

    for i, line in enumerate(lines):

        if line.startswith('<abjad>'):
            if in_block:
                raise Exception('Extra opening tag at line {}.'.format(i))

            else:
                in_block = True
                block = [line]
                starting_line_number = i

        elif line.startswith('</abjad>'):
            if in_block:
                in_block = False
                hide = 'hide=true' in block[0]
                strip_prompt = 'strip_prompt=true' in block[0]
                code_block = abjadbooktools.CodeBlock(lines[1:],
                    starting_line_number,
                    i,
                    hide=hide,
                    strip_prompt=strip_prompt)
                blocks.append(code_block)

            else:
                raise Exception('Extra closing tag at line {}'.format(i))

        elif in_block:
            block.append(line)

    if in_block:
        raise Exception('Unterminated tag at EOF.')

    return blocks
