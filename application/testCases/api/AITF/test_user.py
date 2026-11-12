from __future__ import annotations

import allure
import pytest

from domain.business.api.AITF.user_biz import create_user
from service.assert_utils import AssertUtils
from service.data_driver import parametrize_data


@allure.story("新增用户")
@pytest.mark.parametrize("case", parametrize_data("user.yaml"))
def test_user_add(case):
    resp = create_user(case['account'], case['username'], case['email'], case['password'])
    AssertUtils.status_code(resp, case['assert']['status_code'])




