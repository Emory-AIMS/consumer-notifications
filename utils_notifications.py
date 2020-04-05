
def get_warning_level(status):
    if status == 0:
        return 0
    if status == 1:
        return 4
    if status == 2:
        return 2
    if status == 3:
        return 1
    return 3