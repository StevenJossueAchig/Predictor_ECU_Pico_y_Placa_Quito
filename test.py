import unittest
import requests
import os
from datetime import datetime
from src.pico_y_placa import PicoPlaca


class TestPicoYPlaca(unittest.TestCase):

    def test_invalid_plate(self):
        """
        Test that invalid plate raises ValueError
        """
        plate = 'A-123'
        now = datetime.now()
        date, tm = now.strftime("%Y-%m-%d %H:%M").split()
        with self.assertRaises(ValueError):
            result = PicoPlaca(plate, date, tm).predict()

    def test_invalid_date(self):
        """
        Test that invalid date raises ValueError
        """
        plate = 'EBA-0234'  # private vehicle
        now = datetime.now()
        date, tm = now.strftime("%d/%m/%Y %H:%M").split()
        with self.assertRaises(ValueError):
            result = PicoPlaca(plate, date, tm).predict()

    def test_invalid_time(self):
        """
        Test that invalid time raises ValueError
        """
        plate = 'EBA-0234'  # private vehicle
        now = datetime.now()
        date, tm = now.strftime("%Y-%m-%d %H:%M:%S").split()
        with self.assertRaises(ValueError):
            result = PicoPlaca(plate, date, tm).predict()

    def test_missing_key(self):
        """
        Test that missing API key raises requests.HTTPError
        """
        plate = 'EBA-0234'  # private vehicle
        now = datetime.now()
        date, tm = now.strftime("%Y-%m-%d %H:%M").split()
        try:
            del os.environ['HOLIDAYS_API_KEY']
        except KeyError:
            pass
        with self.assertRaises(requests.HTTPError):
            result = PicoPlaca(plate, date, tm, online=True).predict()


    def test_holiday(self):
        """
        Test that holidays are not restricted
        """
        date = '2021-12-25'  # Christmas
        plate = "EBA-0234"  # private vehicle
        tm = '08:30'  # within peak hours
        result = PicoPlaca(plate, date, tm).predict()
        self.assertTrue(result)

    def test_weekend(self):
        """
        Test that weekends are not restricted
        """
        date = '2021-04-24'  # Saturday
        plate = 'EBA-0234'  # private vehicle
        tm = '08:30'  # within peak hours
        result = PicoPlaca(plate, date, tm).predict()
        self.assertTrue(result)

    def test_outside_peak_hours(self):
        """
        Test that time outside of not peak hours are not restricted
        """
        date = '2021-04-19'  # Monday
        plate = 'EBA-0232'  # private vehicles' plates ending with 2 are restricted on Mondays
        tm = '15:30'  # outside peak hours
        result = PicoPlaca(plate, date, tm).predict()
        self.assertTrue(result)

    def test_vehicle(self):
        """
        Test that public vehicles are not restricted
        """
        date = '2021-04-19'  # Monday
        # Governmental vehicle, plate ending in 1 (normally restricted on Mondays)
        plate = 'PEB-0001'
        tm = '08:30'  # within peak hours
        result = PicoPlaca(plate, date, tm).predict()
        self.assertTrue(result)

    def test_restricted(self):
        """
        Test restricted case
        """
        date = '2021-04-19'  # Monday
        plate = 'EBA-0232'  # private vehicles' plates ending with 2 are restricted on Mondays
        tm = '19:00'  # within peak hours
        result = PicoPlaca(plate, date, tm).predict()
        self.assertFalse(result)
        

if __name__ == '__main__':
    unittest.main()
