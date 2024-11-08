def bonus(x:int, y:int) -> int:
    result = 0
    if x>0 and y>0:
        result = 30
    if x>10 and y<10:
        result += 20
    else:
        result += 10
    return result
    
def check_str_len(text:str) -> str:
    result = 'unknown'

    if len(text) <= 5:
        result = 'too short'
    elif len(text) >= 10:
        result = 'too long'
    else:
        result = 'just right'

    return result

def check_boolean(one:bool, two:bool) -> str:
    result = f'one is {one} and two is {two}'
    return result