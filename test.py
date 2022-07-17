import pytest
import requests
import json

# Server running on localhost on port 5000 (Make sure that server is running in the correct port)
BASE = "http://127.0.0.1:5000/"

# Hosted endpoint online
#BASE = "https://mypyground.pythonanywhere.com/"

def test_home_page():
    response = requests.get(BASE)
    assert response.status_code == 200

#Test base url
@pytest.mark.parametrize("nav", ["garbage", "cat", "dog", "wallaby", "10-53", "10A", "-B5", "    ", "   53   ", "select * from customers where 1 = 1", "<script>alert('this is javascript')</script>"])
def test_navigation_fail(nav):
    response = requests.get(BASE + nav)
    assert response.status_code != 200

#Test celsius to fahrenheit results
@pytest.mark.parametrize("degrees, result", [(100, 212.0), (300, 572.0), (0, 32.0), (50.5, 122.9), (-30, -22.0), (-70, -94.0)])
def test_celsius_parameters_pass(degrees, result):
    response = requests.get(BASE + "api/tempconverter/" + str(degrees))
    token = json.loads(response.text)
    degrees = format(float(degrees), ".1f")
    result = str(result)
    assert token[0]["celsius-to-fahrenheit"]["celsius"] == degrees and token[0]["celsius-to-fahrenheit"]["fahrenheit"] == result

#Test fahrenheit to celsius results
@pytest.mark.parametrize("degrees, result", [(212.0, 100.0), (572.0, 300.0), (32.0, 0.0), (122.9, 50.5), (-22.0, -30.0), (-94.0, -70.0)])
def test_fahrenheit_parameters_pass(degrees, result):
    response = requests.get(BASE + "api/tempconverter/" + str(degrees))
    token = json.loads(response.text)
    degrees = format(float(degrees), ".1f")
    result = str(result)
    assert token[1]["fahrenheit-to-celsius"]["fahrenheit"] == degrees and token[1]["fahrenheit-to-celsius"]["celsius"] == result

#Test invalid degrees from api endpoint
@pytest.mark.parametrize("degrees", ["garbage", "cat", "dog", "wallaby", "10-53", "10A", "-B5", "    ", "   53   ", "select * from customers where 1 = 1"])
def test_parameters_fail(degrees):
    response = requests.get(BASE + "api/tempconverter/" + str(degrees))
    token = json.loads(response.text)
    assert token[0]["error"] == "invalid argument"

#Test empty argument
def test_no_parameters_fail():
    response = requests.get(BASE + "api/tempconverter/" + "")
    assert response.status_code != 200

#Test slashes
@pytest.mark.parametrize("degrees", ["/", "<script>alert('this is javascript')</script>", '/', "\//", '//'])
def test_escape_characters_fail(degrees):
    response = requests.get(BASE + "api/tempconverter/" + degrees)
    assert response.status_code != 200

#Test special characters and invalid slashes
@pytest.mark.parametrize("degrees", ['\n', '\\', '\t'])
def test_escape_characters_fail(degrees):
    response = requests.get(BASE + "api/tempconverter/" + degrees)
    token = json.loads(response.text)
    assert token[0]["error"] == "invalid argument"