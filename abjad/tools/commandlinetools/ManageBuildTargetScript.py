# -*- coding: utf-8 -*-
from __future__ import print_function
import collections
import os
import shutil
import subprocess
import sys
from abjad.tools import stringtools
from abjad.tools import systemtools
from abjad.tools.commandlinetools.ScorePackageScript import ScorePackageScript


class ManageBuildTargetScript(ScorePackageScript):
    '''
    Manages score package build target.

    ..  shell::

        ajv target --help

    '''

    ### CLASS VARIABLES ###

    alias = 'build'
    short_description = 'Manage score package build targets.'

    paper_sizes = collections.OrderedDict([
        ('a10', ((26, 'mm'), (37, 'mm'))),
        ('a9', ((37, 'mm'), (52, 'mm'))),
        ('a8', ((52, 'mm'), (74, 'mm'))),
        ('a7', ((74, 'mm'), (105, 'mm'))),
        ('a6', ((105, 'mm'), (148, 'mm'))),
        ('a5', ((148, 'mm'), (210, 'mm'))),
        ('a4', ((210, 'mm'), (297, 'mm'))),
        ('a3', ((297, 'mm'), (420, 'mm'))),
        ('a2', ((420, 'mm'), (594, 'mm'))),
        ('a1', ((594, 'mm'), (841, 'mm'))),
        ('a0', ((841, 'mm'), (1189, 'mm'))),
        ('b10', ((31, 'mm'), (44, 'mm'))),
        ('b9', ((44, 'mm'), (62, 'mm'))),
        ('b8', ((62, 'mm'), (88, 'mm'))),
        ('b7', ((88, 'mm'), (125, 'mm'))),
        ('b6', ((125, 'mm'), (176, 'mm'))),
        ('b5', ((176, 'mm'), (250, 'mm'))),
        ('b4', ((250, 'mm'), (353, 'mm'))),
        ('b3', ((353, 'mm'), (500, 'mm'))),
        ('b2', ((500, 'mm'), (707, 'mm'))),
        ('b1', ((707, 'mm'), (1000, 'mm'))),
        ('b0', ((1000, 'mm'), (1414, 'mm'))),
        # Below are two extended sizes defined in Din 476
        ('4a0', ((1682, 'mm'), (2378, 'mm'))),
        ('2a0', ((1189, 'mm'), (1682, 'mm'))),
        # Below are ISO 269 standard C series
        ('c10', ((28, 'mm'), (40, 'mm'))),
        ('c9', ((40, 'mm'), (57, 'mm'))),
        ('c8', ((57, 'mm'), (81, 'mm'))),
        ('c7', ((81, 'mm'), (114, 'mm'))),
        ('c6', ((114, 'mm'), (162, 'mm'))),
        ('c5', ((162, 'mm'), (229, 'mm'))),
        ('c4', ((229, 'mm'), (324, 'mm'))),
        ('c3', ((324, 'mm'), (458, 'mm'))),
        ('c2', ((458, 'mm'), (648, 'mm'))),
        ('c1', ((648, 'mm'), (917, 'mm'))),
        ('c0', ((917, 'mm'), (1297, 'mm'))),
        # Below are North American paper sizes
        ('junior-legal', ((8.0, 'in'), (5.0, 'in'))),
        ('legal', ((8.5, 'in'), (14.0, 'in'))),
        ('letter', ((8.5, 'in'), (11.0, 'in'))),
        # Ledger (17x11) is a 90 degree rotation of Tabloid
        ('17x11', ((17.0, 'in'), (11.0, 'in'))),
        ('ledger', ((17.0, 'in'), (11.0, 'in'))),
        # Tabloid (11x17)
        ('11x17', ((11.0, 'in'), (17.0, 'in'))),
        ('tabloid', ((11.0, 'in'), (17.0, 'in'))),
        # government-letter by IEEE Printer Working Group),
        # for children's writing
        ('government-letter', ((8, 'in'), (10.5, 'in'))),
        ('government-legal', ((8.5, 'in'), (13.0, 'in'))),
        ('philippine-legal', ((8.5, 'in'), (13.0, 'in'))),
        # ANSI sizes
        ('ansi a', ((8.5, 'in'), (11.0, 'in'))),
        ('ansi b', ((17.0, 'in'), (11.0, 'in'))),
        ('ansi c', ((17.0, 'in'), (22.0, 'in'))),
        ('ansi d', ((22.0, 'in'), (34.0, 'in'))),
        ('ansi e', ((34.0, 'in'), (44.0, 'in'))),
        ('engineering f', ((28.0, 'in'), (40.0, 'in'))),
        # G and H are very rare, and the lengths are variable up to 90 inches
        # North American Architectural sizes
        ('arch a', ((9.0, 'in'), (12.0, 'in'))),
        ('arch b', ((12.0, 'in'), (18.0, 'in'))),
        ('arch c', ((18.0, 'in'), (24.0, 'in'))),
        ('arch d', ((24.0, 'in'), (36.0, 'in'))),
        ('arch e', ((36.0, 'in'), (48.0, 'in'))),
        ('arch e1', ((30.0, 'in'), (42.0, 'in'))),
        # Other sizes
        # Some are antique sizes which are still using in UK
        ('statement', ((5.5, 'in'), (8.5, 'in'))),
        ('half letter', ((5.5, 'in'), (8.5, 'in'))),
        ('quarto', ((8.0, 'in'), (10.0, 'in'))),
        ('octavo', ((6.75, 'in'), (10.5, 'in'))),
        ('executive', ((7.25, 'in'), (10.5, 'in'))),
        ('monarch', ((7.25, 'in'), (10.5, 'in'))),
        ('foolscap', ((8.27, 'in'), (13.0, 'in'))),
        ('folio', ((8.27, 'in'), (13.0, 'in'))),
        ('super-b', ((13.0, 'in'), (19.0, 'in'))),
        ('post', ((15.5, 'in'), (19.5, 'in'))),
        ('crown', ((15.0, 'in'), (20.0, 'in'))),
        ('large post', ((16.5, 'in'), (21.0, 'in'))),
        ('demy', ((17.5, 'in'), (22.5, 'in'))),
        ('medium', ((18.0, 'in'), (23.0, 'in'))),
        ('broadsheet', ((18.0, 'in'), (24.0, 'in'))),
        ('royal', ((20.0, 'in'), (25.0, 'in'))),
        ('elephant', ((23.0, 'in'), (28.0, 'in'))),
        ('double demy', ((22.5, 'in'), (35.0, 'in'))),
        ('quad demy', ((35.0, 'in'), (45.0, 'in'))),
        ('atlas', ((26.0, 'in'), (34.0, 'in'))),
        ('imperial', ((22.0, 'in'), (30.0, 'in'))),
        ('antiquarian', ((31.0, 'in'), (53.0, 'in'))),
        # PA4 based sizes
        ('pa0', ((840, 'mm'), (1120, 'mm'))),
        ('pa1', ((560, 'mm'), (840, 'mm'))),
        ('pa2', ((420, 'mm'), (560, 'mm'))),
        ('pa3', ((280, 'mm'), (420, 'mm'))),
        ('pa4', ((210, 'mm'), (280, 'mm'))),
        ('pa5', ((140, 'mm'), (210, 'mm'))),
        ('pa6', ((105, 'mm'), (140, 'mm'))),
        ('pa7', ((70, 'mm'), (105, 'mm'))),
        ('pa8', ((52, 'mm'), (70, 'mm'))),
        ('pa9', ((35, 'mm'), (52, 'mm'))),
        ('pa10', ((26, 'mm'), (35, 'mm'))),
        # F4 used in southeast Asia and Australia
        ('f4', ((210, 'mm'), (330, 'mm'))),
        ])

    ### PRIVATE METHODS ###

    def _cleanup_latex_ephemera(self, build_target_path):
        ephemera = [
            '.aux',
            '.log',
            '.out',
            ]
        for path in sorted(build_target_path.glob('*')):
            if path.is_file() and path.suffix in ephemera:
                path.unlink()

    def _handle_create(
        self,
        target_name,
        force,
        paper_size=None,
        orientation=None,
        ):
        from abjad import abjad_configuration
        if target_name is True:
            name = paper_size.lower().replace(' ', '-')
            name = '{}-{}'.format(name, orientation)
        else:
            name = stringtools.to_dash_case(target_name)
        dimensions = self.paper_sizes[paper_size]
        message = 'Creating build target {!r} ({}{} x {}{})'.format(
            name,
            dimensions[0][0], dimensions[0][1],
            dimensions[1][0], dimensions[1][1],
            )
        print(message)
        target_path = self._name_to_score_subdirectory_path(
            name, 'build', self._score_package_path)
        if target_path.exists() and not force:
            print('    Path exists: {!s}'.format(
                target_path.relative_to(self._score_package_path.parent)))
            sys.exit(1)
        metadata = self._read_score_metadata_json(self._score_package_path)
        metadata['score_package_name'] = self._score_package_path.name
        if orientation == 'portrait':
            rotation = 0
            width, height = self.paper_sizes[paper_size]
        else:
            rotation = -90
            height, width = self.paper_sizes[paper_size]
        metadata['rotation'] = rotation
        metadata['orientation'] = orientation
        metadata['paper_size'] = paper_size
        metadata['height'] = height[0]
        metadata['width'] = width[0]
        metadata['unit'] = height[1]
        metadata['global_staff_size'] = 12
        metadata['uppercase_composer_name'] = metadata['composer_name'].upper()
        metadata['uppercase_title'] = metadata['title'].upper()
        metadata['lilypond_version'] = \
            abjad_configuration.get_lilypond_version_string()
        source_name = 'example_build_target'
        source_path = self._get_boilerplate_path().joinpath(source_name)
        suffixes = ('.py', '.tex', '.ly', '.ily')
        for path in self._copy_tree(source_path, target_path):
            if path.is_file() and path.suffix in suffixes:
                self._template_file(path, **metadata)
        print('    Created {!s}'.format(target_path.relative_to(
            self._score_repository_path)))

    def _handle_distribute(self, build_target_name):
        print('Distributing {!r}'.format(build_target_name))
        target_names = [
            path.name for path in self._build_path.glob('*')
            if path.is_dir() and path.name not in ('assets', 'segments')
            ]
        if build_target_name not in target_names:
            print('    Invalid build target!')
            sys.exit(1)
        source_path = self._build_path.joinpath(build_target_name)
        target_path = self._distribution_path.joinpath(build_target_name)
        if target_path.exists():
            shutil.rmtree(str(target_path))
        target_path.mkdir(parents=True)
        score_path = source_path.joinpath('score.pdf')
        if score_path.exists():
            source_name = 'score.pdf'
            target_name = '{}-score.pdf'.format(build_target_name)
            shutil.copyfile(
                str(source_path.joinpath(source_name)),
                str(target_path.joinpath(target_name)),
                )
            print('    {} --> {}'.format(source_name, target_name))
        for parts_path in source_path.glob('part*.pdf'):
            source_name = parts_path.name
            target_name = '{}-{}'.format(build_target_name, source_name)
            shutil.copyfile(
                str(source_path.joinpath(source_name)),
                str(target_path.joinpath(target_name)),
                )
            print('    {} --> {}'.format(source_name, target_name))
        #archive_path = self._distribution_path.joinpath(target_name + '.zip')
        #if archive_path.exists():
        #    shutil.rmtree(str(archive_path))

    def _handle_list(self):
        paths = sorted(
            path for path in self._build_path.glob('*')
            if path.is_dir() and path.name not in ('assets', 'segments')
            )
        print('Available build targets:')
        for path in paths:
            print('    {}'.format(path.name))

    def _handle_render(
        self,
        target_name,
        render_back_cover=None,
        render_front_cover=None,
        render_music=None,
        render_parts=None,
        render_preface=None,
        render_score=None,
        ):
        build_target_path = self._build_path.joinpath(target_name)
        if not build_target_path.exists():
            print('No build target found: {!r}.'.format(target_name))
            sys.exit(1)
        paths_to_open = []
        open_score_only = False
        if not any([
            render_back_cover,
            render_front_cover,
            render_music,
            render_parts,
            render_preface,
            render_score,
            ]):
            render_back_cover = True
            render_front_cover = True
            render_music = True
            render_parts = True
            render_preface = True
            render_score = True
            open_score_only = True
        if render_music:
            path = self._render_music(build_target_path)
            paths_to_open.append(path)
        if render_parts:
            path = self._render_parts(build_target_path)
            paths_to_open.append(path)
        if render_preface:
            path = self._render_preface(build_target_path)
            paths_to_open.append(path)
        if render_front_cover:
            path = self._render_front_cover(build_target_path)
            paths_to_open.append(path)
        if render_back_cover:
            path = self._render_back_cover(build_target_path)
            paths_to_open.append(path)
        if render_score:
            path = self._render_score(build_target_path)
            paths_to_open.append(path)
        if any([
            render_preface,
            render_score,
            render_front_cover,
            render_back_cover,
            ]):
            self._cleanup_latex_ephemera(build_target_path)
        if open_score_only:
            paths_to_open = [build_target_path.joinpath('score.pdf')]
        for path in paths_to_open:
            systemtools.IOManager.open_file(str(path))

    def _process_args(self, args):
        self._setup_paths(args.score_path)
        if args.distribute:
            self._handle_distribute(args.distribute)
        if args.list_:
            self._handle_list()
        if args.new:
            self._handle_create(
                force=args.force,
                orientation=args.orientation,
                paper_size=args.paper_size,
                target_name=args.new,
                )
        if args.render:
            self._handle_render(
                render_back_cover=args.back_cover,
                render_front_cover=args.front_cover,
                render_music=args.music,
                render_parts=args.parts,
                render_preface=args.preface,
                render_score=args.score,
                target_name=args.render,
                )

    def _render_back_cover(self, build_target_path):
        path = build_target_path.joinpath('back-cover.tex')
        print('Rendering {!s}'.format(path.relative_to(self._score_package_path)))
        if not path.is_file():
            print('    Missing: {!s}'.format(path.relative_to(self._score_package_path)))
            sys.exit(1)
        return self._run_latex(path)

    def _render_front_cover(self, build_target_path):
        path = build_target_path.joinpath('front-cover.tex')
        print('Rendering {!s}'.format(path.relative_to(self._score_package_path)))
        if not path.is_file():
            print('    Missing: {!s}'.format(path.relative_to(self._score_package_path)))
            sys.exit(1)
        return self._run_latex(path)

    def _render_music(self, build_target_path):
        path = build_target_path.joinpath('music.ly')
        print('Rendering {!s}'.format(path.relative_to(self._score_package_path)))
        if not path.is_file():
            print('    Missing: {!s}'.format(path.relative_to(self._score_package_path)))
            sys.exit(1)
        return self._run_lilypond(path)

    def _render_parts(self, build_target_path):
        path = build_target_path.joinpath('parts.ly')
        print('Rendering {!s}'.format(path.relative_to(self._score_package_path)))
        if not path.is_file():
            print('    Missing: {!s}'.format(path.relative_to(self._score_package_path)))
            sys.exit(1)
        return self._run_lilypond(path)

    def _render_preface(self, build_target_path):
        path = build_target_path.joinpath('preface.tex')
        print('Rendering {!s}'.format(path.relative_to(self._score_package_path)))
        if not path.is_file():
            print('    Missing: {!s}'.format(path.relative_to(self._score_package_path)))
            sys.exit(1)
        return self._run_latex(path)

    def _render_score(self, build_target_path):
        path = build_target_path.joinpath('score.tex')
        print('Rendering {!s}'.format(path.relative_to(self._score_package_path)))
        if not path.is_file():
            print('    Missing: {!s}'.format(path.relative_to(self._score_package_path)))
            sys.exit(1)
        return self._run_latex(path)

    def _run_latex(self, latex_path):
        latex_path = latex_path.absolute()
        relative_path = latex_path.relative_to(self._score_package_path)
        command = 'xelatex {!s}'.format(latex_path)
        with systemtools.TemporaryDirectoryChange(str(latex_path.parent)):
            for _ in range(2):
                try:
                    exit_code = subprocess.call(command, shell=True)
                except:
                    print('    Failed to render: {!s}'.format(relative_path))
                    sys.exit(1)
                if exit_code:
                    print('    Failed to render: {!s}'.format(relative_path))
                    sys.exit(1)
        return latex_path.with_suffix('.pdf')

    def _run_lilypond(self, lilypond_path):
        from abjad import abjad_configuration
        command = '{} -dno-point-and-click -o {} {}'.format(
            abjad_configuration.get('lilypond_path', 'lilypond'),
            str(lilypond_path).replace('.ly', ''),
            str(lilypond_path),
            )
        with systemtools.TemporaryDirectoryChange(str(lilypond_path.parent)):
            exit_code = subprocess.call(command, shell=True)
        if exit_code:
            print('    Failed to render: {!s}'.format(
                lilypond_path.relative_to(self._score_package_path)))
            sys.exit(1)
        return lilypond_path.with_suffix('.pdf')

    def _setup_argument_parser(self, parser):
        action_group = parser.add_argument_group('actions')
        action_group = action_group.add_mutually_exclusive_group(required=True)
        action_group.add_argument(
            '--new', '-N',
            help='create a new build target',
            metavar='NAME',
            nargs='?',
            const=True,
            default=None,
            )
        action_group.add_argument(
            '--render', '-R',
            help='render sources',
            metavar='NAME',
            )
        action_group.add_argument(
            '--distribute', '-U',
            help='stage build artifacts for distribution',
            metavar='NAME',
            )
        action_group.add_argument(
            '--list', '-L',
            dest='list_',
            help='list build targets',
            action='store_true',
            )
