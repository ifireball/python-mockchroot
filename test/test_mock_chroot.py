#!/usr/bin/env python
"""test_mock_chroot.py - Testing for mock_chroot.py
"""
import pytest
from subprocess import CalledProcessError

from mock_chroot import MockChroot
import mock_chroot


class TestMockChroot(object):
    @pytest.mark.parametrize(
        ('init_args', 'more_args', 'expected'),
        [
            (
                dict(root='a_root_file'),
                ('foo', 'bar'),
                (MockChroot.mock_exe(), '--root=a_root_file', 'foo', 'bar'),
            ),
        ]
    )
    def test__mock_cmd(self, init_args, more_args, expected):
        mock = MockChroot(**init_args)
        result = mock._mock_cmd(*more_args)
        assert result == expected

    def test_chroot(self):
        mc = MockChroot(root='epel-6-x86_64')
        expected = 'CentOS release 6.7 (Final)\nKernel \\r on an \\m\n\n'
        output = mc.chroot('cat', '/etc/issue')
        assert output == expected
        expected = 'testing\n'
        output = mc.chroot('bash', '-c', 'echo testing | tee test.txt')
        assert output == expected
        output = mc.chroot('cat', 'test.txt')
        assert output == expected
        with pytest.raises(CalledProcessError):
            output = mc.chroot('false')
        # the following will raise an exception if we're in the wrong directory
        output = mc.chroot('cat', 'hosts', cwd='etc')

    def test_string_config(self, custom_mock_cfg):
        cmc = MockChroot(config=custom_mock_cfg)
        output = cmc.chroot('/usr/bin/yum', '-q', 'list', 'google-chrome-beta')
        # If the package is not there, or any other error, yum will return a
        # nonzero value, which will raise an exception. So output will contain a
        # non blank string only if the package is found
        assert output

    def test_init_bad_params(self, custom_mock_cfg):
        with pytest.raises(RuntimeError):
            MockChroot(
                root='epel-6-x86_64',
                config=custom_mock_cfg
            )

    def test_clean(self):
        mc = MockChroot(root='epel-6-x86_64')
        expected = 'testing\n'
        output = mc.chroot('bash', '-c', 'echo testing | tee test.txt')
        assert output == expected
        output = mc.chroot('cat', 'test.txt')
        assert output == expected
        mc.clean()
        with pytest.raises(CalledProcessError):
            output = mc.chroot('cat', 'test.txt')
        expected = 'not there\n'
        output = mc.chroot('bash', '-c', 'test -e test.txt || echo not there')
        assert output == expected

    @pytest.mark.parametrize(
        ('args', 'expected'),
        [
            (
                dict(no_clean=True),
                ['--no-clean'],
            ),
            (
                dict(no_clean=False),
                [],
            ),
            (
                dict(define='def1'),
                ['--define', 'def1'],
            ),
            (
                dict(define=('def1', 'def2')),
                ['--define', 'def1', '--define', 'def2'],
            ),
            (
                dict(resultdir='/a/dir'),
                ['--resultdir', '/a/dir'],
            ),
            (
                dict(define=7),
                TypeError,
            ),
            (
                dict(no_clean=False, define='def1', resultdir='/a/dir'),
                ['--define', 'def1', '--resultdir', '/a/dir'],
            ),
        ]
    )
    def test__setup_mock_build_options(self, args, expected):
        if isinstance(expected, type) and issubclass(expected, Exception):
            with pytest.raises(expected):
                MockChroot._setup_mock_build_options(**args)
        else:
            output = MockChroot._setup_mock_build_options(**args)
            assert output == expected

    def test_rebuild(self, monkeypatch):
        # Set to list to get it passed by reference to clusures
        checked_cmd = [[]]

        def check_output(cmd):
            checked_cmd[0] = list(cmd)
            return 'some output'
        monkeypatch.setattr(mock_chroot, 'check_output', check_output)
        mc = MockChroot(root='some_root')
        output = mc.rebuild(src_rpm='some.src.rpm')
        expected = [
            MockChroot.mock_exe(),
            '--root=some_root',
            '--rebuild', 'some.src.rpm'
        ]
        assert checked_cmd[0] == expected
        assert output == 'some output'
        mc.rebuild(src_rpm='some.src.rpm', define='def1')
        expected = [
            MockChroot.mock_exe(),
            '--root=some_root',
            '--rebuild', 'some.src.rpm',
            '--define', 'def1',
        ]
        assert checked_cmd[0] == expected
        assert output == 'some output'

    def test_buildsrpm(self, monkeypatch):
        # Set to list to get it passed by reference to clusures
        checked_cmd = [[]]

        def check_output(cmd):
            checked_cmd[0] = list(cmd)
            return 'some output'
        monkeypatch.setattr(mock_chroot, 'check_output', check_output)
        mc = MockChroot(root='some_root')
        output = mc.buildsrpm(spec='some.spec', sources='/some/sources')
        expected = [
            MockChroot.mock_exe(),
            '--root=some_root',
            '--buildsrpm',
            '--spec', 'some.spec',
            '--sources', '/some/sources',
        ]
        assert checked_cmd[0] == expected
        assert output == 'some output'
        output = mc.buildsrpm(
            spec='some.spec', sources='/some/sources', define='def1'
        )
        expected = [
            MockChroot.mock_exe(),
            '--root=some_root',
            '--buildsrpm',
            '--spec', 'some.spec',
            '--sources', '/some/sources',
            '--define', 'def1',
        ]
        assert checked_cmd[0] == expected
        assert output == 'some output'
