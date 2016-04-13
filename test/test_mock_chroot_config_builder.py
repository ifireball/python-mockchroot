#!/usr/bin/env python
"""test_mock_chroot_config_builder.py - testing for mock_chroot.config.builder
"""
import pytest
from copy import deepcopy

import mock_chroot.config.builder


class TestMockConfigBuilder(object):
    @pytest.mark.parametrize(
        ('to_expr', 'expected', 'locals_init', 'locals_expected'),
        [
            (
                "to['some_key'].set('some_value')",
                "config_opts['some_key'] = 'some_value'",
                {'config_opts': {}},
                {'config_opts': {'some_key': 'some_value'}},
            ),
            (
                "to['a_key'].append('a_value')",
                "config_opts['a_key'].append('a_value')",
                {'config_opts': {'a_key': ['v0']}},
                {'config_opts': {'a_key': ['v0', 'a_value']}},
            ),
            (
                "to['a_key'].extend(('a_val',))",
                "config_opts['a_key'].extend(('a_val',))",
                {'config_opts': {'a_key': ['v0']}},
                {'config_opts': {'a_key': ['v0', 'a_val']}},
            ),
            (
                "to['key1']['key2'].set(7)",
                "config_opts['key1']['key2'] = 7",
                {'config_opts': {'key1': {}}},
                {'config_opts': {'key1': {'key2': 7}}},
            ),
        ]
    )
    def test_to(self, to_expr, expected, locals_init, locals_expected):
        output = eval(to_expr, {}, {'to': mock_chroot.config.builder.to})
        assert output == expected
        conf_locals = deepcopy(locals_init)
        exec(output, {}, conf_locals)
        assert conf_locals == locals_expected
