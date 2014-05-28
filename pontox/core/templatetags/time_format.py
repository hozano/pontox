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
        return str(hours)+"h "+"{minutes}".format(**d)+"min"
    except ValueError:
        return None