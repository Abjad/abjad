from abjad import *
import py.test


def test__NavigationInterface_is_threadable_01( ):
    '''Voice and leaves all thread.'''

    t = Voice("c'8 d'8 e'8 f'8")

    assert t[0]._navigator._is_threadable(t[1])
    assert t[1]._navigator._is_threadable(t[2])
    assert t[2]._navigator._is_threadable(t[3])

    r'''
    \new Voice {
        c'8
        d'8
        e'8
        f'8
    }
    '''


def test__NavigationInterface_is_threadable_02( ):
    '''Staff and leaves all thread.'''

    t = Staff("c'8 d'8 e'8 f'8")

    assert t[0]._navigator._is_threadable(t[1])
    assert t[1]._navigator._is_threadable(t[2])
    assert t[2]._navigator._is_threadable(t[3])

    r'''
    \new Staff {
        c'8
        d'8
        e'8
        f'8
    }
    '''


def test__NavigationInterface_is_threadable_03( ):
    '''Paths exist between all notes in a sequential.'''

    t = Container("c'8 d'8 e'8 f'8")

    assert t[0]._navigator._is_threadable(t[1])
    assert t[1]._navigator._is_threadable(t[2])
    assert t[2]._navigator._is_threadable(t[3])

    r'''
    {
        c'8
        d'8
        e'8
        f'8
    }
    '''

# NONSTRUCTURAL in new parallel --> context model.
#def test__NavigationInterface_is_threadable_04( ):
#   '''A path does NOT exist between leaves with a parent parallel container
#   not contained inside a Voice (an explicit thread).
#   This parallels LilyPonds behavior of creating a separate Staff for each
#   leaf in this particular case. See the next test.'''
#   # [VA] None... i think.
#   # [Baca] I tend to agree. It certainly doesn't make sense to *span* more than one component within a parallel container. But it occurs to me that _threadale_ means something subtly different than _spannable_. Without thinking through all the cases yes, I'm pretty sure that 'threadability' is a necessary (but not sufficient) condition for 'spanability'. That is, 'spanability' is a special, rarer cases of 'threadability'; or, said the other way around, 'threadability' is a more general phenomenon and 'spanability' is a more specific phenomenon. We should discuss more soon.
#   # [VA] I think the behavior is as follows:
#   # -- No thread exists between leaves with a parallel parent NOT contained
#   # inside a sequential container (implicit thread) or a
#   # Voice (explicit thread). LilyPond interprets this as four
#   # separate Staves, thus four threads.
#   # -- A thread DOES exist between leaves with a parallel parent contained
#   # inside a Voices, because these are interpreted as chords by lilypond.
#   # this is the current implementation behavior as of Apr. 3, 2009.
#   # See the next test.
#
#   t = Container("c'8 d'8 e'8 f'8")
#   t.is_parallel = True
#
#   assert not t[0]._navigator._is_threadable(t[1])
#   assert not t[1]._navigator._is_threadable(t[2])
#   assert not t[2]._navigator._is_threadable(t[3])
#
#   r'''<<
#      c'8
#      d'8
#      e'8
#      f'8
#   >>'''


# NONSTRUCTURAL in new parallel --> context model.
#def test__NavigationInterface_is_threadable_05( ):
#   '''A path DOES exist between leaves with a parent parallel container
#   contained inside a Voice (an explicit thread).
#   This parallels LilyPonds behavior of creating chords.'''
#
#   t = Container("c'8 d'8 e'8 f'8")
#   t.is_parallel = True
#   v = Voice([t])
#
#   assert t[0]._navigator._is_threadable(t[1])
#   assert t[1]._navigator._is_threadable(t[2])
#   assert t[2]._navigator._is_threadable(t[3])
#
#   r'''\new Voice {
#            <<
#               c'8
#               d'8
#               e'8
#               f'8
#            >>
#      }'''


