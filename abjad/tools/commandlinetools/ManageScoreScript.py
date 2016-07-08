# -*- coding: utf-8 -*-
from __future__ import print_function
import datetime
import os
import sys
from abjad.tools import stringtools
from abjad.tools.commandlinetools.ScorePackageScript import ScorePackageScript
try:
    import pathlib
except ImportError:
    import pathlib2 as pathlib


class ManageScoreScript(ScorePackageScript):
    '''
    Manages score package.

    ..  shell::

        ajv score --help

    '''

    ### CLASS VARIABLES ###

    alias = 'score'
    short_description = 'Manage score packages.'

    ### PRIVATE METHODS ###

    def _handle_create(
        self,
        title,
        year,
        composer_email=None,
        composer_github=None,
        composer_library=None,
        composer_name=None,
        composer_website=None,
        force=False,
        ):
        print('Creating score package {!r}...'.format(title))
        score_package_name = stringtools.to_accent_free_snake_case(title)
        outer_target_path = pathlib.Path(score_package_name).absolute()
        inner_target_path = outer_target_path.joinpath(score_package_name)
        if outer_target_path.exists() and not force:
            message = '    Directory {!s} already exists.'
            message = message.format(score_package_name)
            print(message)
            sys.exit(1)
        metadata = {
            'score_package_name': score_package_name,
            'composer_email': composer_email,
            'composer_full_name': composer_name,
            'composer_github_username': composer_github,
            'composer_library_package_name': composer_library,
            'score_title': title,
            'year': year,
            }
        boilerplate_path = self._get_boilerplate_path()
        outer_source_path = boilerplate_path.joinpath('example_score')
        inner_source_path = outer_source_path.joinpath('example_score')
        suffixes = ('.py', '.tex', '.ly', '.ily', '.md', '.yml')
        for path in self._copy_tree(
            outer_source_path,
            outer_target_path,
            recurse=False,
            ):
            if path.is_file() and path.suffix in suffixes:
                self._template_file(path, **metadata)
        for path in self._copy_tree(
            inner_source_path,
            inner_target_path,
            recurse=True,
            ):
            if path.is_file() and path.suffix in suffixes:
                self._template_file(path, **metadata)
        self._setup_paths(inner_target_path)
        self._write_json(
            dict(
                composer_email=composer_email,
                composer_github=composer_github,
                composer_library=composer_library,
                composer_name=composer_name,
                composer_website=composer_website,
                title=title,
                year=int(year),
                ),
            inner_target_path.joinpath('metadata.json'),
            )
        print('    Created {path!s}{sep}'.format(
            path=score_package_name,
            sep=os.path.sep))

    def _process_args(self, args):
        if args.new:
            self._handle_create(
                title=args.new,
                year=int(args.year),
                composer_email=args.composer_email,
                composer_github=args.composer_github,
                composer_library=args.composer_library,
                composer_name=args.composer_name,
                composer_website=args.composer_website,
                force=args.force,
                )

    def _setup_argument_parser(self, parser):
        action_group = parser.add_argument_group('actions')
        action_group = action_group.add_mutually_exclusive_group(required=True)
        action_group.add_argument(
            '--new', '-N',
            help='create a new score',
            metavar='TITLE',
            )
        create_group = parser.add_argument_group('--new options')
        create_group.add_argument(
            '--year', '-y',
            default=str(datetime.datetime.today().year),
            metavar='YEAR',
            )
        create_group.add_argument(
            '--composer-name', '-n',
            default='A Composer',
            metavar='NAME',
            )
        create_group.add_argument(
            '--composer-email', '-e',
            default='composer@email.com',
            metavar='EMAIL',
            )
        create_group.add_argument(
            '--composer-github', '-g',
            default='composer',
            metavar='GITHUB_USERNAME',
            )
        create_group.add_argument(
            '--composer-library', '-l',
            default='library',
            metavar='LIBRARY_NAME',
            )
        create_group.add_argument(
            '--composer-website', '-w',
            default='www.composer.com',
            metavar='WEBSITE',
            )
        common_group = parser.add_argument_group('common options')
        common_group.add_argument(
            '--force', '-f',
            action='store_true',
            help='force overwriting',
            )
