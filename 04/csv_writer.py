import csv
import sys

unicode_chars = 'å∫ç'

with open(sys.argv[1], 'wt', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(('Title 1', 'Title 2', 'Title 3', 'Title 4'))
    for i in range(3):
        row = (
            i + 1,
            chr(ord('a') + i),
            '08/{:02d}/07'.format(i + 1),
            unicode_chars[i],
        )
        writer.writerow(row)
with open(sys.argv[1], 'rt', encoding='utf-8') as f:
    reader = csv.reader(f)
    print([r for r in reader])
