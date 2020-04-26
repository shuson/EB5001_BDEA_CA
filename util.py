import arrow
import unicodedata

import xml.etree.ElementTree as ET

from locale import atof
from dateutil import parser
from datetime import datetime

# convert utc to est
def convertUTCtoFull(date):
    date = parser.parse(date)
    utc = arrow.get(date.isoformat())
    return utc.to('US/Eastern').format('dddd, MMM D, YYYY h:mm A')

# convert to year
def convertUTCtoYear(date):
    date = parser.parse(date)
    utc = arrow.get(date.isoformat())
    return utc.to('US/Eastern').format('YYYY')

# convert to month
def convertUTCtoMonth(date):
    date = parser.parse(date)
    utc = arrow.get(date.isoformat())
    return utc.to('US/Eastern').format('MM')

# convert to year-month
def convertUTCtoYearMonth(date):
    date = parser.parse(date)
    utc = arrow.get(date.isoformat())
    return utc.to('US/Eastern').format('YYYY-MM')

# convert to day
def convertUTCtoDay(date):
    date = parser.parse(date)
    utc = arrow.get(date.isoformat())
    return utc.to('US/Eastern').format('D')

# convert to month/day
def convertUTCtoMonthDay(date):
    date = parser.parse(date)
    utc = arrow.get(date.isoformat())
    return utc.to('US/Eastern').format('YYYY-MM-DD')

# convert to day of week
def convertUTCtoDayOfWeek(date):
    date = parser.parse(date)
    utc = arrow.get(date.isoformat())
    return utc.to('US/Eastern').format('d')

# convert to time
def convertUTCtoHourOfDay(date):
    date = parser.parse(date)
    utc = arrow.get(date.isoformat())
    return int(utc.to('US/Eastern').format('HH'))

# convert to week of year
def convertUTCtoWeekNumber(date):
    date = parser.parse(date)
    return int(date.strftime('%U'))

# convert to year + week of year
def convertUTCtoYearWeekNumber(date):
    date = parser.parse(date)
    utc = arrow.get(date.isoformat())
    year = utc.to('US/Eastern').format('YYYY')
    weekno = int(date.strftime('%U'))
    return str(year) + '-' + str(weekno).zfill(2)

# Strip HTML
def stripHTML(html):
    tree = ET.fromstring(html)
    return ET.tostring(tree, encoding='utf8', method='text')

# Encode with closest thing to character
def encodeText(line):
    line = unicodedata.normalize('NFKD', line).encode('ascii','ignore')
    return line