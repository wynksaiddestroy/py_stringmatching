import cython
cimport cython

def cython_sim_ident(unicode char1, unicode char2):
    return 1 if (char1==char2) else 0

def int_max(int a,int b):
    """Finds the maximum integer of the given two integers.
        Args:
            integer1,integer2 (int): Input integers.
        Returns:
            Maximum integer (int).
    """
    if a > b : return a
    else: return b

def int_min_two(int a,int b):
    """Finds the minimum integer of the given two integers.
    Args:
        integer a,integer b (int): Input integers.
    Returns:
        Minimum integer (int).
    """
    if a > b : return b
    else: return a

def int_min_three(int a, int b, int c):
    """Finds the minimum integer of the given two integers.
    Args:
        integer a,integer b, integer c (int): Input integers.
    Returns:
        Minimum integer (int).
    """

    if (a<=b) and (a<= c):
        return a
    elif (b<=c):
        return b
    else:
        return c
