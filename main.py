import requests
import time
import datetime
import geocoder
from metar import Metar
import sys
from PyQt5 import QtCore, QtGui, uic, QtWidgets
import pyqtgraph as pg

# Windows installing metar package:
# git clone https://github.com/python-metar/python-metar
# navigate to folder, Windows(C:) > Users > "name" > python.metar
# run: python setup.py install
# from within the directory 

# Linux installing metar package:
# git clone https://github.com/python-metar/python-metar
# navigate to folder
# run: sudo python setup.py install

qtCreatorFile="metar.ui"
# Ui_MainWindow, QtBaseClass=uic.loadUiType(qtCreatorFile)

class MainWindow(QtWidgets.QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi(qtCreatorFile, self)

        # Set up the user interface from Designer.
        # self.setupUi(self)
        
        #set the window title
        self.setWindowTitle("Local Salt Lake Valley METAR")
        #Ok button
        self.okButton = self.findChild(QtWidgets.QPushButton, "okButton")
        self.okButton.setProperty("text", "OK")
        self.okButton.setProperty("autoDefault", True)
        self.okButton.setProperty("default", False)
        self.okButton.clicked.connect(self.reject)
        #Cancel Button
        self.cancelButton = self.findChild(QtWidgets.QPushButton, "cancelButton")
        self.cancelButton.setProperty("text", "Cancel")
        self.cancelButton.setProperty("autoDefault", False)
        self.cancelButton.setProperty("default", False)
        self.cancelButton.clicked.connect(self.reject)
        
        # #initialize each label for first metar
        # self.stationLabel.setText(SLCMetar.station_id)
        # self.metarTime.setText(SLCMetar.time.ctime())
        # self.temperature.setText("Temperature: " + SLCMetar.temp.string("C"))
        # self.dewPoint.setText("Dew Point: " + SLCMetar.dewpt.string("C"))
        # self.visibility.setText("Visibility: " + SLCMetar.visibility())
        # self.altimeter.setText("Altimeter: " + SLCMetar.press.string() + " of Hg")
        # self.wind.setText("Wind: " + SLCMetar.wind_speed.string("kt"))
        # self.gusts.setText("Gusts: " + str(SLCMetar.wind_gust))
        # self.weather.setText("Weather: " + SLCMetar.present_weather())
        # self.weatherBox.setMarkdown("" + SLCMetar.sky_conditions())
        # self.remarksBox.setMarkdown("" + SLCMetar.remarks())
        
        self.worker = WorkerThread()
        self.worker.start()
        self.worker.update_progress.connect(self.updateAPIValues)#sends emitted variable to the function
        
    def updateAPIValues(self, listOfMetars): #listOfMetars is the emitted var
        currMetar : Metar.Metar = listOfMetars[0]
        
        # main atmospheric labels
        self.stationLabel = self.findChild(QtWidgets.QLabel, "stationLabel")
        self.stationLabel.setProperty("text", currMetar.station_id)
        self.temperature = self.findChild(QtWidgets.QLabel, "temperature")
        self.temperature.setProperty("text", "Temperature: %s" % currMetar.temp.string("C"))
        self.dewPoint = self.findChild(QtWidgets.QLabel, "dewPoint")
        self.dewPoint.setProperty("text", "Dew Point: %s" % currMetar.dewpt.string("C"))
        self.visibility = self.findChild(QtWidgets.QLabel, "visibility")
        self.visibility.setProperty("text", "Visibility: %s" % currMetar.visibility())
        self.altimeter = self.findChild(QtWidgets.QLabel, "altimeter")
        self.altimeter.setProperty("text", "Altimeter: %s Hg" % currMetar.press.string("IN"))
        self.wind = self.findChild(QtWidgets.QLabel, "wind")
        self.wind.setProperty("text", "Wind: %s at %s" % (currMetar.wind_speed , currMetar.wind_dir))
        self.gusts = self.findChild(QtWidgets.QLabel, "gusts")
        self.gusts.setProperty("text", "Gusts: %s" % currMetar.wind_gust)
        
        # text boxes for "Weather" and "Remarks" labels
        self.weatherLabel = self.findChild(QtWidgets.QLabel, "weather")
        self.weatherLabel.setProperty("text", "Weather:")
        self.weatherBox = self.findChild(QtWidgets.QTextBrowser, "weatherBox")
        self.weatherBox.setProperty("markdown", '%s %s'% (currMetar.present_weather(), currMetar.sky_conditions()))
        self.remarksLabel = self.findChild(QtWidgets.QLabel, "remarks")
        self.remarksLabel.setProperty("text", "Remarks:")
        self.remarksBox = self.findChild(QtWidgets.QTextBrowser, "remarksBox")
        self.remarksBox.setProperty("markdown", "\n- %s" % currMetar.remarks("\n- "))
        
        
        metarDecoder(currMetar)

class WorkerThread(QtCore.QThread):
    update_progress = QtCore.pyqtSignal(list)
    loopDuration : int = 5 #Unit: sec
    starttime = time.time()
    emittedList = []
    def run(self):
        while True:
            emittedList = aviationWeatherAPI()
            self.update_progress.emit(emittedList)
            time.sleep(self.loopDuration - ((time.time() - self.starttime) % self.loopDuration)) 
            
            
        
def main():
    #create app
    app = QtWidgets.QApplication(sys.argv)
    #create and show the window
    main = MainWindow()
    
    with open("stylesheet.qss","r") as file:
        app.setStyleSheet(file.read())
        
    main.show()
    
    #start the app
    sys.exit(app.exec())

def aviationWeatherAPI():
    #collect data from the aviationweather.gov api. 
    multiRequest = requests.get("https://beta.aviationweather.gov/cgi-bin/data/metar.php?ids=KSLC,KTVY,KU42")
    airportMetars = multiRequest.text.splitlines()
    result : list = []
    for element in airportMetars:
        result.append(Metar.Metar(element))
    return result

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

if __name__ == "__main__":
    aviationWeatherAPI()
    main()