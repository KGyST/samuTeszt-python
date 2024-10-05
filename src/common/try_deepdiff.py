import json
from itertools import zip_longest
import os


jsonBiggest = '''
{
  "py/state": 
  [      
    1,
    2
  ]
}
'''

jsonSmallest = '''
{
  "py/state": 
  [
    1,
    2,
    3
  ],
    "py/object": "__main__.ClassToBeNested",
    "nestedObjectS":
  {
  }
}
'''

ROOT_PATH = r"E:\Git\LCFMapper\tests\GSMParamLib.GSMParamLib\ParamSection\getParamIDsByTypeNameAndValue"
jsonBiggest = open(os.path.join (ROOT_PATH, "fac8f37630a9.json"), "r").read()
jsonSmallest = open(os.path.join (ROOT_PATH, "a52f67dd2fbf.json"), "r").read()
jsonSmallest2 = open(os.path.join (ROOT_PATH, "b46d2cbaf3c3.json"), "r").read()


class Differable:
  def __init__(self, data, codec=json):
    self._codec = codec
    if isinstance(data, str):
      self._this = self._codec.loads(data)
    elif isinstance(data, dict):
      self._this = data
    else:
      self._this = {}

  @property
  def data(self):
    return self._this

  def __and__(self, other: 'Differable'):
    def _and(this, that):
      if isinstance(this, type(that)):
        if isinstance(this, list):
          _result = []
          for item1, item2 in zip(this, that):
            if (s := _and(item1, item2)) is not None:
              _result.append(s)
            else:
              break
          return _result
        elif isinstance(this, dict):
          _result = {}
          for key in this.keys():
            # Preserving key order of this
            if key in that:
              if (s := _and(this[key], that[key])) is not None:
                _result[key] = s
          return _result
        elif isinstance(this, (int, str)):
          if this == that:
            return this
          # FIXME more types
      else:
        return None

    result = Differable(_and(self._this, other.data))
    return result

  def __sub__(self, other: 'Differable'):
    def _sub(this, that):
      if isinstance(this, type(that)):
        if isinstance(this, list):
          if len(this) > len(that):
            from itertools import zip_longest
            return [None if y else x for x, y in zip_longest(this, that)]
          # elif len(this) < len(that):
          #   return None
          else:
            return None
        elif isinstance(this, dict):
          _result = {}
          for key in this.keys():
            if key not in that:
              if this[key] is not None:
                _result[key] = this[key]
            else:
              if (sub := _sub(this[key], that[key])) is not None:
                _result[key] = sub
          if all(v is None for v in _result.values()):
            return None
          return _result
        elif isinstance(this, (int, str)):
          if this == that:
            return None
      else:
        return None

    result = Differable(_sub(self._this, other.data))
    return result

  def __or__(self, other: 'Differable'):
    def _or(this, that):
      from types import NoneType
      if isinstance(this, type(that)):
        if isinstance(this, list):
          return [_or(i1, i2) for i1, i2 in zip_longest(this, that)]
        elif isinstance(this, dict):
          _result = {}
          for key in this.keys() | that.keys():
            if key not in that:
              _result[key] = this[key]
            elif key not in this:
              _result[key] = that[key]
            else:
              _result[key] = _or(this[key], that[key])
          return _result
        elif isinstance(this, (int, str)):
            return this
      elif isinstance(this, NoneType):
        return that
      elif isinstance(that, NoneType):
        return this
      else:
        return None

    result = Differable(_or(self._this, other.data))
    return result

  def __str__(self):
    return self._codec.dumps(self._this, indent=2, ensure_ascii=False)


differable1 = Differable(jsonSmallest2)
differable2 = Differable(jsonSmallest)

# print(differable1 & differable2)
# print(differable2 - differable1)
# print(differable2 | differable1)
diff = differable1 - differable2
print(diff)
# sum = diff | differable1
# print(sum)


# _k = None
# path = r"E:\Git\LCFMapper\tests\GSMParamLib.GSMParamLib\ParamSection\getParamIDsByTypeNameAndValue"
#
# for w in os.walk(path):
#   for f in w[2]:
#     _j = Differable(open(os.path.join(path, f)).read())
#
#     if _k:
#       _k = _j & _k
#     else:
#       _k = _j
#
# print (_k)

with open("diff.json", "w", encoding="utf-8") as f1:
  f1.write(diff.__str__())

