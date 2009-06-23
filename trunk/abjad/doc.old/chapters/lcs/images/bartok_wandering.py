from abjad import *
from abjad.tools import construct

ps = PianoStaff([ ])

s = Staff([ ])
m = RigidMeasure((2, 4), [Note(i, (1, 8)) for i in [9, 7, 5, 4]])
m[0].dynamics = 'pp'
Beam(m)
s.append(m)
m = RigidMeasure((3, 4), construct.notes([2,7,5,4,2], [(1, 4)]+[(1, 8)]*4))
m[1].dynamics = 'mp'
Beam(m[1:])
s.append(m)
m = RigidMeasure((2, 4), 
   construct.notes([0,2,4,5,4], [(1, 8), (1, 16), (1, 16), (1, 8), (1, 8)]))
Beam(m[0:3])
Beam(m[3:])
s.append(m)
m = RigidMeasure((2, 4), [Note(2, (1, 2))])
s.append(m)
m = RigidMeasure((2, 4), [Note(2, (1, 2))])
s.append(m)
Tie(s[-2:])
Slur(s.leaves[0:5])
Slur(s.leaves[5:])
Crescendo(s.leaves[-7:-2])
Decrescendo(s.leaves[-2:])
ts = Text(s.leaves[-7:])
ts.bound_details__left__text = Markup('ritard.')

ps.append(s)

s = Staff([ ])
s.clef = 'bass'
v2 = Voice(construct.notes([-1, 2, 0], [(1, 4), (1, 8), (1, 8)]))
v2[1].dynamics = 'pp'
v2.invocation.name ='v2'
m = RigidMeasure((2, 4), [v2])
s.append(m)
v2 = Voice(construct.notes([-1, -3, -4, 0, -2], 
   [(1, 8), (1, 8), (1, 4), (1, 8), (1, 8)]))
v2[3].dynamics = 'mp'
v2.invocation.name = 'v2'   
m = RigidMeasure((3, 4), [v2])
s.append(m)
v2 = Voice(construct.notes([-3, -5, -6, -5, -3], 
   [(1, 8), (1, 8), (1, 8), (1, 16), (1, 16)]))
v2.invocation.name = 'v2'   
m = RigidMeasure((2, 4), [v2])
s.append(m)
v1a= Voice([Note(-1, (1, 2))])
v1a.invocation.name = 'v1'
v1a.voice.number = 1
v2a= Voice([Note(-1, (1, 4)), Note(-3, (1, 4))])
v2a.invocation.name = 'v2'
v2a.voice.number = 2
m = RigidMeasure((2, 4), [Parallel([v1a, v2a])])
s.append(m)
v1b= Voice([Note(-1, (1, 2))])
v1b.invocation.name = 'v1'
v1b.voice.number = 1
v2b= Voice([Note(-5, (1, 2))])
v2b.invocation.name = 'v2'
v2b.voice.number = 2
m = RigidMeasure((2, 4), [Parallel([v1b, v2b])])
s.append(m)
s.barline = '||'
Tie([v1a[0], v1b[0]])

Beam(s.leaves[1:5])
Beam(s.leaves[6:10])
Beam(s.leaves[10:13])

Slur(s.leaves[1:6])
slr = Slur(s.leaves[6:13] + [v2a, v2b])
slr.position = 'down'

ps.append(s)
print report(ps)
f(ps)
show(ps)