def test__NavigationInterface_is_threadable_06( ):
    '''Tuplets and leaves all thread.'''

    t = tuplettools.FixedDurationTuplet(Duration(2, 8), "c'8 d'8 e'8")

    assert t[0]._navigator._is_threadable(t[1])
    assert t[1]._navigator._is_threadable(t[0])

    assert t[1]._navigator._is_threadable(t[2])
    assert t[2]._navigator._is_threadable(t[1])

    r'''
    \times 2/3 {
        c'8
        d'8
        e'8
    }
    '''


def test__NavigationInterface_is_threadable_07( ):
    '''Voice and its noncontext contents all thread.'''

    t = Voice(Container(notetools.make_repeated_notes(4)) * 2)
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

    r'''
    \new Voice {
        {
            c'8
            d'8
            e'8
            f'8
        }
        {
            g'8
            a'8
            b'8
            c''8
        }
    }
    '''

    assert t[0]._navigator._is_threadable(t[1])
    assert t[1]._navigator._is_threadable(t[0])

    assert t[0]._navigator._is_threadable(t[1][0])
    assert t[0]._navigator._is_threadable(t[1][1])
    assert t[0]._navigator._is_threadable(t[1][2])
    assert t[0]._navigator._is_threadable(t[1][3])
    assert t[1]._navigator._is_threadable(t[0][0])
    assert t[1]._navigator._is_threadable(t[0][1])
    assert t[1]._navigator._is_threadable(t[0][2])
    assert t[1]._navigator._is_threadable(t[0][3])


def test__NavigationInterface_is_threadable_08( ):
    '''Voice and its noncontext contents all thread.'''

    t1 = tuplettools.FixedDurationTuplet(Duration(2, 8), [Note(i, (1, 8)) for i in range(3)])
    t2 = tuplettools.FixedDurationTuplet(Duration(2, 8), [Note(i, (1, 8)) for i in range(3, 6)])
    t = Voice([t1, t2])

    assert t[0]._navigator._is_threadable(t[1])
    assert t[1]._navigator._is_threadable(t[0])

    assert t[0]._navigator._is_threadable(t[1][0])
    assert t[0]._navigator._is_threadable(t[1][1])
    assert t[0]._navigator._is_threadable(t[1][2])
    assert t[1]._navigator._is_threadable(t[0][0])
    assert t[1]._navigator._is_threadable(t[0][1])
    assert t[1]._navigator._is_threadable(t[0][2])

    r'''
    \new Voice {
        \times 2/3 {
            c'8
            cs'8
            d'8
        }
        \times 2/3 {
            ef'8
            e'8
            f'8
        }
    }
    '''


def test__NavigationInterface_is_threadable_09( ):
    '''Can not thread across differently identified anonymous voices.'''

    v1 = Voice([Note(i, (1, 8)) for i in range(4)])
    v2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
    t = Staff([v1, v2])

    assert not t[0]._navigator._is_threadable(t[1])
    assert not t[1]._navigator._is_threadable(t[0])
    assert not t[0][0]._navigator._is_threadable(t[1][0])
    assert not t[1][0]._navigator._is_threadable(t[0][-1])

    assert v1[0]._navigator._is_threadable(v1[1])
    assert v1[1]._navigator._is_threadable(v1[2])
    assert v1[2]._navigator._is_threadable(v1[3])

    assert v2[0]._navigator._is_threadable(v2[1])
    assert v2[1]._navigator._is_threadable(v2[2])
    assert v2[2]._navigator._is_threadable(v2[3])

    r'''
    \new Staff {
        \new Voice {
            c'8
            cs'8
            d'8
            ef'8
        }
        \new Voice {
            e'8
            f'8
            fs'8
            g'8
        }
    }
    '''


