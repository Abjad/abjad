# -*- encoding: utf-8 -*-
from abjad import *
from red_example_score.materials.magic_numbers.output import magic_numbers


numerators = magic_numbers[:8]
numerators = [_ % 11 + 1 for _ in numerators]
pairs = [(_, 8) for _ in numerators]
time_signatures = [TimeSignature(_) for _ in pairs]