import datetime
import requests
import os
import argparse
import re
import json
from dateutil.easter import easter
from dateutil.relativedelta import relativedelta as rd, FR
from holidays.constants import JAN, MAY, AUG, OCT, NOV, DEC
from holidays.holiday_base import HolidayBase


class Ecuador(HolidayBase):
    # https://viajala.com.ec/blog/calendario-dias-feriados-ecuador-actualizado
    # https://es.wikipedia.org/wiki/Cuaresma
    # https://es.wikipedia.org/wiki/ISO_3166-2:EC

    # ISO 3166-2 codes for the principal subdivisions, called provinces
    PROVINCES = ["EC-P"]  # TODO add more provinces

    def __init__(self, **kwargs):
        self.country = "EC"
        self.prov = kwargs.pop("prov", "ON")
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        # New Year's Day
        self[datetime.date(year, JAN, 1)] = "Año Nuevo [New Year's Day]"

        # Holy Week
        name_fri = "Semana Santa (Viernes Santo) [Good Friday)]"
        name_easter = "Día de Pascuas [Easter Day]"
        self[easter(year) + rd(weekday=FR(-1))] = name_fri
        self[easter(year)] = name_easter

        # Carnival
        total_lent_days = 46
        name_mondaycarnival = "Lunes de carnaval [Carnival of Monday)]"
        name_tuesdaycarnival = "Martes de carnaval [Tuesday of Carnival)]"
        self[easter(year) - datetime.timedelta(days=total_lent_days + 2)
             ] = name_mondaycarnival
        self[easter(year) - datetime.timedelta(days=total_lent_days + 1)
             ] = name_tuesdaycarnival

        # Labor Day
        name = "Día Nacional del Trabajo [Labour Day]"
        self[datetime.date(year, MAY, 1)] = name

        # Pichincha battle
        name = "Batalla del Pichincha [Pichincha Battle]"
        self[datetime.date(year, MAY, 31)] = name

        # First Cry of Independence
        name = "Primer Grito de la Independencia [First Cry of Independence]"
        self[datetime.date(year, AUG, 10)] = name

        # Guayaquil's independence
        name = "Independencia de Guayaquil [Guayaquil's Independence]"
        self[datetime.date(year, OCT, 9)] = name

        # Day of the Dead
        name = "Día de los difuntos [Day of the Dead]"
        self[datetime.date(year, NOV, 2)] = name

        # Independence of Cuenca
        name = "Independencia de Cuenca [Independence of Cuenca]"
        self[datetime.date(year, NOV, 3)] = name

        # Foundation of Quito
        if self.prov == "EC-P":
            name = "Fundación de Quito [Foundation of Quito]"
            self[datetime.date(year, DEC, 6)] = name

        # Christmas
        name = "Navidad [Christmas]"
        self[datetime.date(year, DEC, 25)] = name


