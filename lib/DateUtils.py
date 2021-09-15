from datetime import date, datetime, timedelta

def toBrazilianDate(date):
    return date.strftime('%d/%m/%Y')

def fromBrazilianDate(strDate):
    return datetime.strptime(strDate, '%d/%m/%Y')

def today():
    return date.today()

def now():
    return datetime.now()

def addDays(date, days):
    return date + timedelta(days=days)

def addMonths(date, months):
    return date + timedelta(days=months*30)

