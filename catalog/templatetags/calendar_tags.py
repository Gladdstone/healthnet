from django import template
from calendar import HTMLCalendar

register = template.Library()

@register.simple_tag
def appointment_calendar(year, month):
	return HTMLCalendar(year, month)
	
#register.tag("appointment_calendar", appointment_calendar)