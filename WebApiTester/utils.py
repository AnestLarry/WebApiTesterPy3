def not_empty(x: any) -> bool:
    if x is not None:
        if type(x) in [int, float, bool]:
            return True
        else:
            return len(x) > 0
    else:
        return False