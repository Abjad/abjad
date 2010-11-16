from abjad.tools.treetools import BoundedInterval


def _make_test_blocks( ):
    return [
        BoundedInterval(0, 3, 'a'),
        BoundedInterval(5, 13, 'b'),
        BoundedInterval(6, 10, 'c'),
        BoundedInterval(8, 9, 'd'),
        BoundedInterval(15, 23, 'e'),
        BoundedInterval(16, 21, 'f'),
        BoundedInterval(17, 19, 'g'),
        BoundedInterval(19, 20, 'h'),
        BoundedInterval(25, 30, 'i'),
        BoundedInterval(26, 26, 'j'),
        BoundedInterval(26, 29, 'k'),
        BoundedInterval(32, 34, 'l'),
        BoundedInterval(34, 37, 'm'),
#        Block(0, 3, 'a'),
#        Block(5, 8, 'b'),
#        Block(6, 4, 'c'),
#        Block(8, 1, 'd'),
#        Block(15, 8, 'e'),
#        Block(16, 5, 'f'),
#        Block(17, 2, 'g'),
#        Block(19, 1, 'h'),
#        Block(25, 5, 'i'),
#        Block(26, 0, 'j'),
#        Block(26, 3, 'k'),
#        Block(32, 2, 'l'),
#        Block(34, 3, 'm'),
    ]

