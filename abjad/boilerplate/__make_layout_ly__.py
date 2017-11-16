#! /usr/bin/env python
import abjad
import baca
import os
import pathlib
import sys
import traceback


if __name__ == '__main__':

    try:
        from layout import layout
        assert isinstance(layout, baca.LayoutMeasureMap), repr(layout)
    except ImportError:
        traceback.print_exc()
        sys.exit(1)

    try:
        file_ = pathlib.Path(os.path.realpath(__file__))
        build_directory = file_.parent
        build_name = build_directory.name
        layout = abjad.new(layout, build=build_name)
    except:
        traceback.print_exc()
        sys.exit(1)
        
    try:
        builds_directory = build_directory.parent
        score_name = builds_directory.parent.name
        score_path = abjad.Path(score_name)
        time_signatures = score_path._segments('time_signatures.py')
        text = time_signatures.read_text()
        exec(text)
        prototype = abjad.TypedOrderedDict
        assert isinstance(time_signatures, prototype), repr(time_signatures)
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        time_signatures_ = []
        for segment_name, strings in time_signatures.items():
            for string in strings:
                time_signature = abjad.TimeSignature.from_string(string)
                time_signatures_.append(time_signature)
        time_signatures = time_signatures_
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        maker = baca.SegmentMaker(
            layout_measure_map=layout,
            omit_empty_start_bar=True,
            omit_stage_number_markup=True,
            score_template=baca.SingleStaffScoreTemplate(),
            time_signatures=time_signatures,
            )
        lilypond_file = maker.run()
        context = lilypond_file['GlobalSkips']
        skips = baca.select(context).skips()
        for skip in skips:
            abjad.detach(abjad.TimeSignature, skip)
        score = lilypond_file['Score']
        del(score['MusicContext'])
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        score = lilypond_file['Score']
        text = format(score)
        text = text.replace('GlobalSkips', 'PageLayout')
        layout_ly = build_directory / 'layout.ly'
        layout_ly.write_text(text)
        print(f'Writing {layout_ly} ...')
    except:
        traceback.print_exc()
        sys.exit(1)

    try:
        break_measures = []
        prototype = (abjad.LineBreak, abjad.PageBreak)
        skips = abjad.iterate(score['GlobalSkips']).leaves(abjad.Skip)
        for i, skip in enumerate(skips):
            if abjad.inspect(skip).has_indicator(prototype):
                measure_number = i + 1
                break_measures.append(measure_number)
        build_metadata = score_path.builds.get_metadatum(build_name)
        build_metadata = build_metadata or abjad.TypedOrderedDict()
        build_metadata['break_measures'] = break_measures
        score_path.builds.add_metadatum(build_name, build_metadata)
        print(f'Writing build metadata ...')
    except:
        traceback.print_exc()
        sys.exit(1)

    sys.exit(0)
