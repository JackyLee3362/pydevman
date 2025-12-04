from pydevman.string.match import (
    increment_str_last_num,
    match_by_strategy,
    match_str_last_num,
)


def test_match():
    assert match_by_strategy("abc", "abc", "equal")


def test_get_num_from_str():
    s = ""
    s1 = match_str_last_num(s)
    s2 = increment_str_last_num(s)
    assert s1 is None
    assert s2 == "-(1)"

    s = "101"
    s1 = match_str_last_num(s)
    s2 = increment_str_last_num(s)
    assert s1 == "101"
    assert s2 == "102"

    s = "a1bc1"
    s1 = match_str_last_num(s)
    s2 = increment_str_last_num(s)
    assert s1 == "1"
    assert s2 == "a1bc2"

    s = "abc"
    s1 = match_str_last_num(s)
    s2 = increment_str_last_num(s)
    assert s1 is None
    assert s2 == "abc-(1)"

    s = "abc-(1)"
    s1 = match_str_last_num(s)
    s2 = increment_str_last_num(s)
    assert s1 == "1"
    assert s2 == "abc-(2)"

    s = "abc10"
    s1 = match_str_last_num(s)
    s2 = increment_str_last_num(s)
    assert s1 == "10"
    assert s2 == "abc11"

    s = "abc01"
    s1 = match_str_last_num(s)
    s2 = increment_str_last_num(s)
    assert s1 == "01"
    assert s2 == "abc02"

    s = "abc01def020"
    s1 = match_str_last_num(s)
    s2 = increment_str_last_num(s)
    assert s1 == "020"
    assert s2 == "abc01def021"

    s = "abc 010 0200 003000 dd"
    s1 = match_str_last_num(s)
    s2 = increment_str_last_num(s)
    assert s1 == "003000"
    assert s2 == "abc 010 0200 003001 dd"

    s = "abc999def"
    s1 = match_str_last_num(s)
    s2 = increment_str_last_num(s)
    assert s1 == "999"
    assert s2 == "abc1000def"

    s = "abc0999def"
    s1 = match_str_last_num(s)
    s2 = increment_str_last_num(s)
    assert s1 == "0999"
    assert s2 == "abc1000def"