#        action_group.add_argument(
#            '--copy', '-Y',
#            help='copy build target',
#            metavar=('SOURCE', 'TARGET'),
#            nargs=2,
#            )
#        action_group.add_argument(
#            '--rename', '-M',
#            help='rename build target',
#            metavar=('SOURCE', 'TARGET'),
#            nargs=2,
#            )
#        action_group.add_argument(
#            '--delete', '-D',
#            help='delete build target',
#            metavar='NAME',
#            )
        render_group = parser.add_argument_group(
            '--render flags',
            'Use when rendering specific assets only.',
            )
        render_group.add_argument(
            '--front-cover',
            help='render the front cover LaTeX source',
            action='store_true',
            )
        render_group.add_argument(
            '--back-cover',
            help='render the back cover LaTeX source',
            action='store_true',
            )
        render_group.add_argument(
            '--preface',
            help='render the preface LaTeX source',
            action='store_true',
            )
        render_group.add_argument(
            '--score',
            help='render the aggregate score LaTeX source',
            action='store_true',
            )
        render_group.add_argument(
            '--music',
            help='render the music LilyPond source',
            action='store_true',
            )
        render_group.add_argument(
            '--parts',
            help='render the parts LilyPond source',
            action='store_true',
            )
        create_group = parser.add_argument_group('--new options')
        create_group.add_argument(
            '--paper-size',
            metavar='PAPER_SIZE',
            help='select new build target paper size',
            choices=list(self.paper_sizes.keys()),
            default='letter',
            )
        create_group.add_argument(
            '--orientation',
            metavar='ORIENTATION',
            help='select new build target orientation',
            choices=['landscape', 'portrait'],
            default='portrait',
            )
        common_group = parser.add_argument_group('common options')
        common_group.add_argument(
            '--score-path', '-s',
            metavar='SCORE',
            help='score path or package name',
            default=os.path.curdir,
            )
        common_group.add_argument(
            '--force', '-f',
            action='store_true',
            help='force overwriting',
            )
