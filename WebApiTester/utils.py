from requests import Response


def not_empty(x: any) -> bool:
    if x is not None:
        if type(x) in [int, float, bool]:
            return True
        else:
            return len(x) > 0
    else:
        return False

def status_code_eq_200(x: Response) -> bool:
    return x.status_code == 200
