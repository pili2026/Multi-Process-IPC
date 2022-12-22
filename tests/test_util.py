import pytest

from utils.util import covert_number_raw


def test_covert_number_raw_with_input_invalid_number():
    with pytest.raises(ValueError) as e_info:
        covert_number_raw("q w e")

    assert e_info.value.args[0] == "The input is invalid, please check the value."


def test_covert_number_raw_with_input_valid_number():
    ret: str = covert_number_raw("1 2 3")
    assert_ret = "[1, 2, 3]"

    assert ret == assert_ret
