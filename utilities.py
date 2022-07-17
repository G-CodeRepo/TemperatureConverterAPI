import re
import urllib

#Business level classes
class TemperatureConverter():
    @classmethod
    def celsius_to_fahrenheit(self, degrees_cel):
        return (degrees_cel * 1.8)+ 32
    
    @classmethod
    def fahrenheit_to_celsius(self, degrees_fahr):
        return (degrees_fahr - 32) / 1.8

class Validator():
    @classmethod
    def is_valid_number(self, number):
        return re.search('^[-]*[0-9]+[.]*[0-9]*$', number)

    @classmethod
    def escape_characters(self, number):
        return urllib.parse.quote(number)