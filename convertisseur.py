from PySide2.QtWidgets import (QWidget, QHBoxLayout, QLabel, QApplication, QComboBox, QLineEdit)
from PySide2.QtGui import QPalette
from PySide2.QtCore import Qt
from currency_converter import CurrencyConverter
import sys


class Converter(QWidget):
    def __init__(self):
        QWidget.__init__(self)

        self.c = CurrencyConverter(fallback_on_wrong_date=True)

        self.setWindowTitle('Converter')

        self.activefirstChoice = QLabel("", self)
        self.activelastChoice = QLabel("", self)
        self.firstValue = QLineEdit("0", self)
        self.lastValue = QLineEdit("0", self)

        self.firstChoice = QComboBox()
        self.lastChoice = QComboBox()

        layout = QHBoxLayout()
        layout.addWidget(self.firstChoice)
        layout.addWidget(self.firstValue)
        layout.addWidget(self.lastChoice)
        layout.addWidget(self.lastValue)
        self.setLayout(layout)

        for key in sorted(self.c.currencies):
            self.firstChoice.addItem(key)
            self.lastChoice.addItem(key)

        self.firstChoice.activated[str].connect(self.onchangefirstChoice)
        self.firstValue.textChanged[str].connect(self.onchangefirstValue)
        self.lastChoice.activated[str].connect(self.onchangelastChoice)
        self.lastValue.textChanged[str].connect(self.onchangelastValue)

    def onchangefirstChoice(self, text):
        self.activefirstChoice = text

    def onchangefirstValue(self, text):
        if text == "":
            self.firstValue.setText("0")
        else:
            self.lastValue.blockSignals(True)
            self.firstValue.setText(text)
            value = str(self.c.convert(float(text),str(self.firstChoice.currentText()),str(self.lastChoice.currentText())))
            print(value)
            self.lastValue.setText(value)
            self.lastValue.blockSignals(False)
            self.lastValue.adjustSize()

    def onchangelastChoice(self, text):
        self.activelastChoice = text

    def onchangelastValue(self, text):
        if text != "":
            self.firstValue.blockSignals(True)
            self.lastValue.setText(text)
            value = str(self.c.convert(float(text),str(self.firstChoice.currentText()),str(self.lastChoice.currentText())))
            print(value)
            self.firstValue.setText(value)
            self.firstValue.blockSignals(False)
            self.firstValue.adjustSize()
        else:
            self.lastValue.setText("0")

app = QApplication.instance()

if not app:
    app = QApplication(sys.argv)
    currency = Converter()
    currency.show()
app.exec_()