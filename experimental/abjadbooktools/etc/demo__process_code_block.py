from abjad.tools import *
from experimental import *


pipe = documentationtools.Pipe()

lines = '''from abjad import *

staff = Staff("c d e f")
show(staff)

def foo(x):
    print "FOO BAR"
    return 3 * x

print foo(4)'''.split('\n')

result = pipe.read_wait().split('\n')
result = []
result.extend(abjadbooktools.process_code_block(pipe, lines, image_count=0, hide_prompt=False)[0])

for line in result:
    print '+++ {}'.format(line)

