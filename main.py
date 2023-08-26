import requests
import time
import datetime
import geocoder
from metar import Metar
import sys
from PyQt6 import QtCore, QtGui, uic, QtWidgets
import pyqtgraph as pg


# Windows installing metar package:
# git clone https://github.com/python-metar/python-metar
# navigate to folder, Windows: C:\Windows\System32\cmd.exe
# run: python setup.py install
# from within the directory 

# Linux installing metar package:
# git clone https://github.com/python-metar/python-metar
# navigate to folder
# run: sudo python setup.py install

qtCreatorFile="metar.ui"
Ui_MainWindow, QtBaseClass=uic.loadUiType(qtCreatorFile)

class MainWindow(Ui_MainWindow, QtBaseClass):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()

        # Set up the user interface from Designer.
        self.setupUi(self)
        
        #set the window title
        self.setWindowTitle("Local Salt Lake Valley METAR")
        
        #Ok button
        self.okButton.clicked.connect(self.reject)
        self.okButton.setAutoDefault(True)
        self.okButton.setDefault(False)
        self.okButton.setText("OK")
        #Cancel Button
        self.cancelButton.clicked.connect(self.reject)
        self.cancelButton.setAutoDefault(False)
        self.cancelButton.setDefault(False)
        self.cancelButton.setText("Cancel")

def main():
    #create app
    app = QtWidgets.QApplication(sys.argv)
    #create and show the window
    main = MainWindow()
    main.show()
    #start the app
    sys.exit(app.exec())

def aviationWeatherAPI():
    starttime = time.time()
    myLocation = geocoder.ip('me')
    loopDuration : int = 5
    
    #collect data from the aviationweather.gov api. 
    multiRequest = requests.get("https://beta.aviationweather.gov/cgi-bin/data/metar.php?ids=KSLC,KTVY,KU42")
    airportMetars = multiRequest.text.splitlines()
    SLCmetar = Metar.Metar(airportMetars[0])
    print(airportMetars[0])
    metarDecoder(SLCmetar)

def metarDecoder(metar : Metar.Metar):
    # The 'station_id' attribute is a string.
    print("station: %s" % metar.station_id)

    if metar.type:
        print("type: %s" % metar.report_type())

    # The 'time' attribute is a datetime object
    if metar.time:
        print("time: %s" % metar.time.ctime())

    # The 'temp' and 'dewpt' attributes are temperature objects
    if metar.temp:
        print("temperature: %s" % metar.temp.string("C"))

    if metar.dewpt:
        print("dew point: %s" % metar.dewpt.string("C"))

    # The wind() method returns a string describing wind observations
    # which may include speed, direction, variability and gusts.
    if metar.wind_speed:
        print("wind: %s" % metar.wind())

    # The peak_wind() method returns a string describing the peak wind
    # speed and direction.
    if metar.wind_speed_peak:
        print("wind: %s" % metar.peak_wind())

    # The visibility() method summarizes the visibility observation.
    if metar.vis:
        print("visibility: %s" % metar.visibility())

    # The runway_visual_range() method summarizes the runway visibility
    # observations.
    if metar.runway:
        print("visual range: %s" % metar.runway_visual_range())

    # The 'press' attribute is a pressure object.
    if metar.press:
        print("pressure: %s" % metar.press.string("mb"))

    # The 'precip_1hr' attribute is a precipitation object.
    if metar.precip_1hr:
        print("precipitation: %s" % metar.precip_1hr.string("in"))

    # The present_weather() method summarizes the weather description (rain, etc.)
    print("weather: %s" % metar.present_weather())

    # The sky_conditions() method summarizes the cloud-cover observations.
    print("sky: %s" % metar.sky_conditions("\n     "))

    # The remarks() method describes the remark groups that were parsed, but
    # are not available directly as Metar attributes.  The precipitation,
    # min/max temperature and peak wind remarks, for instance, are stored as
    # attributes and won't be listed here.
    if metar._remarks:
        print("remarks:")
        print("- " + metar.remarks("\n- "))   
    
# while True:
#     print(f"Current Location: {myLocation.city}")
#     print(f"Latitude + Longitude: {myLocation.latlng}")
#     print(multiRequest)
#     print()
    
#     time.sleep(loopDuration - ((time.time() - starttime) % loopDuration))    

if __name__ == "__main__":
    aviationWeatherAPI()
    main()