#!/usr/bin/env python
"""test_mock_chroot_config_koji.py - Testing for mock_chroot.config/koji.py
"""
import pytest

from mock_chroot import MockChroot
from mock_chroot.config import from_koji


class TestMockConfigKoji(object):
    # For practical reasons this code actually tries to test by connecting to
    # Brew. Patches are welcome to mockup Brew or at least change the test to
    # use a public Koji instance
    def test_chroot_by_tag(self):
        mc = MockChroot(config=from_koji(tag='rhevm-3.5-rhel-6-mead-build'))
        expected = (
            'Red Hat Enterprise Linux Server release 6.3 Beta '
            '(Santiago)\nKernel \\r on an \\m\n\n'
        )
        output = mc.chroot('cat', '/etc/issue')
        assert output == expected

    def test_chroot_by_target(self):
        mc = MockChroot(
            config=from_koji(target='rhevm-3.5-rhel-6-mead-candidate')
        )
        expected = (
            'Red Hat Enterprise Linux Server release 6.3 Beta '
            '(Santiago)\nKernel \\r on an \\m\n\n'
        )
        output = mc.chroot('cat', '/etc/issue')
        assert output == expected

    def test_init_bad_params(self):
        with pytest.raises(RuntimeError):
            from_koji(
                tag='rhevm-3.5-rhel-6-mead-build',
                target='rhevm-3.5-rhel-6-mead-candidate'
            )
        with pytest.raises(RuntimeError):
            from_koji()

    def test_koji_tag_for_target(self):
        expected = 'rhevm-3.5-rhel-6-mead-build'
        output = from_koji.koji_tag_for_target(
            target='rhevm-3.5-rhel-6-mead-candidate'
        )
        assert output == expected
        with pytest.raises(RuntimeError):
            from_koji.koji_tag_for_target(
                target='does-not-exist'
            )