class PicoPlaca:
    __days = [
            "Monday",
            "Tuesday",
            "Wednesday",
            "Thursday",
            "Friday",
            "Saturday",
            "Sunday"]

    # Dictionary that holds the restrictions inf the form {day: forbidden last digit}
    __restrictions = {
            "Monday": [1, 2],
            "Tuesday": [3, 4],
            "Wednesday": [5, 6],
            "Thursday": [7, 8],
            "Friday": [9, 0],
            "Saturday": [],
            "Sunday": []}

    def __init__(self, plate, date, tm, online=False):
        # plate is a string such as 'PEB-0001' or 'CD-0123'
        # date is a string in ISO 8601 format YYYY-MM-DD, e.g.: 2020-04-22
        # tm is a string representing time in format HH:MM, e.g.: 08:35
        # if online == True the abstract public holidays API will be used

        # Validate input
        if not re.match('^[A-Z]{2,3}-[0-9]{4}$', plate):
            raise ValueError(
                'The plate must be in the following format: XX-YYYY or XXX-YYYY, where X is a capital letter and Y is a digit')
        
        try:
            datetime.datetime.strptime(date, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            raise ValueError(
                'The date must be in the following format: YYYY-MM-DD (e.g.: 2021-04-02)')
        
        if not re.match('^([01][0-9]|2[0-3]):([0-5][0-9]|)$', tm):
            raise ValueError(
                'The time must be in the following format: HH:MM (e.g., 08:31, 14:22, 00:01)')
        
        self.plate = plate
        self.date = date
        self.tm = tm
        self.online = online


    def __find_day(self, date):
        # Returns the day from the date, e.g.: Wednesday
        # date is a string in ISO 8601 format YYYY-MM-DD, e.g.: 2020-04-22
        d = datetime.datetime.strptime(date, '%Y-%m-%d').weekday()
        return self.__days[d]


    def __is_forbidden_time(self, check_time):
        # Returns True if provided time is inside the forbidden peak hours, otherwise False
        # Peak hours: 07:00 - 09:30 and 16:00 - 19:30
        # check_time is a string in format HH:MM, e.g., 08:35
        t = datetime.datetime.strptime(check_time, '%H:%M').time()
        return ((t >= datetime.time(7, 0) and t <= datetime.time(9, 30)) or
                (t >= datetime.time(16, 0) and t <= datetime.time(19, 30)))


    def __is_holiday(self, date, online):
        # Returns True if the checked date (in ISO 8601 format YYYY-MM-DD) is a public holiday in Ecuador, otherwise False
        # if online == True it will use a REST API, otherwise it will generate the holidays of the examined year
        y, m, d = date.split('-')

        if online:
            # abstractapi Holidays API, free version: 1000 requests per month
            # 1 request per second
            # retrieve API key from enviroment variable
            key = os.environ.get('HOLIDAYS_API_KEY')
            response = requests.get(
                "https://holidays.abstractapi.com/v1/?api_key={}&country=EC&year={}&month={}&day={}".format(key, y, m, d))
            if (response.status_code == 401):
                # This means there is a missing API key
                raise requests.HTTPError(
                    'Missing API key. Store your key in the enviroment variable HOLIDAYS_API_KEY')
            if response.content == b'[]':  # if there is no holiday we get an empty array
                return False
            # Fix Maundy Thursday incorrectly denoted as holiday
            if json.loads(response.text[1:-1])['name'] == 'Maundy Thursday':
                return False
            return True
        else:
            ecu_holidays = Ecuador(prov='EC-P')
            return date in ecu_holidays


    def predict(self):
        # Returns True if the vehicle with the specified plate can be on the road at the specified date and time, otherwise False
        
        # Check if date is a holiday
        if self.__is_holiday(self.date, self.online):
            return True

        # Check for restriction-excluded vehicles according to the second letter of the plate or if using only two letters
        # https://es.wikipedia.org/wiki/Matr%C3%ADculas_automovil%C3%ADsticas_de_Ecuador
        if self.plate[1] in 'AUZEXM' or len(self.plate.split('-')[0]) == 2:
            return True

        # Check if provided time is not in the forbidden peak hours
        if not self.__is_forbidden_time(self.tm):
            return True

        day = self.__find_day(self.date)  # Find day of the week from date
        # Check if last digit of the plate is not restricted in this particular day
        if int(self.plate[-1]) not in self.__restrictions[day]:
            return True

        return False


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Pico y Placa Quito Predictor: Check if the vehicle with the provided plate can be on the road on the provided date and time')
    parser.add_argument(
        '-o',
        '--online',
        action='store_true',
        help='use abstract\'s Public Holidays API')
    parser.add_argument(
        '-p',
        '--plate',
        required=True,
        help='the vehicle\'s plate: XXX-YYYY or XX-YYYY, where X is a capital letter and Y is a digit')
    parser.add_argument(
        '-d',
        '--date',
        required=True,
        help='the date to be checked: YYYY-MM-DD')
    parser.add_argument(
        '-t',
        '--time',
        required=True,
        help='the time to be checked: HH:MM')
    args = parser.parse_args()

    pyp = PicoPlaca(args.plate, args.date, args.time, args.online)

    if pyp.predict():
        print(
            'The vehicle with plate {} CAN be on the road on {} at {}.'.format(
                args.plate,
                args.date,
                args.time))
    else:
        print(
            'The vehicle with plate {} CANNOT be on the road on {} at {}.'.format(
                args.plate,
                args.date,
                args.time))