def test__NavigationInterface_is_threadable_10( ):
    '''Can thread across like-named voices.'''

    v1 = Voice([Note(i, (1, 8)) for i in range(4)])
    v1.name = 'foo'
    v2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
    v2.name = 'foo'
    t = Staff([v1, v2])

    assert t[0]._navigator._is_threadable(t[1])
    assert t[1]._navigator._is_threadable(t[0])

    assert t[0]._navigator._is_threadable(t[1][0])
    assert t[0]._navigator._is_threadable(t[1][1])
    assert t[0]._navigator._is_threadable(t[1][2])
    assert t[0]._navigator._is_threadable(t[1][3])
    assert t[1]._navigator._is_threadable(t[0][0])
    assert t[1]._navigator._is_threadable(t[0][1])
    assert t[1]._navigator._is_threadable(t[0][2])
    assert t[1]._navigator._is_threadable(t[0][3])

    r'''
    \new Staff {
        \context Voice = "foo" {
            c'8
            cs'8
            d'8
            ef'8
        }
        \context Voice = "foo" {
            e'8
            f'8
            fs'8
            g'8
        }
    }
    '''


def test__NavigationInterface_is_threadable_11( ):
    '''Can not thread across differently named voices.'''

    v1 = Voice([Note(i, (1, 8)) for i in range(4)])
    v1.name = 'foo'
    v2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
    v2.name = 'bar'
    t = Staff([v1, v2])

    assert not t[0]._navigator._is_threadable(t[1])
    assert not t[1]._navigator._is_threadable(t[0])

    r'''
    \new Staff {
        \context Voice = "foo" {
            c'8
            cs'8
            d'8
            ef'8
        }
        \context Voice = "bar" {
            e'8
            f'8
            fs'8
            g'8
        }
    }
    '''


def test__NavigationInterface_is_threadable_12( ):
    '''Can not thread across differently identified anonymous voices.'''

    v1 = Voice([Note(i, (1, 8)) for i in range(4)])
    v2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
    s1 = Staff([v1])
    s2 = Staff([v2])
    seq = Container([s1, s2])

    assert not seq[0]._navigator._is_threadable(seq[1])
    assert not seq[1]._navigator._is_threadable(seq[0])

    assert not seq[0][0]._navigator._is_threadable(seq[1][0])
    assert not seq[1][0]._navigator._is_threadable(seq[0][0])

    assert not seq[0]._navigator._is_threadable(seq[0][0])
    assert not seq[0]._navigator._is_threadable(seq[1][0])
    assert not seq[1]._navigator._is_threadable(seq[0][0])
    assert not seq[1]._navigator._is_threadable(seq[1][0])

    r'''
    {
        \new Staff {
            \new Voice {
                c'8
                cs'8
                d'8
                ef'8
            }
        }
        \new Staff {
            \new Voice {
                e'8
                f'8
                fs'8
                g'8
            }
        }
    }
    '''


