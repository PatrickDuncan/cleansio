""" Helper Functions for Speech """

def leading_zero(num):
    """ Adds a leading 0 to single digit numbers. Converts numbers to string """
    str_num = str(num)
    if len(str_num) < 2:
        return '0'+str_num
    return str_num
