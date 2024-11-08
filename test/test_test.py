from test import bonus, check_str_len, check_boolean

def test_bonus_AnweisungsUeberdeckung_1():
    assert bonus(5,5) == 40

def test_bonus_AnweisungsUeberdeckung_2():
    assert bonus(11,5) == 50

def test_bonus_ZweigUeberdeckung_1():
    assert bonus(11,0) == 20

def test_str_len_1():
    assert check_str_len('1234') == 'too short'

def test_str_len_2():
    assert check_str_len('1234567890') == 'too long'

def test_str_len_3():
    assert check_str_len('123456') == 'just right'

def test_boolean_1():
    assert check_boolean(True, False) == 'one is True and two is False'

def test_boolean_2():
    assert check_boolean(False, True) == 'one is False and two is True'

def test_boolean_3():
    assert check_boolean(True, True) == 'one is True and two is True'

def test_boolean_4():
    assert check_boolean(False, False) == 'one is False and two is False'