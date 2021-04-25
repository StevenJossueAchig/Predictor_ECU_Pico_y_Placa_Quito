from datetime import date, timedelta
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

class HolidayEcuador(HolidayBase):
    """
    A class to represent a Holiday in Ecuador by province (HolidayEcuador)
    It aims to make determining whether a 
    specific date is a holiday as fast and flexible as possible.
    https://www.turismo.gob.ec/wp-content/uploads/2020/03/CALENDARIO-DE-FERIADOS.pdf
    ...

    Attributes (It inherits the HolidayBase class)
    ----------
    prov: str
        province code according to ISO3166-2

    Methods
    -------
    __init__(self, plate, date, time, online=False):
        Constructs all the necessary attributes for the HolidayEcuador object.
    _populate(self, year):
        Returns if a date is holiday or not
    """     
    # ISO 3166-2 codes for the principal subdivisions, called provinces
    # https://es.wikipedia.org/wiki/ISO_3166-2:EC
    PROVINCES = ["EC-P"]  # TODO add more provinces

    def __init__(self, **kwargs):
        """
        Constructs all the necessary attributes for the HolidayEcuador object.
        """         
        self.country = "ECU"
        self.prov = kwargs.pop("prov", "ON")
        HolidayBase.__init__(self, **kwargs)

    def _populate(self, year):
        """
        Checks if a date is holiday or not
        
        Parameters
        ----------
        year : str
            year of a date

        Returns
        -------
        Returns true if a date is a holiday otherwise flase 
        """                    
        # New Year's Day 
        self[date(year, JAN, 1)] = "Año Nuevo [New Year's Day]"
        
        # Christmas
        self[date(year, DEC, 25)] = "Navidad [Christmas]"
        
        # Holy Week
        self[easter(year) + rd(weekday=FR(-1))] = "Semana Santa (Viernes Santo) [Good Friday)]"
        self[easter(year)] = "Día de Pascuas [Easter Day]"
        
        # Carnival
        total_lent_days = 46
        self[easter(year) - timedelta(days=total_lent_days+2)] = "Lunes de carnaval [Carnival of Monday)]"
        self[easter(year) - timedelta(days=total_lent_days+1)] = "Martes de carnaval [Tuesday of Carnival)]"
        
        # Labor day
        name = "Día Nacional del Trabajo [Labour Day]"
        # (Law 858/Reform Law to the LOSEP (in force since December 21, 2016 /R.O # 906)) If the holiday falls on Saturday or Tuesday
        # the mandatory rest will go to the immediate previous Friday or Monday
        # respectively
        if year > 2015 and date(year, MAY, 1).weekday() in (5,1):
            self[date(year, MAY, 1) - timedelta(days=1)] = name
        # (Law 858/Reform Law to the LOSEP (in force since December 21, 2016 /R.O # 906)) if the holiday falls on Sunday
        # the mandatory rest will go to the following Monday
        elif year > 2015 and date(year, MAY, 1).weekday() == 6:
            self[date(year, MAY, 1) + timedelta(days=1)] = name
        # (Law 858/Reform Law to the LOSEP (in force since December 21, 2016 /R.O # 906)) Holidays that are on Wednesday or Thursday
        # will be moved to the Friday of that week
        elif year > 2015 and  date(year, MAY, 1).weekday() in (2,3):
            self[date(year, MAY, 1) + rd(weekday=FR)] = name
        else:
            self[date(year, MAY, 1)] = name
        
        # Pichincha battle, the rules are the same as the labor day
        name = "Batalla del Pichincha [Pichincha Battle]"
        if year > 2015 and date(year, MAY, 24).weekday() in (5,1):
            self[date(year, MAY, 24).weekday() - timedelta(days=1)] = name
        elif year > 2015 and date(year, MAY, 24).weekday() == 6:
            self[date(year, MAY, 24) + timedelta(days=1)] = name
        elif year > 2015 and  date(year, MAY, 24).weekday() in (2,3):
            self[date(year, MAY, 24) + rd(weekday=FR)] = name
        else:
            self[date(year, MAY, 24)] = name        
        
        # First Cry of Independence, the rules are the same as the labor day
        name = "Primer Grito de la Independencia [First Cry of Independence]"
        if year > 2015 and date(year, AUG, 10).weekday() in (5,1):
            self[date(year, AUG, 10)- timedelta(days=1)] = name
        elif year > 2015 and date(year, AUG, 10).weekday() == 6:
            self[date(year, AUG, 10) + timedelta(days=1)] = name
        elif year > 2015 and  date(year, AUG, 10).weekday() in (2,3):
            self[date(year, AUG, 10) + rd(weekday=FR)] = name
        else:
            self[date(year, AUG, 10)] = name       
        
        # Guayaquil's independence, the rules are the same as the labor day
        name = "Independencia de Guayaquil [Guayaquil's Independence]"
        if year > 2015 and date(year, OCT, 9).weekday() in (5,1):
            self[date(year, OCT, 9) - timedelta(days=1)] = name
        elif year > 2015 and date(year, OCT, 9).weekday() == 6:
            self[date(year, OCT, 9) + timedelta(days=1)] = name
        elif year > 2015 and  date(year, MAY, 1).weekday() in (2,3):
            self[date(year, OCT, 9) + rd(weekday=FR)] = name
        else:
            self[date(year, OCT, 9)] = name        
        
        # Day of the Dead and
        namedd = "Día de los difuntos [Day of the Dead]" 
        # Independence of Cuenca
        nameic = "Independencia de Cuenca [Independence of Cuenca]"
        #(Law 858/Reform Law to the LOSEP (in force since December 21, 2016 /R.O # 906)) 
        #For national and/or local holidays that coincide on continuous days, 
        #the following rules will apply:
        if (date(year, NOV, 2).weekday() == 5 and  date(year, NOV, 3).weekday() == 6):
            self[date(year, NOV, 2) - timedelta(days=1)] = namedd
            self[date(year, NOV, 3) + timedelta(days=1)] = nameic     
        elif (date(year, NOV, 3).weekday() == 2):
            self[date(year, NOV, 2)] = namedd
            self[date(year, NOV, 3) - timedelta(days=2)] = nameic
        elif (date(year, NOV, 3).weekday() == 3):
            self[date(year, NOV, 3)] = nameic
            self[date(year, NOV, 2) + timedelta(days=2)] = namedd
        elif (date(year, NOV, 3).weekday() == 5):
            self[date(year, NOV, 2)] =  namedd
            self[date(year, NOV, 3) - timedelta(days=2)] = nameic
        elif (date(year, NOV, 3).weekday() == 0):
            self[date(year, NOV, 3)] = nameic
            self[date(year, NOV, 2) + timedelta(days=2)] = namedd
        else:
            self[date(year, NOV, 2)] = namedd
            self[date(year, NOV, 3)] = nameic  
            
        # Foundation of Quito, applies only to Pichincha province, 
        # the rules are the same as the labor day
        name = "Fundación de Quito [Foundation of Quito]"        
        if self.prov in ("EC-P"):
            if year > 2015 and date(year, DEC, 6).weekday() in (5,1):
                self[date(year, DEC, 6) - timedelta(days=1)] = name
            elif year > 2015 and date(year, DEC, 6).weekday() == 6:
                self[(date(year, DEC, 6).weekday()) + timedelta(days=1)] =name
            elif year > 2015 and  date(year, DEC, 6).weekday() in (2,3):
                self[date(year, DEC, 6) + rd(weekday=FR)] = name
            else:
                self[date(year, DEC, 6)] = name

