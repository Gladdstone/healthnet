from django import template

from calendar import HTMLCalendar

register = template.Library()

@register.tag('calendar')
def calendar(parser, token):
	args = token.contents.split()
	return CalendarNode(args[1], args[2])
	
class CalendarNode(template.Node):
	def __init__(self, year, month):
		try:
			self.year = template.Variable(year)
			self.month = template.Variable(month)
		except ValueError:
			raise template.TemplateSyntaxError
		
	def render(self, context):
		try:
			my_year = self.year.resolve(context)
			my_month = self.month.resolve(context)
			cal = HTMLCalendar()
			return cal.formatmonth(int(my_year), int(my_month))
		except ValueError:
			return	
		except template.VariableDoesNotExist:
			return