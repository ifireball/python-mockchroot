#!/usr/bin/env python
"""test_mock_chroot_config_highlevel.py - Testing for high-level Mock
configuration generators in mock_chroot.config.highlevel
"""
import mock_chroot.config
from mock_chroot import MockChroot


class TestMockConfigHighLevel(object):
    def test_bind_mount(self, custom_mock_cfg, dir_to_mount):
        cmc = MockChroot(config=mock_chroot.config.compose(
            custom_mock_cfg,
            mock_chroot.config.bind_mount(dir_to_mount['pair'])
        ))
        output = cmc.chroot('cat', dir_to_mount['test_file_path'])
        # If we got here, we've no exception so the file is there
        assert output

    def test_file(self, custom_mock_cfg):
        file_path = '/a_generated_file.txt'
        file_content = 'just some generated text'
        cmc = MockChroot(config=mock_chroot.config.compose(
            custom_mock_cfg,
            mock_chroot.config.file(file_path, file_content)
        ))
        # Must clean the chroot for files to be created
        cmc.clean()
        output = cmc.chroot('cat', file_path)
        # If we got here, we've no exception so the file is there
        assert output == file_content

    def test_env_vars(self, custom_mock_cfg):
        var_name = 'MY_VAR'
        var_value = 'my value'
        cmc = MockChroot(config=mock_chroot.config.compose(
            custom_mock_cfg,
            mock_chroot.config.env_vars(**{var_name: var_value})
        ))
        output = cmc.chroot('bash', '-c', 'echo "${0}"'.format(var_name))
        # If we got here, we've no exception so the file is there
        assert output.rstrip() == var_value

    def test_use_host_resolv(self, custom_mock_cfg):
        host_name = 'www.google.com'
        cmc = MockChroot(config=mock_chroot.config.compose(
            custom_mock_cfg,
            mock_chroot.config.use_host_resolv()
        ))
        output = cmc.chroot('getent', 'hosts', host_name)
        # If we got here, we've no exception so DNS worked
        assert output
