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
      BoundedInterval(26, 29, 'j'),
      BoundedInterval(32, 34, 'k'),
      BoundedInterval(34, 37, 'l'),
   ]
