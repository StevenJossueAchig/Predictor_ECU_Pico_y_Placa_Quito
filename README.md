# pico-y-placa

A "Pico y Placa" predictor. The inputs are a license plate number (the full number, not the last digit), a date (as a String), and a time, and the program returns whether or not that car can be on the road on the specified date and time.
This predictor is developed according to the regulations of [the Municipal Ordinance of Quito No. 0305](http://www7.quito.gob.ec/mdmq_ordenanzas/Ordenanzas/ORDENANZAS%20A%C3%91OS%20ANTERIORES/ORDM-305-%20%20CIRCULACION%20VEHICULAR%20PICO%20Y%20PLACA.pdf).


## Requirements

The following libraries are required:

* [requests](https://pypi.org/project/requests/)

* [holidays](https://pypi.org/project/holidays/)

If you wish to use the [abstract Public Holidays API](https://www.abstractapi.com/holidays-api), save the API key in the enviroment variable HOLIDAYS_API_KEY. Note that this API excludes the rules of [Reform Law to the LOSEP (in force since December 21, 2016 /R.O # 906)](https://biblioteca.defensoria.gob.ec/bitstream/37000/1683/1/LEY%20ORG%C3%81NICA%20REFORMATORIA%20A%20LA%20LEY%20ORG%C3%81NICA%20DEL%20SERVICIO%20P%C3%9ABLICO%20Y%20AL%20C%C3%93DIGO%20DEL%20TRABAJO.pdf) related to the Holidays in Ecuador. Nevertheless, the offline mode of the “Pico y Placa” predictor considers all rules of the law mentioned above.

## Usage

```
usage: pico_y_placa.py [-h] [-o] -p PLATE -d DATE -t TIME

Pico y Placa Quito Predictor: Check if the vehicle with the provided plate can be on the road on the provided date and time

optional arguments:
  -h, --help            show this help message and exit
  -o, --online          use abstract's Public Holidays API
  -p PLATE, --plate PLATE
                        the vehicle's plate: XXX-YYYY or XX-YYYY, where X is a capital letter and Y is a digit
  -d DATE, --date DATE  the date to be checked: YYYY-MM-DD
  -t TIME, --time TIME  the time to be checked: HH:MM
```
## Note 1. Format of the input data
```
Plate: following the [Ecuador car license plate format](https://es.wikipedia.org/wiki/Matr%C3%ADculas_automovil%C3%ADsticas_de_Ecuador), the parameter “Plate” should have this format: *XXX-YYY*  (commercial, government, official, and private vehicles) or *XX-YYYY* (diplomatic service and temporary hospitalization vehicles), where X is a capital letter, and Y is a digit. Example: *EBA-0234*, *CC-0012.*
Date: considering the [ISO 8601](https://es.wikipedia.org/wiki/ISO_8601), the parameter “Date” should have the following format: *YYYY-MM-DD*. Examples: *2021-04-24*, *2020-09-10.*
Time: the time must always be represented under the 24h system, that is, the number of hours that have elapsed since midnight. The 12h format is not allowed. Format: *HH:MM*, where HH and MM should be composed of two digits, respectively. Examples: *12:30, 21:10, 09:05, 00:00 (midnight).*
To use the [abstract Public Holidays API](https://www.abstractapi.com/holidays-api) add the flag -o or --online. Otherwise, the predicator will use the class “HolidayEcaudor” to check if a date is a holiday or not.  The default option is offline.  
```

## Example

```
$ python pico_y_placa.py -p EBA-0234 -d 2021-04-23 -t 15:15
The vehicle with plate EBA-0234 CAN be on the road on 2021-04-23 at 15:15.
```

## Automated Testing

[test.py](https://github.com/mmacas11/Predictor_ECU_Pico_y_Placa_Quito/blob/main/test.py) is used for executing unit tests automatically. The primary purpose is to confirm that each unit of the software code performs as expected. Unit Testing was done during the development (coding phase) of the predictor.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
