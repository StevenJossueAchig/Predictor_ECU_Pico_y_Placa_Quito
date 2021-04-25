# pico-y-placa

A "Pico y Placa" predictor. The inputs are a license plate number (the full number, not the last digit), a date (as a String), and a time, and the program returns whether or not that car can be on the road on the specified date and time.
This predictor is developed according to the regulations of [the Municipal Ordinance of Quito No. 0305](http://www7.quito.gob.ec/mdmq_ordenanzas/Ordenanzas/ORDENANZAS%20A%C3%91OS%20ANTERIORES/ORDM-305-%20%20CIRCULACION%20VEHICULAR%20PICO%20Y%20PLACA.pdf).


## Requirements

The following libraries are required:

* [requests](https://pypi.org/project/requests/)

* [holidays](https://pypi.org/project/holidays/)

If you wish to use the [abstract Public Holidays API](https://www.abstractapi.com/holidays-api), save the API key in the enviroment variable HOLIDAYS_API_KEY.

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

## Example

```
$ python pico_y_placa.py -p EBA-0234 -d 2021-04-23 -t 15:15
The vehicle with plate EBA-0234 CAN be on the road on 2021-04-23 at 15:15.
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details
