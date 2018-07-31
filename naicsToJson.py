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


def insertRow(currentRow, codes):
  inserted = False
  currentKey = currentRow['Code']
  #Are there subcodes for codes?
  if 'subCodes' in codes and codes['subCodes']:
    subCodes = codes['subCodes']
    #loop through and see if there is a matching prefix key
    thekeys = subCodes.keys()
    if len(thekeys) > 0:
      for key in thekeys:
        if currentKey.startswith(key):
          #child of this key, recurse
          insertRow(currentRow, subCodes[key])
          inserted = True
  else:
    codes['subCodes'] = {}
    subCodes = codes['subCodes']

  if not inserted:
    subCodes[currentKey] = currentRow


def main(argv):
  """main

  Read in NAICS code csv, convert it to nested json structure

  :param argv: command-line arguments
  """
  args = parse_args(argv)
  nPath = Path(args.input).resolve()
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



