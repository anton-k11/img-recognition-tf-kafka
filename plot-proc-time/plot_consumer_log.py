from datetime import datetime, timedelta
import re
import logging
import matplotlib.pyplot as plt
from matplotlib.dates import DateFormatter
from python_on_whales import docker
from dateutil import parser

#Plot from hardcoded values
#x = [dt(2023, 5, 15, 9, 20, 22), dt(2023, 5, 15, 9, 21, 45), dt(2023, 5, 15, 9, 22, 34), dt(2023, 5, 15, 9, 23, 25), dt(2023, 5, 15, 9, 24, 15), dt(2023, 5, 15, 9, 25, 34), dt(2023, 5, 15, 9, 26, 50)]
#y = [3, 3, 5, 7, 9, 11, 15]

logging.basicConfig(format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

container_logs = docker.compose.logs(
      services=['decision-consumer'],
      tail=None,
      follow=False,
      no_log_prefix=False,
      timestamps=False,
      since=None,
      until=None,
      stream=False,
  )


#Plot form log
x = []
y = []

for line in container_logs.splitlines():
  if "Delivered" in line:
    temp_x = re.findall(r'\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3}', line)[0]
    temp_y = re.findall(r'Delivered in (\d*) ms.', line)[0]
    date = parser.parse(temp_x)

    logging.info(f'x is {temp_x}, y is {temp_y}, date is {date}')

    x.append(date)
    y.append(int(temp_y))


fig, ax = plt.subplots()
date_form = DateFormatter("%H:%M:%S")
ax.plot(x, y)
ax.xaxis.set_major_formatter(date_form)
ax.fill_between(x, y)
ax.set_ylim(ymin=100, ymax=450)
#ax.set_xlim(datetime.now() - timedelta(hours=3, minutes=9))
ax.set_xbound(datetime.now() - timedelta(hours=3, minutes=10), datetime.now() - timedelta(hours=2, minutes=59, seconds=30))
plt.title("End To End Time")
plt.xlabel("Timestamp")
plt.ylabel("Milliseconds")
# mng = plt.get_current_fig_manager()
# mng.resize(*mng.window.maxsize())
plt.show()
