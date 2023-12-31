from src.api import SJApi, HHApi, BaseApi
import pytest


def test_sj_api():
    """Test SJ Api"""

    # case #1
    sj = SJApi()
    data = sj.get_vacancies()
    assert data is not None

    # case #2
    with pytest.raises(Exception):
        SJApi(api_key=None)

    # case #3
    sj.url = 'https://v-petrenko.ru/none/'
    with pytest.raises(Exception):
        sj.get_vacancies()


def test_hh_api():
    """Test HH Api"""

    # Case #1
    hh = HHApi()
    data = hh.get_vacancies()
    assert data is not None


def test_base_api():
    class Tmp(BaseApi):
        def __init__(self):
            super().__init__()

    tmp = Tmp()
    assert tmp.url is None
    assert tmp.headers is None
