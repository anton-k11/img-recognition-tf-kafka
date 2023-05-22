import re
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from dateutil import parser

#Plot from hardcoded values
#x = [dt(2023, 5, 15, 9, 20, 22), dt(2023, 5, 15, 9, 21, 45), dt(2023, 5, 15, 9, 22, 34), dt(2023, 5, 15, 9, 23, 25), dt(2023, 5, 15, 9, 24, 15), dt(2023, 5, 15, 9, 25, 34), dt(2023, 5, 15, 9, 26, 50)]
#y = [3, 3, 5, 7, 9, 11, 15]

#Plot form log
x = []
y = []
with open('log.txt') as log_file:
  for line in log_file.readlines():
    temp_x = re.findall(r'\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}.\d{3}Z', line)[0]
    temp_y = re.findall('message":"(.*)"}', line)[0]
    date = parser.parse(temp_x)
    x.append(date)
    y.append(int(temp_y))

fig, ax = plt.subplots()
date_form = DateFormatter("%H:%M:%S")
ax.plot(x, y)
ax.xaxis.set_major_formatter(date_form)
ax.fill_between(x, y)
ax.set_ylim(ymin=0)
plt.title("Time Taken by Process")
plt.xlabel("Timestamp")
plt.ylabel("Y")
plt.show()
