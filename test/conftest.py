#!/usr/bin/env python
"""conftest.py - PyTest testing fixtures
"""
import os
import pytest


@pytest.fixture
def custom_mock_cfg():
    fixture_file = os.path.join(
        os.path.dirname(__file__),
        'fixtures',
        'custom.cfg'
    )
    with open(fixture_file, 'r') as ffd:
        cfg = ffd.read()
    return cfg


@pytest.fixture
def dir_to_mount():
    src_path = os.path.join(
        os.path.dirname(__file__),
        'fixtures/mounted_data'
    )
    mnt_pt = '/mounted_data'
    test_file = 'mounted_file.txt'
    pair = (src_path, mnt_pt)
    return dict(
        src_path=src_path,
        mnt_pt=mnt_pt,
        test_file=test_file,
        test_file_path=os.path.join(mnt_pt, test_file),
        pair=pair,
        config_opts={
            'plugin_conf': {
                'bind_mount_enable': True,
                'bind_mount_opts': {'dirs': [pair]}
            }
        }
    )
