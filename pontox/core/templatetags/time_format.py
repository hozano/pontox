__author__ = 'pedro'
from django import template

register = template.Library()

@register.simple_tag
def horas_acumuladas(timedelta):
    try:
        td = timedelta
        hours = td.seconds/3600+(td.days*24)
        d = {"days": td.days}
        d["hours"], rem = (divmod(td.seconds, 3600))
        d["minutes"], d["seconds"] = divmod(rem, 60)
        if len(str(hours)) == 1:
            hours = '0'+str(hours)
        minutes = "{minutes}".format(**d)
        if len(minutes) == 1:
            minutes = '0'+str(minutes)
        return str(hours)+"h "+minutes+'min'
    except ValueError:
        return None