def test__NavigationInterface_is_threadable_13( ):
    '''Can not thread across differently identified anonymous voices.'''

    vl1 = Voice([Note(i, (1, 8)) for i in range(4)])
    vl2 = Voice([Note(i, (1, 8)) for i in range(4, 8)])
    vh1 = Voice([Note(i, (1, 8)) for i in range(12, 16)])
    vh2 = Voice([Note(i, (1, 8)) for i in range(16, 20)])
    s1 = Staff([vh1, vl1])
    s1.is_parallel = True
    s2 = Staff([vl2, vh2])
    s2.is_parallel = True
    seq = Container([s1, s2])

    assert not seq[0]._navigator._is_threadable(seq[1])
    assert not seq[0]._navigator._is_threadable(seq[1][0])
    assert not seq[0]._navigator._is_threadable(seq[1][0][0])
    assert not seq[0]._navigator._is_threadable(seq[1][1])
    assert not seq[0]._navigator._is_threadable(seq[1][1][0])

    assert not seq[0][0]._navigator._is_threadable(seq[1])
    assert not seq[0][0]._navigator._is_threadable(seq[1][0])
    assert not seq[0][0]._navigator._is_threadable(seq[1][0][0])
    assert not seq[0][0]._navigator._is_threadable(seq[1][1])
    assert not seq[0][0]._navigator._is_threadable(seq[1][1][0])

    assert not seq[0][0][-1]._navigator._is_threadable(seq[1])
    assert not seq[0][0][-1]._navigator._is_threadable(seq[1][0])
    assert not seq[0][0][-1]._navigator._is_threadable(seq[1][0][0])
    assert not seq[0][0][-1]._navigator._is_threadable(seq[1][1])
    assert not seq[0][0][-1]._navigator._is_threadable(seq[1][1][0])

    assert not seq[0][1]._navigator._is_threadable(seq[1])
    assert not seq[0][1]._navigator._is_threadable(seq[1][0])
    assert not seq[0][1]._navigator._is_threadable(seq[1][0][0])
    assert not seq[0][1]._navigator._is_threadable(seq[1][1])
    assert not seq[0][1]._navigator._is_threadable(seq[1][1][0])

    assert not seq[0][1][-1]._navigator._is_threadable(seq[1])
    assert not seq[0][1][-1]._navigator._is_threadable(seq[1][0])
    assert not seq[0][1][-1]._navigator._is_threadable(seq[1][0][0])
    assert not seq[0][1][-1]._navigator._is_threadable(seq[1][1])
    assert not seq[0][1][-1]._navigator._is_threadable(seq[1][1][0])

    r'''
    {
        \new Staff <<
            \new Voice {
                c''8
                cs''8
                d''8
                ef''8
            }
            \new Voice {
                c'8
                cs'8
                d'8
                ef'8
            }
        >>
        \new Staff <<
            \new Voice {
                e'8
                f'8
                fs'8
                g'8
            }
            \new Voice {
                e''8
                f''8
                fs''8
                g''8
            }
        >>
    }
    '''


def test__NavigationInterface_is_threadable_14( ):
    '''Voice threads its noncontext contents.'''

    s1 = Container([Note(i, (1, 8)) for i in range(4)])
    s1 = Container([s1])
    s2 = Container([Note(i, (1, 8)) for i in range(4, 8)])
    s2 = Container([s2])
    t = Voice([s1, s2])

    r'''
    \new Voice {
        {
            {
                c'8
                cs'8
                d'8
                ef'8
            }
        }
        {
            {
                e'8
                f'8
                fs'8
                g'8
            }
        }
    }
    '''

    assert t[0]._navigator._is_threadable(t[1])
    assert t[0]._navigator._is_threadable(t[1][0])
    assert t[0]._navigator._is_threadable(t[1][0][0])

    assert t[0][0]._navigator._is_threadable(t[1])
    assert t[0][0]._navigator._is_threadable(t[1][0])
    assert t[0][0]._navigator._is_threadable(t[1][0][0])

    assert t[0][0][-1]._navigator._is_threadable(t[1])
    assert t[0][0][-1]._navigator._is_threadable(t[1][0])
    assert t[0][0][-1]._navigator._is_threadable(t[1][0][0])


def test__NavigationInterface_is_threadable_15( ):
    '''Like-named staves do NOT thread.'''

    t = Container(Staff([ ]) * 2)
    t[0].name = 'foo'
    t[1].name = 'foo'

    r'''
    {
        \context Staff = "foo" {
        }
        \context Staff = "foo" {
        }
    }
    '''

    assert not t[0]._navigator._is_threadable(t[1])
    assert not t[1]._navigator._is_threadable(t[0])


def test__NavigationInterface_is_threadable_16( ):
    '''Can NOT thread across like-named voices in like-named staves.'''

    t = Container(Staff([Voice(notetools.make_repeated_notes(4))]) * 2)
    t[0].name = 'staff'
    t[0][0].name = 'voice'
    t[1].name = 'staff'
    t[1][0].name = 'voice'
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

    r'''
    {
        \context Staff = "staff" {
            \context Voice = "voice" {
                c'8
                d'8
                e'8
                f'8
            }
        }
        \context Staff = "staff" {
            \context Voice = "voice" {
                g'8
                a'8
                b'8
                c''8
            }
        }
    }
    '''

    leaves = t.leaves

    assert leaves[0]._navigator._is_threadable(leaves[1])
    assert leaves[4]._navigator._is_threadable(leaves[7])
    assert not leaves[0]._navigator._is_threadable(leaves[4])
    assert not leaves[4]._navigator._is_threadable(leaves[0])


