from os import path as osp

def _validate_prefix(prefix: str) -> str:

    if not prefix.endswith(" "):
        prefix = prefix + " "
    if prefix[-2:]!=": ":
        prefix = prefix[:-2] + ": "

    return prefix

def _add_prefix(msg: str, prefix: str) -> str:
    if prefix is not None:
        prefix = _validate_prefix(prefix)
        msg = prefix + msg
    return msg


def assert_true(condition: bool, msg: str=None):

    if msg is not None:
        raise ValueError(msg)

def assert_equal(v0, v1, prefix: str=None):
    if v0!=v1:
        _msg = f"{v0} (value0) != {v1} (value1)."
        _msg = _add_prefix(_msg, prefix)
        raise ValueError(_msg)

def assert_path_exists(path: str, prefix: str=None):
    if not osp.exists(path):
        _msg = f"Path {path} does not exists."
        _msg = _add_prefix(_msg, prefix)
        raise FileExistsError(_msg)

def assert_is_instance(obj, t: type, prefix: str=None):
    if not isinstance(obj, t):
        _msg = f"Incorrect object type: {type(obj).__name__}"
        _msg = _add_prefix(_msg, prefix)
        raise TypeError(_msg)

def assert_is_not_none(obj, prefix: str=None):
    if obj is None:
        _msg = f"Object is None."
        _msg = _add_prefix(_msg, prefix)
        raise ValueError(_msg)

def assert_is_not_empty(obj, prefix: str=None):
    if len(obj)==0:
        _msg = f"Object is empty."
        _msg = _add_prefix(_msg, prefix)
        raise ValueError(_msg)