from django import template

register = template.Library()

@register.filter
def get_entry_for_date(entries, day):
    """Return the HabitEntry object for a given date if it exists."""
    return entries.filter(date=day).first()

@register.filter
def filter_done_in_week(entries, week_days):
    """Return only entries marked done within the given week."""
    return entries.filter(date__in=week_days, done=True)