class PicoPlaca:
    """
    A class to represent a vehicle restriction measure (Pico y Placa) - ORDENANZA METROPOLITANA No. 0305
    http://www7.quito.gob.ec/mdmq_ordenanzas/Ordenanzas/ORDENANZAS%20A%C3%91OS%20ANTERIORES/ORDM-305-%20%20CIRCULACION%20VEHICULAR%20PICO%20Y%20PLACA.pdf
    ...

    Attributes
    ----------
    plate : str 
        The registration or patent of a vehicle is a combination of alphabetic or numeric 
        characters that identifies and individualizes the vehicle with respect to the others; 
        The used format is XX-YYYY or XXX-YYYY, where X is a capital letter and Y is a digit.
    date : str
        Date on which the vehicle intends to transit
        It is following the ISO 8601 format YYYY-MM-DD: e.g., 2020-04-22.
    time : str
        time in which the vehicle intends to transit
        It is following the format HH:MM: e.g., 08:35, 19:30
    online: boolean, optional
        if online == True the abstract public holidays API will be used

    Methods
    -------
    __init__(self, plate, date, time, online=False):
        Constructs all the necessary attributes for the PicoPlaca object.
    plate(self):
        Gets the plate attribute value
    plate(self, value):
        Sets the plate attribute value
    date(self):
        Gets the date attribute value
    date(self, value):
        Sets the date attribute value
    time(self):
        Gets the time attribute value
    time(self, value):
        Sets the time attribute value
    __find_day(self, date):
        Returns the day from the date: e.g., Wednesday
    __is_forbidden_time(self, check_time):
        Returns True if provided time is inside the forbidden peak hours, otherwise False
    __is_holiday:
        Returns True if the checked date (in ISO 8601 format YYYY-MM-DD) is a public holiday in Ecuador, otherwise False
    predict(self):
        Returns True if the vehicle with the specified plate can be on the road at the specified date and time, otherwise False
    """ 
    #Days of the week
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

    def __init__(self, plate, date, time, online=False):
        """
        Constructs all the necessary attributes for the PicoPlaca object.
        
        Parameters
        ----------
            plate : str 
                The registration or patent of a vehicle is a combination of alphabetic or numeric 
                characters that identifies and individualizes the vehicle with respect to the others; 
                The used format is AA-YYYY or XXX-YYYY, where X is a capital letter and Y is a digit.
            date : str
                Date on which the vehicle intends to transit
                It is following the ISO 8601 format YYYY-MM-DD: e.g., 2020-04-22.
            time : str
                time in which the vehicle intends to transit
                It is following the format HH:MM: e.g., 08:35, 19:30
            online: boolean, optional
                if online == True the abstract public holidays API will be used (default is False)               
        """                
        self.plate = plate
        self.date = date
        self.time = time
        self.online = online


    @property
    def plate(self):
        """Gets the plate attribute value"""
        return self._plate


    @plate.setter
    def plate(self, value):
        """
        Sets the plate attribute value

        Parameters
        ----------
        value : str
        
        Raises
        ------
        ValueError
            If value string is not formated as XX-YYYY or XXX-YYYY, where X is a capital letter and Y is a digit
        """
        if not re.match('^[A-Z]{2,3}-[0-9]{4}$', value):
            raise ValueError(
                'The plate must be in the following format: XX-YYYY or XXX-YYYY, where X is a capital letter and Y is a digit')
        self._plate = value


    @property
    def date(self):
        """Gets the date attribute value"""
        return self._date


    @date.setter
    def date(self, value):
        """
        Sets the date attribute value

        Parameters
        ----------
        value : str
        
        Raises
        ------
        ValueError
            If value string is not formated as YYYY-MM-DD (e.g.: 2021-04-02)
        """
        try:
            if len(value) != 10:
                raise ValueError
            datetime.datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError(
                'The date must be in the following format: YYYY-MM-DD (e.g.: 2021-04-02)') from None
        self._date = value
        

    @property
    def time(self):
        """Gets the time attribute value"""
        return self._time


    @time.setter
    def time(self, value):
        """
        Sets the time attribute value

        Parameters
        ----------
        value : str
        
        Raises
        ------
        ValueError
            If value string is not formated as HH:MM (e.g., 08:31, 14:22, 00:01)
        """
        if not re.match('^([01][0-9]|2[0-3]):([0-5][0-9]|)$', value):
            raise ValueError(
                'The time must be in the following format: HH:MM (e.g., 08:31, 14:22, 00:01)')
        self._time = value


    def __find_day(self, date):
        """
        Finds the day from the date: e.g., Wednesday

        Parameters
        ----------
        date : str
            It is following the ISO 8601 format YYYY-MM-DD: e.g., 2020-04-22

        Returns
        -------
        Returns the day from the date as a string
        """        
        d = datetime.datetime.strptime(date, '%Y-%m-%d').weekday()
        return self.__days[d]


    def __is_forbidden_time(self, check_time):
        """
        Checks if the time provided is within the prohibited peak hours,
        where the peak hours are: 07:00 - 09:30 and 16:00 - 19:30

        Parameters
        ----------
        check_time : str
            Time that will be checked. It is in format HH:MM: e.g., 08:35, 19:15

        Returns
        -------
        Returns True if provided time is inside the forbidden peak hours, otherwise False
        """           
        t = datetime.datetime.strptime(check_time, '%H:%M').time()
        return ((t >= datetime.time(7, 0) and t <= datetime.time(9, 30)) or
                (t >= datetime.time(16, 0) and t <= datetime.time(19, 30)))


    def __is_holiday(self, date, online):
        """
        Checks if date (in ISO 8601 format YYYY-MM-DD) is a public holiday in Ecuador
        if online == True it will use a REST API, otherwise it will generate the holidays of the examined year
        
        Parameters
        ----------
        date : str
            It is following the ISO 8601 format YYYY-MM-DD: e.g., 2020-04-22
        online: boolean, optional
            if online == True the abstract public holidays API will be used        

        Returns
        -------
        Returns True if the checked date (in ISO 8601 format YYYY-MM-DD) is a public holiday in Ecuador, otherwise False
        """            
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
            ecu_holidays = HolidayEcuador(prov='EC-P')
            return date in ecu_holidays


    def predict(self):
        """
        Checks if vehicle with the specified plate can be on the road on the provided date and time based on the Pico y Placa rules:
        http://www7.quito.gob.ec/mdmq_ordenanzas/Ordenanzas/ORDENANZAS%20A%C3%91OS%20ANTERIORES/ORDM-305-%20%20CIRCULACION%20VEHICULAR%20PICO%20Y%20PLACA.pdf    

        Returns
        -------
        Returns True if the vehicle with the specified plate can be on the road at the specified date and time, otherwise False
        """
        # Check if date is a holiday
        if self.__is_holiday(self.date, self.online):
            return True

        # Check for restriction-excluded vehicles according to the second letter of the plate or if using only two letters
        # https://es.wikipedia.org/wiki/Matr%C3%ADculas_automovil%C3%ADsticas_de_Ecuador
        if self.plate[1] in 'AUZEXM' or len(self.plate.split('-')[0]) == 2:
            return True

        # Check if provided time is not in the forbidden peak hours
        if not self.__is_forbidden_time(self.time):
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
