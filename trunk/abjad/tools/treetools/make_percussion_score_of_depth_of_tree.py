from abjad import *
from abjad.tools.treetools import *


def make_percussion_score_from_depth_tree(depth_tree):
    
    assert all_bounded_intervals_contain_key_of_klass(depth_tree, 'depth', int)
