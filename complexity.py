#!/usr/bin/python

import sys


def main():
  PrintDistanceToReplicatorByGeneration()


def PrintDistanceToReplicatorByGeneration():
  while True:
    generation = Generation.FromFile(sys.stdin)
    print 't%5u' % generation.time,
    for sequence_plus, sequence_minus in generation.sequences:
      distance_min = min(
        Sequence.REPLICATOR.DistanceTo(sequence_plus),
        Sequence.REPLICATOR.DistanceTo(sequence_minus))
      print '%2u' % distance_min,
    print


class Generation(object):

  @classmethod
  def FromFile(cls, f):
    time = cls._PeekTime(f)
    sequences = []
    while cls._PeekTime(f) == time:
      time_a, count_a, seq_a = cls._ReadSequence(f)
      time_b, count_b, seq_b = cls._ReadSequence(f)
      assert time_a == time_b
      assert count_a == count_b
      sequences.append((Sequence(seq_a), Sequence(seq_b)))
    return cls(time, sequences)

  @classmethod
  def _PeekTime(cls, f):
    offset = f.tell()
    line = f.readline()
    f.seek(offset)
    if line:
      assert line[0] == 't'
      time = int(line[1:line.index(' ')])
      return time

  @classmethod
  def _ReadSequence(cls, f):
    time_str, count_str, seq_str, _0, _1, _2 = f.readline().rstrip().split()
    assert time_str[0] == 't'
    time = int(time_str[1:])
    assert count_str[0] in 'sctp'
    count = int(count_str[1:-1])
    return time, count, seq_str

  def __init__(self, time, sequences):
    self._time = time
    self._sequences = sequences

  @property
  def time(self):
    return self._time

  @property
  def sequences(self):
    return self._sequences


class Sequence(object):

  def __init__(self, seq):
    assert len(seq) == 50
    assert all(c in 'ACGU' for c in seq)
    self._seq = seq

  def __len__(self):
    return len(self._seq)

  def __getitem__(self, i):
    return self._seq[i]

  @classmethod
  def Distance(cls, a, b):
    assert len(a) == len(b)
    return sum(int(a[i] != b[i]) for i in xrange(len(a)))
      
  def DistanceTo(self, other):
    return self.Distance(self, other)

Sequence.REPLICATOR = Sequence('CCCCCCCCCCCCCCGGCCGGAAACAACGUAAGAGCCAUUGUGUGGAUGCC')


if __name__ == '__main__':
  main()

