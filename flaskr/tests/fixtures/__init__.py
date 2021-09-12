import string
import random


class RandomStringFixture():

  def create(self):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))


class ObjectFixture():
  """ Returns a fixed object value"""

  def __init__(self, value = None):
    self._value = value

  def create(self):
    return self._value


class RandomStringOfNumbers():
  def __init__(self, length = None):
    self._length = length

  def create(self):
    range_start = 10**(self._length-1)
    range_end = (10**self._length)-1
    return str(random.randint(range_start, range_end))
