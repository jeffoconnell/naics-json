"""naicsToJson

Given a NAICS csv category listing, this will convert it to a nested json structure

Jeff O'Connell
"""

import argparse
import csv
import json
import os
import sys
from pathlib import Path


class NaicsCode(object):
  """docstring for NaicsCode"""
  def __init__(self, row):
    super().__init__()
    self.seq = row['Seq']
    self.code = row['Code']
    self.title = row['Title']
    self.subCodes = []
  def get_json_state(self):
    return {
            "code": self.code,
            "name": self.title,
            "id": int(self.seq),
            "children": self.subCodes }
    #[self.seq, self.code, self.title, self.subCodes]

class NaicsEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, NaicsCode):
      return obj.get_json_state()
    else:
      return json.JSONEncoder.default(self, obj)



def parse_args(argv):
  """parse_args

  Parse arguments

  :param argv: arguments
  """
  parser = argparse.ArgumentParser(description='')
  parser.add_argument('--in', dest='input', help='NAICS csv input file')
  parser.add_argument('--out', dest='output', help='NAICS json output file')
  args = parser.parse_args(argv)
  return args

def buildCodeKeyArray(origCode):
  #careful, some keys are stupid bullshit ranges ' - '
  #attempt to split the key on the delimeter '-'
  keysArray = origCode.split("-")
  #if there is more than one value, create the range.
  if len(keysArray) > 1:
    #convert to integers
    strKeys = list(map(int, keysArray))
    #create the numeric range
    keyRange = list(range(strKeys[0], strKeys[1]))
    #range lops off the end, so put it back
    keyRange.append(strKeys[1])
    #convert back to array of strings
    keysArray = list(map(str, keyRange))

  return keysArray


def insertRow(currentRow, codes):
  inserted = False

  #loop through and see if there is a matching prefix key
  for row in codes:
    keyArray = buildCodeKeyArray(row.code)
    #since the key could be a range, you need to check them all
    for theKey in keyArray:
      if currentRow.code.startswith(theKey):
        #child of this key, recurse
        insertRow(currentRow, row.subCodes)
        inserted = True

  if not inserted:
    #subCodes[currentRow['Code']] = currentRow
    codes.append(currentRow)


def main(argv):
  """main

  Read in NAICS code csv, convert it to nested json structure

  :param argv: command-line arguments
  """
  args = parse_args(argv)
  nPath = Path(args.input).resolve()
  #print (sys.getrecursionlimit())
  #sys.setrecursionlimit(1500)
  with open(nPath) as naicsFile:
    reader = csv.DictReader(naicsFile, delimiter=',')

    codes = []
    for row in reader:
      theRow = NaicsCode(row)

      #print (json.dumps(theRow, cls=NaicsEncoder))

      insertRow(theRow, codes)

  if args.output:
    with open(args.output, 'w') as fp:
      json.dump(codes, fp, cls=NaicsEncoder)
  else:
    print (json.dumps(codes, cls=NaicsEncoder))

if __name__ == '__main__':
    main(sys.argv[1:])



