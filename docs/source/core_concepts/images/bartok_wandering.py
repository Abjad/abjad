import abjad

piano_staff = abjad.StaffGroup(lilypond_type="PianoStaff")

upper_staff = abjad.Staff()
lower_staff = abjad.Staff()

piano_staff.append(upper_staff)
piano_staff.append(lower_staff)

m1 = abjad.Measure((2, 4), [])
m2 = abjad.Measure((3, 4), [])
m3 = abjad.Measure((2, 4), [])
m4 = abjad.Measure((2, 4), [])
m5 = abjad.Measure((2, 4), [])
upper_measures = [m1, m2, m3, m4, m5]
lower_measures = scoretools.copy_components_and_covered_spanners(upper_measures)

upper_staff.extend(upper_measures)
lower_staff.extend(lower_measures)

# add notes to upper measures

upper_measures[0].extend([abjad.Note(i, (1, 8)) for i in [9, 7, 5, 4]])
upper_measures[1].extend(
    scoretools.make_notes([2, 7, 5, 4, 2], [(1, 4)] + [(1, 8)] * 4)
)
notes = scoretools.make_notes(
    [0, 2, 4, 5, 4], [(1, 8), (1, 16), (1, 16), (1, 8), (1, 8)]
)
upper_measures[2].extend(notes)
upper_measures[3].append(abjad.Note(2, (1, 2)))
upper_measures[4].append(abjad.Note(2, (1, 2)))


# add notes to lower measures

v2 = abjad.Voice(scoretools.make_notes([-1, 2, 0], [(1, 4), (1, 8), (1, 8)]))
v2[1].dynamics.mark = "pp"
v2.name = "v2"
lower_measures[0].append(v2)

v2 = abjad.Voice(
    scoretools.make_notes([-1, -3, -4, 0, -2], [(1, 8), (1, 8), (1, 4), (1, 8), (1, 8)])
)
v2[3].dynamics.mark = "mp"
v2.name = "v2"
lower_measures[1].append(v2)

v2 = Voice(
    scoretools.make_notes(
        [-3, -5, -6, -5, -3], [(1, 8), (1, 8), (1, 8), (1, 16), (1, 16)]
    )
)
v2.name = "v2"
lower_measures[2].append(v2)


v1a = Voice([Note(-1, (1, 2))])
v1a.name = "v1"
v1a.voice.number = 1
v2a = Voice([Note(-1, (1, 4)), Note(-3, (1, 4))])
v2a.name = "v2"
v2a.voice.number = 2
p = Container([v1a, v2a])
p.simultaneous = True
lower_measures[3].append(p)

v1b = Voice([Note(-1, (1, 2))])
v1b.name = "v1"
v1b.voice.number = 1
v2b = Voice([Note(-5, (1, 2))])
v2b.name = "v2"
v2b.voice.number = 2

p = Container([v1b, v2b])
p.simultaneous = True
lower_measures[4].append(p)

# embelish
# upper staff

upper_measures[0][0].dynamics.mark = "pp"
abjad.Beam(upper_measures[0])

upper_measures[1][1].dynamics.mark = "mp"
abjad.Beam(upper_measures[1][1:])

abjad.Beam(upper_measures[2][0:3])
abjad.Beam(upper_measures[2][3:])

abjad.Tie(upper_staff[-2:])
abjad.Slur(upper_staff.leaves[0:5])
abjad.Slur(upper_staff.leaves[5:])
abjad.Crescendo(upper_staff.leaves[-7:-2])
abjad.Decrescendo(upper_staff.leaves[-2:])
tx = abjad.Text(upper_staff.leaves[-7:])
tx.bound_details__left__text = abjad.Markup("ritard.")

# lower staff

lower_staff.clef.forced = abjad.Clef("bass")

abjad.Tie([v1a[0], v1b[0]])

abjad.Beam(lower_staff.leaves[1:5])
abjad.Beam(lower_staff.leaves[6:10])
abjad.Beam(lower_staff.leaves[10:13])

abjad.Slur(lower_staff.leaves[1:6])
slr = abjad.Slur(lower_staff.leaves[6:13] + [v2a, v2b])
slr.position = Down

lower_staff.barline.kind = "||"

f(piano_staff)
show(piano_staff)