def test__NavigationInterface_is_threadable_17( ):
    '''Can thread across like-named voices.
        But can NOT thread across differently identified anonymous staves.'''

    t = Container(Staff([Voice(notetools.make_repeated_notes(4))]) * 2)
    t[0][0].name = 'voice'
    t[1][0].name = 'voice'
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

    r'''
    {
        \new Staff {
            \context Voice = "voice" {
                c'8
                d'8
                e'8
                f'8
            }
        }
        \new Staff {
            \context Voice = "voice" {
                g'8
                a'8
                b'8
                c''8
            }
        }
    }
    '''

    leaves = t.leaves

    assert leaves[0]._navigator._is_threadable(leaves[1])
    assert not leaves[0]._navigator._is_threadable(leaves[4])

    assert not leaves[4]._navigator._is_threadable(leaves[0])
    assert leaves[4]._navigator._is_threadable(leaves[7])


def test__NavigationInterface_is_threadable_18( ):
    '''Like-named voices thread.'''

    t = Container(Voice(notetools.make_repeated_notes(4)) * 2)
    t[0].name = 'foo'
    t[1].name = 'foo'
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

    r'''
    {
        \context Voice = "foo" {
            c'8
            d'8
            e'8
            f'8
        }
        \context Voice = "foo" {
            g'8
            a'8
            b'8
            c''8
        }
    }
    '''

    assert t[0]._navigator._is_threadable(t[1])
    assert t[1]._navigator._is_threadable(t[0])

    assert t[0][0]._navigator._is_threadable(t[1][0])
    assert t[1][0]._navigator._is_threadable(t[0][1])


def test__NavigationInterface_is_threadable_19( ):
    '''Can not thread from differently identified
        anonymous and implicit voices.'''

    t = Staff(notetools.make_repeated_notes(4))
    t.insert(2, Voice(notetools.make_repeated_notes(2)))
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

    r'''
    \new Staff {
        c'8
        d'8
        \new Voice {
            e'8
            f'8
        }
        g'8
        a'8
    }
    '''

    assert t[0]._navigator._is_threadable(t[1])
    assert not t[0]._navigator._is_threadable(t[2][0])
    assert t[0]._navigator._is_threadable(t[3])

    assert not t[2][0]._navigator._is_threadable(t[0])
    assert t[2][0]._navigator._is_threadable(t[2][1])
    assert not t[2][0]._navigator._is_threadable(t[3])


def test__NavigationInterface_is_threadable_20( ):
    '''Like-named voices thread.'''

    v1 = Voice(notetools.make_repeated_notes(4))
    v2 = Voice(notetools.make_repeated_notes(4))
    v1.name = v2.name = 'voiceOne'
    t = Container([v1, v2])
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

    r'''
        {
            \context Voice = "voiceOne" {
                c'8
                d'8
                e'8
                f'8
            }
            \context Voice = "voiceOne" {
                g'8
                a'8
                b'8
                c''8
            }
        }
    '''
    assert v1._navigator._is_threadable(v2)
    for n1, n2 in zip(t.leaves[0:-1], t.leaves[1:]):
        assert n1._navigator._is_threadable(n2)


def test__NavigationInterface_is_threadable_21( ):
    '''Like-named voices thread.'''

    v1 = Voice(notetools.make_repeated_notes(4))
    v2 = Voice(notetools.make_repeated_notes(4))
    v1.name = v2.name = 'voiceOne'
    t = Container([Container([v1]), Container([v2])])
    t[0].is_parallel = True
    t[1].is_parallel = True
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

    r'''
    {
        <<
            \context Voice = "voiceOne" {
                c'8
                d'8
                e'8
                f'8
            }
        >>
        <<
            \context Voice = "voiceOne" {
                g'8
                a'8
                b'8
                c''8
            }
        >>
    }
    '''

    assert v1._navigator._is_threadable(v2)
    for n1, n2 in zip(t.leaves[0:-1], t.leaves[1:]):
        assert n1._navigator._is_threadable(n2)


