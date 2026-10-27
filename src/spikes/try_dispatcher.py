from types import NoneType
from typing import Callable, Union, Any
from samuTeszt.src.common.constants import MAIN, ENCODING

FNV_PRIME = 0x01000193
HASH_OF_NONE = 0x811c9dc5
MASK = 0xffffffff

def fnv1a_hash(value, key=None, result=None, func:Callable=None):
  hash_value = HASH_OF_NONE
  hash_value ^= func(value)
  hash_value *= FNV_PRIME
  if key:
    for byte in key.encode(ENCODING):
      hash_value ^= byte
      hash_value *= FNV_PRIME
  hash_value &= MASK
  return result ^ hash_value


class Dispatcher:
  def __init__(self,
               func_int: Callable,
               func_dict: Callable,
               func_list: Callable,
               func__dict__: Callable,
               func__slots__: Callable,
               func_else: Callable,
               ):
    self._func_int = func_int
    self._func_dict = func_dict
    self._func_list = func_list
    self._func__dict__ = func__dict__
    self._func__slots__ = func__slots__ if func__slots__ else self._func__dict__
    self._func_else = func_else


  def _dispatch(self, obj, func):
    HASH_OF_NONE = None
    result = HASH_OF_NONE

    # if (obj_id := id(obj)) in visited:
    #     return visited[obj_id]

    if hasattr(obj, '__dict__'):
        for key in sorted(obj.__dict__.keys()):
            if not isinstance(obj.__dict__[key], Callable):
                result = self.func_dict(obj.__dict__[key], key, result, self._dispatch)
    elif hasattr(obj, '__slots__'):
        for slot in sorted(obj.__slots__):
            # just for uninitalized __slots__ right after __new__:
            if hasattr(obj, slot):
                result = self._func__slots__(getattr(obj, slot), slot, result, self._dispatch)
    elif isinstance(obj, dict):
        for key in sorted(obj.keys()):
            result = self._func_dict(obj[key], key, result, self._dispatch)
    elif isinstance(obj, (list, tuple, set)):
        for item in obj:
            result = self._func_list(item, None, result, self._dispatch)
    elif isinstance(obj, (int, float, bool, bytes, frozenset)):
        result = self._func_else(obj)
    # # elif isinstance(obj, str):
    # #     result = fnv1a_hash(None, obj)
    # elif obj is None:
    #     result = hash(None)
    else:
        result = HASH_OF_NONE
    return result

if __name__ == "__main__":
  d = Dispatcher(
    func_else=lambda obj: hash(obj)
  )

