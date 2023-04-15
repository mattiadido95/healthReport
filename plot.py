import csv
import matplotlib.pyplot as plt
from datetime import datetime


def plot_csv_data(filename):
    data = {}
    with open(filename, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            date = datetime.strptime(row['creationDate'], '%Y-%m-%d %H:%M:%S %z').date()
            value = float(row['value'])
            if date in data:
                data[date] += value
            else:
                data[date] = value

    dates = list(data.keys())
    dates.sort()
    values = [data[d] for d in dates]

    plt.figure(dpi=300)
    plt.plot(dates, values)
    plt.plot(dates, values, 'ro', linestyle='dotted')
    plt.xlabel('Date')
    plt.ylabel('Value')
    plt.show()
