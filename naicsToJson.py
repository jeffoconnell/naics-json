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
  currentKey = currentRow['Code']

  #Are there subcodes for this NAICS code?
  if 'subCodes' in codes and codes['subCodes']:
    subCodes = codes['subCodes']
    #loop through and see if there is a matching prefix key
    thekeys = subCodes.keys()
    if len(thekeys) > 0:
      for key in thekeys:
        keyArray = buildCodeKeyArray(key)
        #since the key could be a range, you need to check them all
        for theKey in keyArray:
          if currentKey.startswith(theKey):
            #child of this key, recurse
            insertRow(currentRow, subCodes[key])
            inserted = True

  else:
    codes['subCodes'] = {}
    subCodes = codes['subCodes']

  if not inserted:
    subCodes[currentRow['Code']] = currentRow


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

    codes = {"subCodes": {}}
    for row in reader:
      insertRow(row, codes)

  if args.output:
    with open(args.output, 'w') as fp:
      json.dump(codes, fp)
  else:
    print (json.dumps(codes))

if __name__ == '__main__':
    main(sys.argv[1:])



