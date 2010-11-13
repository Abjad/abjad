from abjad.tools.treetools import Block


def _make_test_blocks( ):
    return [
        Block(0, 3, 'a'),
        Block(5, 8, 'b'),
        Block(6, 4, 'c'),
        Block(8, 1, 'd'),
        Block(15, 8, 'e'),
        Block(16, 5, 'f'),
        Block(17, 2, 'g'),
        Block(19, 1, 'h'),
        Block(25, 5, 'i'),
        Block(26, 0, 'j'),
        Block(26, 3, 'k'),
        Block(32, 2, 'l'),
        Block(34, 3, 'm'),
    ]

