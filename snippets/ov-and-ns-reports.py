"""
A little script to filter transactions in NS and OV chipkaart CSV reports.

I use it to generate reimbursement request that includes only my work commute.
"""
import csv
import sys
from datetime import date

STATIONS = {
    # add here your home and work destinations
    ...,
}


def matches_ov(row: dict[str, str]) -> bool:
    if not row['Amount'].strip():
        return False
    day, month, year = row['Date'].split('-')
    d = date(int(year), int(month), int(day))
    if d.weekday() >= 5:
        return False
    if row['Departure'].strip() in STATIONS:
        return True
    if row['Destination'].strip() in STATIONS:
        return True
    return False


def matches_ns(row: dict[str, str]) -> bool:
    day, month, year = row['Datum'].split('-')
    d = date(int(year), int(month), int(day))
    if d.weekday() >= 5:
        return False
    row['Af'] = row['Af'].replace(',', '.')
    st_from = row['Vertrek'].strip()
    st_to = row['Bestemming'].strip()
    if not st_from or not st_to:
        return False
    if st_from in STATIONS:
        return True
    if st_to.strip() in STATIONS:
        return True
    return False


def matches(row: dict[str, str]) -> bool:
    if 'Bestemming' in row:
        return matches_ns(row)
    return matches_ov(row)


T_OV = '{Date}\tCommute (from {Departure} to {Destination})\t{Amount}'
T_NS = '{Datum}\tCommute (from {Vertrek} to {Bestemming})\t{Af}'

lines = []
assert sys.argv[1:]
for fname in sys.argv[1:]:
    IS_OV = fname.startswith('transactions_')
    sep = ';' if IS_OV else ','
    with open(fname) as stream:
        reader = csv.DictReader(stream, delimiter=sep)
        for row in reader:
            if not matches(row):
                # print('! {Date}\t"{Departure}"\t"{Destination}"'.format(**row))
                continue
            t = T_OV if IS_OV else T_NS
            line = t.format(**row)
            line = line.replace('€', '')
            lines.append(line)
    if not IS_OV:
        lines.reverse()
print(*lines, sep='\n')
