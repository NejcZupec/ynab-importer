import csv


class CSVBuilder(object):

    def __init__(self, header, rows):
        self.header = header
        self.rows = rows

    def export_csv(self, filename='export.csv'):
        csv_file = open(filename, 'w')
        writer = csv.writer(csv_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        writer.writerow(self.header)
        for row in self.rows:
            writer.writerow(list(row))
