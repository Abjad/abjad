# -*- coding: utf-8 -*-
import os
import platform
from abjad.tools import commandlinetools
from abjad.tools import systemtools
from base import ScorePackageScriptTestCase


class Test(ScorePackageScriptTestCase):

    expected_files = [
        'test_score/test_score/build/.gitignore',
        'test_score/test_score/build/assets/.gitignore',
        'test_score/test_score/build/assets/instrumentation.tex',
        'test_score/test_score/build/assets/performance-notes.tex',
        'test_score/test_score/build/letter-portrait/back-cover.tex',
        'test_score/test_score/build/letter-portrait/front-cover.tex',
        'test_score/test_score/build/letter-portrait/music.ly',
        'test_score/test_score/build/letter-portrait/parts.ly',
        'test_score/test_score/build/letter-portrait/preface.tex',
        'test_score/test_score/build/letter-portrait/score.tex',
        'test_score/test_score/build/parts.ily',
        'test_score/test_score/build/segments.ily',
        'test_score/test_score/build/segments/.gitignore',
        ]

    if platform.system().lower() == 'windows':
        expected_files = [_.replace('/', os.path.sep) for _ in expected_files]

    def test_exists(self):
        self.create_score()
        script = commandlinetools.ManageBuildTargetScript()
        command = ['--new']
        with systemtools.TemporaryDirectoryChange(str(self.score_path)):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
            with systemtools.RedirectedStreams(stdout=self.string_io):
                with self.assertRaises(SystemExit) as context_manager:
                    script(command)
                assert context_manager.exception.code == 1
        self.compare_captured_output(r'''
        Creating build target 'letter-portrait' (8.5in x 11.0in)
            Path exists: test_score/build/letter-portrait
        '''.replace('/', os.path.sep))

    def test_explicit(self):
        self.create_score()
        script = commandlinetools.ManageBuildTargetScript()
        command = [
            '--new',
            '--paper-size', 'a3',
            '--orientation', 'landscape',
            ]
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        self.compare_captured_output(r'''
        Creating build target 'a3-landscape' (297mm x 420mm)
            Reading test_score/metadata.json ... OK!
            Created test_score/build/a3-landscape
        '''.replace('/', os.path.sep))
        path = self.build_path.joinpath('a3-landscape', 'score.tex')
        self.compare_lilypond_contents(path, r'''
            \documentclass{article}
            \usepackage[papersize={420mm, 297mm}]{geometry}
            \usepackage{pdfpages}
            \begin{document}

            \includepdf[pages=-]{front-cover.pdf}
            \includepdf[pages=-]{preface.pdf}
            \includepdf[angle=-90,pages=-]{music.pdf}
            \includepdf[pages=-]{back-cover.pdf}

            \end{document}
        ''')

    def test_force_replace(self):
        self.create_score()
        script = commandlinetools.ManageBuildTargetScript()
        command = ['-f', '--new']
        with systemtools.TemporaryDirectoryChange(str(self.score_path)):
            try:
                script(command)
            except SystemExit:
                raise RuntimeError('SystemExit')
            with systemtools.RedirectedStreams(stdout=self.string_io):
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        self.compare_captured_output(r'''
        Creating build target 'letter-portrait' (8.5in x 11.0in)
            Reading test_score/metadata.json ... OK!
            Created test_score/build/letter-portrait
        '''.replace('/', os.path.sep))

    def test_implicit(self):
        self.create_score()
        script = commandlinetools.ManageBuildTargetScript()
        command = ['--new']
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        self.compare_captured_output(r'''
        Creating build target 'letter-portrait' (8.5in x 11.0in)
            Reading test_score/metadata.json ... OK!
            Created test_score/build/letter-portrait
        '''.replace('/', os.path.sep))
        self.compare_path_contents(self.build_path, self.expected_files)
        path = self.build_path.joinpath('letter-portrait', 'music.ly')
        self.compare_lilypond_contents(path, r'''
            \language "english"

            #(ly:set-option 'relative-includes #t)
            \include "../../stylesheets/stylesheet.ily"

            #(set-default-paper-size "letter" 'portrait)
            #(set-global-staff-size 12)

            \layout {
            }

            \paper {
            }

            \score {
                \include "../segments.ily"
            }
        ''')
        path = self.build_path.joinpath('letter-portrait', 'parts.ly')
        self.compare_lilypond_contents(path, r'''
            \language "english"

            #(ly:set-option 'relative-includes #t)
            \include "../../stylesheets/stylesheet.ily"
            \include "../../stylesheets/parts.ily"

            #(set-default-paper-size "letter" 'portrait)
            #(set-global-staff-size 12)

            \include "../parts.ily"
        ''')
        path = self.build_path.joinpath('letter-portrait', 'score.tex')
        self.compare_lilypond_contents(path, r'''
            \documentclass{article}
            \usepackage[papersize={8.5in, 11.0in}]{geometry}
            \usepackage{pdfpages}
            \begin{document}

            \includepdf[pages=-]{front-cover.pdf}
            \includepdf[pages=-]{preface.pdf}
            \includepdf[angle=0,pages=-]{music.pdf}
            \includepdf[pages=-]{back-cover.pdf}

            \end{document}
        ''')
        path = self.build_path.joinpath('letter-portrait', 'front-cover.tex')
        self.compare_lilypond_contents(path, r"""
        \documentclass[11pt]{report}
        <BLANKLINE>
        \usepackage[T1]{fontenc}
        \usepackage[papersize={8.5in, 11.0in}]{geometry}
        \usepackage{tikz}
        \usepackage{xltxtra,fontspec,xunicode}
        \usetikzlibrary{calc}
        <BLANKLINE>
        %\defaultfontfeatures{Scale=MatchLowercase}
        %\setromanfont[Numbers=Uppercase]{Didot}
        \newlength{\drop}
        \parindent=0pt
        <BLANKLINE>
        \begin{document}
            \begin{titlepage}
        <BLANKLINE>
                \begin{tikzpicture}[remember picture, overlay]
                    \draw[line width = 1.6pt]
                        ($(current page.north west) + (1in,-1in)$)
                        rectangle
                        ($(current page.south east) + (-1in,1in)$);
                    \draw[line width = 0.4pt]
                        ($(current page.north west) + (1in,-1in) + (2.8pt,-2.8pt)$)
                        rectangle
                        ($(current page.south east) + (-1in,1in) + (-2.8pt,2.8pt)$);
                \end{tikzpicture}
        <BLANKLINE>
                \drop=0.1\textheight
                \centering
        <BLANKLINE>
                \vspace*{2\baselineskip}
        <BLANKLINE>
                \rule{\textwidth}{1.6pt}\vspace*{-\baselineskip}\vspace*{2pt}
                \rule{\textwidth}{0.4pt}\\[\baselineskip]
                {
                    \fontsize{6cm}{1em}\selectfont
                    TEST SCORE
                }
                \rule{\textwidth}{0.4pt}\vspace*{-\baselineskip}\vspace{3.2pt}
                \rule{\textwidth}{1.6pt}\\[\baselineskip]
        <BLANKLINE>
                \vspace*{2\baselineskip}
        <BLANKLINE>
                {
                    \itshape
                    Composed by
                }
                \\
                {
                    \Large
                    JOSIAH WOLF OBERHOLTZER
                    \par
                }
        <BLANKLINE>
                \vspace*{2\baselineskip}
        <BLANKLINE>
                {
                    \Large
                    2016
                }
        <BLANKLINE>
                \vfill
        <BLANKLINE>
            \end{titlepage}
        \end{document}
        """)
        path = self.build_path.joinpath('letter-portrait', 'back-cover.tex')
        self.compare_lilypond_contents(path, r'''
        \documentclass[11pt]{report}

        \usepackage[utf8]{inputenc}
        \usepackage{eurosym}
        \usepackage[papersize={8.5in, 11.0in}]{geometry}
        \usepackage{tikz}
        \usepackage{xltxtra,fontspec,xunicode}
        \usetikzlibrary{calc}

        %\defaultfontfeatures{Scale=MatchLowercase}
        %\setromanfont[Numbers=Uppercase]{Didot}

        \begin{document}
            \begin{titlepage}

                \begin{tikzpicture}[remember picture, overlay]
                    \draw[line width = 1.6pt]
                        ($(current page.north west) + (1in,-1in)$)
                        rectangle
                        ($(current page.south east) + (-1in,1in)$);
                    \draw[line width = 0.4pt]
                        ($(current page.north west) + (1in,-1in) + (2.8pt,-2.8pt)$)
                        rectangle
                        ($(current page.south east) + (-1in,1in) + (-2.8pt,2.8pt)$);
                \end{tikzpicture}

                \vfill

                \begin{center}

                \vspace{1em}
                {
                    \itshape
                    Scores available from the composer at\\
                }
                {
                    www.josiahwolfoberholtzer.com\\
                }
                \vspace{1em}
                \euro 750 / \$1000

                \end{center}

            \end{titlepage}
        \end{document}
        ''')

    def test_internal_path(self):
        self.create_score()
        script = commandlinetools.ManageBuildTargetScript()
        command = ['--new']
        internal_path = self.score_path.joinpath('test_score', 'build')
        assert internal_path.exists()
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(internal_path)):
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        self.compare_captured_output(r'''
        Creating build target 'letter-portrait' (8.5in x 11.0in)
            Reading test_score/metadata.json ... OK!
            Created test_score/build/letter-portrait
        '''.replace('/', os.path.sep))

    def test_named(self):
        self.create_score()
        script = commandlinetools.ManageBuildTargetScript()
        command = [
            '--new',
            'World Premiere Version',
            '--paper-size', 'a3',
            '--orientation', 'landscape',
            ]
        with systemtools.RedirectedStreams(stdout=self.string_io):
            with systemtools.TemporaryDirectoryChange(str(self.score_path)):
                try:
                    script(command)
                except SystemExit:
                    raise RuntimeError('SystemExit')
        self.compare_captured_output(r'''
        Creating build target 'world-premiere-version' (297mm x 420mm)
            Reading test_score/metadata.json ... OK!
            Created test_score/build/world-premiere-version
        '''.replace('/', os.path.sep))
