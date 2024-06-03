import inspect


def get_parent_name():
    try:
        current_frame = inspect.currentframe()
        outer_frame = inspect.getouterframes(current_frame, 3)
        return outer_frame[2][3]
    except Exception as e:
        print(e)
        return "Unknown Function"
