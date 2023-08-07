'''          _                      _    
            | |           @tt 2023 | |   
  _ __   ___| |___      _____  _ __| | __
 | '_ \/ _ \ __\ \ /\ / / _ \| '__| |/ /
 | | | |  __/ |_ \ V  V / (_) | |' |   < 
 |_| |_|\___|\__| \_/\_/ \___/|_|  |_|\_\
   ┬ ┬┌─┐┌┬┐┌─┐┬ ┬  ,,__   ┌─┐┬┌─
   │││├─┤ │ │  ├─┤ c''  )' ├─┘││ ┬
   └┴┘┴ ┴ ┴ └─┘┴ ┴  ''-''  ┴  ┴└─┘
                          

find this app helpful? ... 
cashapp@travisodellart or paypal.me/odellcreativegroup

'''


import sys 
from PySide6 import QtCore, QtGui, QtWidgets 
 
class NetworkMonitor(QMenu): 
    def __init__(self): 
        super().__init__() 
        self.networks = [] 
 
        for interface in QNetworkInterface.allInterfaces(): 
            self.networks.append(NetworkItem(interface)) 
 
        for network in self.networks: 
            self.addAction(network.action) 
 
        self.addSeparator() 
 
        action = QAction("Add Network...", self) 
        action.triggered.connect(self.addNetwork) 
 
        self.addAction(action) 
 
    def addNetwork(self): 
        dialog = NetworkDialog() 
        if dialog.exec_(): 
            network = NetworkItem(dialog.interface, dialog.name, dialog.bridge) 
            self.addAction(network.action) 
 
class NetworkItem(QAction): 
    def __init__(self, interface, name="", bridge=False): 
        super().__init__(interface.name) 
        self.interface = interface 
        self.name = name 
        self.bridge = bridge 
 
        self.uplink = 0 
        self.downlink = 0 
 
        self.update() 
 
    def update(self): 
        self.uplink = self.interface.statistics().rxBytes() / 1024 
        self.downlink = self.interface.statistics().txBytes() / 1024 
 
        self.setText(f"{self.name} ({self.uplink:.2f}kbps / {self.downlink:.2f}kbps)") 
 
    def status(self): 
        if self.interface.isUp(): 
            if self.interface.isRunning(): 
                return "active" 
            else: 
                return "idle" 
        else: 
            return "not-active" 
 
    def statusIcon(self): 
        if self.status() == "active": 
            return "✅" 
        elif self.status() == "idle": 
            return "⏲️" 
        elif self.status() == "not-active": 
            return "❌" 
 
class NetworkDialog(QDialog): 
    def __init__(self): 
        super().__init__() 
 
        self.interface = QComboBox() 
        self.interface.addItems([interface.name for interface in QNetworkInterface.allInterfaces()]) 
 
        self.name = QLineEdit() 
 
        self.bridge = QCheckBox("Bridge") 
 
        buttonBox = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel) 
        buttonBox.accepted.connect(self.accept) 
        buttonBox.rejected.connect(self.reject) 
 
        layout = QVBoxLayout() 
        layout.addWidget(self.interface) 
        layout.addWidget(self.name) 
        layout.addWidget(self.bridge) 
        layout.addWidget(buttonBox) 
 
        self.setLayout(layout) 
 
    def getInterface(self): 
        return self.interface.currentText() 
 
    def getName(self): 
        return self.name.text() 
 
    def isBridge(self): 
        return self.bridge.isChecked() 
 
if __name__ == "__main__": 
    app = QApplication(sys.argv) 
    menu = NetworkMonitor() 
    menu.show() 
    sys.exit(app.exec_()) 
