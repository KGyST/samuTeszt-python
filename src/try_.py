#!C:\Program Files\Python27amd64\python.exe
# -*- coding: utf-8 -*-
"""
Author: Sam KARLI
E-mail: karliterv@gmail.com
Date: 
Description:
THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT ANY WARRANTIES OF ANY KIND.
"""

import jsonpickle
import pprint


class Dummy:
  def __init__(self, iIdx):
    self.iIdx = iIdx
    self.prev = None
    self.next = None

  # def __repr__(self):
  #   return f"Dummy ({self.prev.iIdx} -> {self.iIdx} -> {self.next.iIdx})"


lDummy = []
_pDummy = None

for i in range(3):
  _dummy = Dummy(i)

  if _pDummy:
    _pDummy.next = _dummy

  lDummy.append(_dummy)
  _dummy.prev = _pDummy
  _pDummy = _dummy

lDummy[-1].next = lDummy[0]
lDummy[0].prev = lDummy[-1]

print (lDummy)

print (jsonpickle.dumps(lDummy))

