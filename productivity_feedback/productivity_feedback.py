import datetime
import os
import thread
import time
import SysTrayIcon

from rescuetime.api.service.Service import Service
from rescuetime.api.access.AnalyticApiKey import AnalyticApiKey
from rescuetime.api.model.ResponseData import ResponseData

_sysTrayIcon = None;

def get_current_productivity():
	# get today's productivity scores from the service
    s = Service()
    key = AnalyticApiKey('YOUR_API_KEY_HERE', s)
    params = {'op': 'select',
	          'vn': 0,
			  'pv': 'interval',
			  'rs': 'day',
			  'rb': datetime.date.today().strftime('%Y-%m-%d'),
			  're': (datetime.date.today() + datetime.timedelta(days = 1)).strftime('%Y-%m-%d'),
			  'rk': 'productivity'}
    r = ResponseData(key, **params)
    r.sync()
	
	# combine into a single value
    total_seconds = 0
    productive_seconds = 0
    for k in r.object:
        if k == 'rows':
            for ro in r.object[k]:
                seconds = ro[1]
                score = ro[3]
                total_seconds += seconds
                if score > 0:
                    productive_seconds += seconds
    productivity = int(round(100 * float(productive_seconds) / float(total_seconds)))
    return min(productivity, 99)

def show_current_productivity(sysTrayIcon):
    try:
        # get current productivity and update system tray icon
        productivity = get_current_productivity()
        icon_filename = os.path.join('digits', str(productivity) + '.ico')
        sysTrayIcon.icon = icon_filename
        sysTrayIcon.refresh_icon()
    except:
        pass

def _background_action(sysTrayIcon):
    while True:
        time.sleep(60)
        show_current_productivity(sysTrayIcon)

if __name__ == '__main__':
    hover_text = 'RescueTime Productivity'
    icon_filename = os.path.join('digits', '50.ico')
    SysTrayIcon.SysTrayIcon(icon_filename, hover_text, (), _background_action)
