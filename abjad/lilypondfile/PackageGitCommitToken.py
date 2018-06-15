import importlib
import os
import subprocess
from abjad import system
from abjad.system.AbjadValueObject import AbjadValueObject


class PackageGitCommitToken(AbjadValueObject):
    """
    A Python package git commit token.

    ..  container:: example

        >>> token = abjad.PackageGitCommitToken('abjad')
        >>> token
        PackageGitCommitToken(package_name='abjad')

        >>> print(format(token))  # doctest: +SKIP
        package "abjad" @ b6a48a7 [implement-lpf-git-token] (2016-02-02 13:36:25)

    """

    ### CLASS VARIABLES ###

    __slots__ = (
        '_package_name',
        )

    ### INITIALIZER ###

    def __init__(self, package_name=None):
        self._package_name = package_name

    ### SPECIAL METHODS ###

    def __format__(self, format_specification=''):
        """
        Formats package git commit token.

        ..  container:: example

            >>> token = abjad.PackageGitCommitToken('abjad')
            >>> print(format(token)) # doctest: +SKIP
            package "abjad" @ b6a48a7 [implement-lpf-git-token] (2016-02-02 13:36:25)

        Return string.
        """
        if not self.package_name:
            return ''
        if format_specification in ('', 'lilypond'):
            return self._get_lilypond_format()
        elif format_specification == 'storage':
            return system.StorageFormatManager(self).get_storage_format()
        return str(self)

    ### PRIVATE METHODS ###

    def _get_commit_timestamp(self, commit_hash):
        command = 'git show -s --format=%ci {}'.format(commit_hash)
        return self._run_command(command)

    def _get_git_branch(self):
        command = 'git rev-parse --abbrev-ref HEAD'
        return self._run_command(command)

    def _get_git_hash(self):
        command = 'git rev-parse HEAD'
        return self._run_command(command)

    def _get_lilypond_format(self):
        path = self._get_package_path()
        with system.TemporaryDirectoryChange(path):
            git_branch = self._get_git_branch()
            git_hash = self._get_git_hash()
            timestamp = self._get_commit_timestamp(git_hash)
            #print(git_branch, git_hash, timestamp)
        date, time, _ = timestamp.split()
        return 'package "{}" @ {} [{}] ({} {})'.format(
            self._package_name,
            git_hash[:7],
            git_branch,
            date,
            time,
            )

    def _get_package_path(self):
        module = importlib.import_module(self._package_name)
        path = module.__path__[0]
        if not os.path.isdir(path):
            path = os.path.dirname(path)
        path = os.path.abspath(path)
        return path

    def _run_command(self, command):
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            )
        process.wait()
        if process.returncode:
            return None
        result = process.stdout.read().splitlines()[0]
        result = result.decode('utf-8')
        return result

    ### PUBLIC PROPERTIES ###

    @property
    def package_name(self):
        """
        Gets package name of package git commit token.

        ..  container:: example

            >>> token = abjad.PackageGitCommitToken('abjad')
            >>> token.package_name
            'abjad'

        Returns string.
        """
        return self._package_name
