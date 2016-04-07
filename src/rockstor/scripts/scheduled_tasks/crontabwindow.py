from datetime import datetime, time

#Crontabwindow created as a separate module to avoid code duplication on snapshots and scrubs tasks

def crontab_range(range):
    inrange = False
    #logger.debug('Crontab window is %s' % range)
    if (range == '*-*-*-*-*-*'):
        inrange = True #on range value equal to always (*-*-*-*-*-*), always exec tasks
    else:
        today = datetime.today()
        today_time = today.time()
        today_weekday = today.weekday()
        range_windows = range.split('-')
        hour_start = int(range_windows[0]) if range_windows[0] != '*' else 0
        mins_start = int(range_windows[1]) if range_windows[1] != '*' else 0
        hour_stop = int(range_windows[2]) if range_windows[2] != '*' else 23
        mins_stop = int(range_windows[3]) if range_windows[3] != '*' else 59
        day_start = int(range_windows[4]) if range_windows[4] != '*' else 0
        day_stop = int(range_windows[5]) if range_windows[5] != '*' else 6
        time_start = time(hour_start, mins_start)
        time_stop = time(hour_stop, mins_stop,59)

        #if crontab window isn't clockwise (unconvencional cron window) current time/day will never be true on start <= current <= end
        #so we get it true if start <= current OR current <= end

        if (hour_start <= hour_stop):
            intime = time_start <= today_time <= time_stop
        else:
            intime = (time_start <= today_time or today_time <= time_stop)

        if (day_start <= day_stop):
            inday = day_start <= today_weekday <= day_stop
        else:
            inday = (day_start <= today_weekday or today_weekday <= day_stop)
        inrange = intime and inday
    return inrange