def test__NavigationInterface_is_threadable_22( ):
    '''Like-named voices in like-named staves do NOT thread.'''

    v1 = Voice(notetools.make_repeated_notes(4))
    v2 = Voice(notetools.make_repeated_notes(4))
    v1.name = v2.name = 'voiceOne'
    s1 = Staff([v1])
    s2 = Staff([v2])
    s1.name = s2.name = 'staffOne'
    s1.is_parallel = True
    s2.is_parallel = True
    t = Container([s1, s2])
    pitchtools.set_ascending_named_diatonic_pitches_on_nontied_pitched_components_in_expr(t)

    r'''
    {
        \context Staff = "staffOne" <<
            \context Voice = "voiceOne" {
                c'8
                d'8
                e'8
                f'8
            }
        >>
        \context Staff = "staffOne" <<
            \context Voice = "voiceOne" {
                g'8
                a'8
                b'8
                c''8
            }
        >>
    }
    '''

    assert not v1._navigator._is_threadable(v2)
    assert not s1._navigator._is_threadable(s2)


def test__NavigationInterface_is_threadable_23( ):
    '''Like-name staff groups thread.'''

    t = Container([scoretools.StaffGroup([ ]), scoretools.StaffGroup([ ])])
    t[0].name = t[1].name = 'staffGroup'

    r'''
    {
        \context StaffGroup = "staffGroup" <<
        >>
        \context StaffGroup = "staffGroup" <<
        >>
    }
    '''

    assert t[0]._navigator._is_threadable(t[1])


def test__NavigationInterface_is_threadable_24( ):
    r'''Containers and leaves here all inhabit the same implicit voice.
        All components thread.'''

    t = Container(Container(notetools.make_repeated_notes(4)) * 2)
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)

    assert t[0][-1]._navigator._is_threadable(t[1][0])
    assert t[1][0]._navigator._is_threadable(t[0][-1])

    r'''
    {
        {
            c'8
            cs'8
            d'8
            ef'8
        }
        {
            e'8
            f'8
            fs'8
            g'8
        }
    }
    '''


def test__NavigationInterface_is_threadable_25( ):
    '''Differently identified anonymous voices do not thread.'''

    t = Container(Voice(notetools.make_repeated_notes(4)) * 2)
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)

    assert not t[0][-1]._navigator._is_threadable(t[1][0])
    assert not t[1][0]._navigator._is_threadable(t[0][-1])

    r'''
    {
        \new Voice {
            c'8
            cs'8
            d'8
            ef'8
        }
        \new Voice {
            e'8
            f'8
            fs'8
            g'8
        }
    }
    '''


def test__NavigationInterface_is_threadable_26( ):
    '''Differently identified anonymous voices do not thread.
        Differently identified anonymous staves do not thread.'''

    t = Container(Staff([Voice(notetools.make_repeated_notes(4))]) * 2)
    pitchtools.set_ascending_named_chromatic_pitches_on_nontied_pitched_components_in_expr(t)

    assert not t[0][0][-1]._navigator._is_threadable(t[1][0][0])
    assert not t[1][0][0]._navigator._is_threadable(t[0][0][-1])

    assert not t[0][0]._navigator._is_threadable(t[1][0])
    assert not t[1][0]._navigator._is_threadable(t[0][0])

    assert not t[0]._navigator._is_threadable(t[1])
    assert t[0]._navigator._is_threadable(t[0])

    r'''
    {
        \new Staff {
            \new Voice {
                c'8
                cs'8
                d'8
                ef'8
            }
        }
        \new Staff {
            \new Voice {
                e'8
                f'8
                fs'8
                g'8
            }
        }
    }
    '''
