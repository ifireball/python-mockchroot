#!/usr/bin/env python
"""test_mock_chroot_config.py - Testing for mock_chroot/config.py
"""
import pytest
from textwrap import dedent
from collections import namedtuple

import mock_chroot.config

InputExpected = namedtuple('InputExpected', ('input', 'expected'))


class TestMockConfig(object):
    class conf_obj:
        """Mockup configuration object"""
        def __init__(self, tag, methods=None):
            """setup a configurtion object with the given methods"""
            for method in methods or ():
                def phase_method(self, cmp_ctx, tag=tag, method=method):
                    cmp_ctx['ln#'] = cmp_ctx.get('ln#', 0) + 1
                    return "{0:02} {1}: {2}".format(cmp_ctx['ln#'], tag, method)
                setattr(self, method, phase_method.__get__(self))
            self.__str__ = (lambda(slf): str(tag)).__get__(self)

    @pytest.mark.parametrize(
        ('conf_objects', 'expected'),
        [
            (
                (
                    conf_obj('c1', ('initialization', 'body', 'finalization')),
                    conf_obj('c2', ('initialization', 'finalization')),
                    conf_obj('c3', ('body',)),
                    conf_obj('c4'),
                    'plain string',
                ),
                dedent("""
                    01 c1: initialization
                    02 c2: initialization
                    03 c1: body
                    c2
                    04 c3: body
                    c4
                    plain string
                    05 c2: finalization
                    06 c1: finalization
                """).strip()
            ),
            (
                (),
                ''
            ),
            (
                (
                    conf_obj('c1', ('body',)),
                    mock_chroot.config.compose(
                        conf_obj('c2', ('body',)),
                        conf_obj('c3', ('body',))
                    ),
                ),
                dedent("""
                    01 c1: body
                    02 c2: body
                    03 c3: body
                """).strip()
            ),
        ]
    )
    def test_compose(self, conf_objects, expected):
        composit = mock_chroot.config.compose(*conf_objects)
        output = str(composit)
        assert output == expected

    @pytest.mark.parametrize(
        ('initialization', 'body', 'finalization', 'expected_str'),
        [
            (
                InputExpected(input='init1', expected='init1'),
                InputExpected(input='body1', expected='body1'),
                InputExpected(input='fin1', expected='fin1'),
                'init1\nbody1\nfin1'
            ),
            (
                InputExpected(input=None, expected=AttributeError),
                InputExpected(input='body2', expected='body2'),
                InputExpected(input=None, expected=AttributeError),
                'body2'
            ),
            (
                InputExpected(input='init3', expected='init3'),
                InputExpected(input=None, expected=AttributeError),
                InputExpected(input=None, expected=AttributeError),
                'init3'
            ),
            (
                InputExpected(input='init4', expected='init4'),
                InputExpected(input='body4', expected='body4'),
                InputExpected(input=None, expected=AttributeError),
                'init4\nbody4'
            ),
        ]
    )
    def test_configuration_object(
        self, initialization, body, finalization, expected_str
    ):
        ALL_METHODS = ('initialization', 'body', 'finalization')

        conf_obj = mock_chroot.config.ConfigurationObject(
            initialization=initialization.input,
            body=body.input,
            finalization=finalization.input
        )
        for method in ALL_METHODS:
            method_inp_exp = locals()[method]
            if (
                isinstance(method_inp_exp.expected, type)
                and issubclass(method_inp_exp.expected, Exception)
            ):
                with pytest.raises(method_inp_exp.expected):
                    getattr(conf_obj, method)({})
            else:
                output = getattr(conf_obj, method)({})
                assert output == method_inp_exp.expected
        output = str(conf_obj)
        assert output == expected_str
