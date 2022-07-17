#Python webserver
from flask import Flask, render_template
from flask_restful import Api, Resource
import utilities

app = Flask(__name__)
api = Api(app)

############# Model #################
# Currently no database             #
# This is where sqlalchemy would go #
#                                   #
#####################################

############# Service ###############
# Contains REST api services        #
#                                   #
#####################################
class TemperatureConverterAPI(Resource):
    @classmethod
    def get(self, degrees):
        degrees_cels = str()
        degrees_fahr = str()
        validator = utilities.Validator()
        results = []

        degrees = validator.escape_characters(degrees)
        if validator.is_valid_number(degrees):
            t = utilities.TemperatureConverter()
            degrees_fahr= format(t.celsius_to_fahrenheit(float(degrees)), ".1f")
            degrees_cels = format(t.fahrenheit_to_celsius(float(degrees)), ".1f")
            
            #Convert input for consistent formatting
            degrees = format(float(degrees), ".1f")
            
            results.append({"celsius-to-fahrenheit": {"celsius" : degrees, "fahrenheit" : degrees_fahr}})
            results.append({"fahrenheit-to-celsius": {"fahrenheit" : degrees, "celsius" : degrees_cels}})
        else:
            results.append({"error": "invalid argument"})
        return results

############# Controller ############# 
# Contains the endpoints/routes      #
#                                    #
######################################
api.add_resource(TemperatureConverterAPI, "/api/tempconverter/<degrees>")

@app.route("/")
def home():
    return render_template("index.html")

############# Main ##################################################
# Uncomment if running server locally.                              #
# Run "python3 app.py" in terminal to start local server.           #
# In this case below, it will be open to localhost port 5000        #
# port argument is optional since Flask will default to port 5000   #
# URL might look something like http://127.0.0.1:5000               #
#####################################################################
if __name__ == '__main__':
    app.run(debug=True)