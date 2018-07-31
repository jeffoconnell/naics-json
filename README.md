## naics-json

A simple python script that converts standard flat NAICS csv to a nested hierachy json file.


### To Run

#### To File
There are two arguments --in (the csv file) and --out (your new json file)

```bash
python3 naicsToJson.py --in ./naics.csv --out test.json
```

#### To stdout
There are two arguments --in (the csv file) and --out (your new json file)

```bash
python3 naicsToJson.py --in ./naics.csv
```