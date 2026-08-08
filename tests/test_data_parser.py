from branch_growth_analyst.data_parser import (
    parse_indonesian_number,
    parse_indonesian_percent,
    format_indonesian_number,
    format_indonesian_percent,
)

def test_parse_indonesian_number():
    assert parse_indonesian_number("1.234") == 1234
    assert parse_indonesian_number("500") == 500
    assert parse_indonesian_number("") == 0
    assert parse_indonesian_number(None) == 0
    assert parse_indonesian_number("abc") == 0

def test_parse_indonesian_percent():
    assert parse_indonesian_percent("2,5%") == 2.5
    assert parse_indonesian_percent("0,22%") == 0.22
    assert parse_indonesian_percent("1.07%") == 1.07
    assert parse_indonesian_percent("") == 0.0
    assert parse_indonesian_percent(None) == 0.0

def test_format_indonesian_number():
    assert format_indonesian_number(1234) == "1.234"
    assert format_indonesian_number(500) == "500"
    assert format_indonesian_number(0) == "0"

def test_format_indonesian_percent():
    assert format_indonesian_percent(2.5) == "2,50%"
    assert format_indonesian_percent(0.22) == "0,22%"
    assert format_indonesian_percent(5.0) == "5%"
    assert format_indonesian_percent(0.0) == "0%"
