import abjad


def test_spannertools_Spanner__apply_overrides_01():

    overrides = {
        'text_spanner__dash_period': '1.5',
        'text_spanner__bound_details__right_broken__padding': '0',
        'text_spanner__bound_details__left_broken__text': "markuptools.Markup((markuptools.MarkupCommand('italic','(fl.)'),markuptools.MarkupCommand('hspace',1)))",
        'text_spanner__bound_details__left__stencil_align_dir_y': '0',
        'text_spanner__bound_details__right__text': "markuptools.Markup((markuptools.MarkupCommand('draw-line',schemetools.SchemePair((0, -1))),))",
        'text_spanner__bound_details__right_broken__text': 'None',
        'text_spanner__bound_details__right__padding': '1',
        'text_spanner__bound_details__left__padding': '-1',
        'text_spanner__dash_fraction': '0.25',
    }

    overrides['text_spanner__bound_details__left__text'] = \
        "markuptools.Markup((markuptools.MarkupCommand('italic','“white” flautando'),markuptools.MarkupCommand('hspace',1)))"

    white_flautando_spanner = abjad.TextSpanner(overrides=overrides)

    staff = abjad.Staff("c'4 d'4 e'4 f'4")
    abjad.attach(white_flautando_spanner, staff[:])

    assert format(staff) == abjad.String.normalize(
        r'''
        \new Staff {
            \override TextSpanner.bound-details.left-broken.text = \markup {
                \italic
                    (fl.)
                \hspace
                    #1
                }
            \override TextSpanner.bound-details.left.padding = #'-1
            \override TextSpanner.bound-details.left.stencil-align-dir-y = #'0
            \override TextSpanner.bound-details.left.text = \markup {
                \italic
                    "“white” flautando"
                \hspace
                    #1
                }
            \override TextSpanner.bound-details.right-broken.padding = #'0
            \override TextSpanner.bound-details.right-broken.text = #'None
            \override TextSpanner.bound-details.right.padding = #'1
            \override TextSpanner.bound-details.right.text = \markup {
                \draw-line
                    #'(0 . -1)
                }
            \override TextSpanner.dash-fraction = #'0.25
            \override TextSpanner.dash-period = #'1.5
            c'4 \startTextSpan
            d'4
            e'4
            \revert TextSpanner.bound-details
            \revert TextSpanner.dash-fraction
            \revert TextSpanner.dash-period
            f'4 \stopTextSpan
        }
        '''
        ), format(staff)
