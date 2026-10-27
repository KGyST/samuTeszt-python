#!C:\Program Files\Python27amd64\python.exe
# -*- coding: utf-8 -*-
"""
Author: Sam KARLI
E-mail: karliterv@gmail.com
Date: 
Description:
THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT ANY WARRANTIES OF ANY KIND.
"""


class DummyObject:
  def __init__(self, a):
    self.a = a


class InstanceDecorator:
  def __init__(self, instance, path=""):
    """
    :param instance:
    :param path:
    """
    self._instance = instance
    self._path = path
    self._dict = {}

  def __setattr__(self, key, value):
    """
    :param key:
    :param value:
    :return:
    """
    if key not in ('_instance', '_path', '_dict'):
      self._dict[self._path + '/' + key] = value
      self._instance.__setattr__(key, InstanceDecorator(value, self._path + '/' + key))
    else:
      super().__setattr__(key, value)

  def __getattr__(self, item):
    return self._instance.__getattribute__(item)

  def __str__(self):
    import jsonpickle
    return jsonpickle.dumps(self, indent=4)


do1 = DummyObject(1)
id1 = InstanceDecorator(do1)

print(id1)

id1.do2 = DummyObject(2)
id1.do2.do3 = DummyObject(3)

print(id1)

