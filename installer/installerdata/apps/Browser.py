import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLineEdit, QToolBar
)
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl, Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PyQt6 Web Browser")
        self.setWindowFlag(Qt.WindowType.WindowStaysOnTopHint, True)
        self.setGeometry(100, 100, 1200, 800)

        # Create the browser widget
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl("https://www.wow.com"))

        # Create the navigation toolbar
        self.navigation_bar = QToolBar()
        self.addToolBar(self.navigation_bar)

        # Add Back button
        back_action = QAction('Back', self)
        back_action.triggered.connect(self.browser.back)
        self.navigation_bar.addAction(back_action)

        # Add Forward button
        forward_action = QAction('Forward', self)
        forward_action.triggered.connect(self.browser.forward)
        self.navigation_bar.addAction(forward_action)

        # Add Refresh button
        refresh_action = QAction('Refresh', self)
        refresh_action.triggered.connect(self.browser.reload)
        self.navigation_bar.addAction(refresh_action)

        # Add Home button
        home_action = QAction('Home', self)
        home_action.triggered.connect(self.navigate_home)
        self.navigation_bar.addAction(home_action)

        # Add the address bar widget
        self.address_bar = QLineEdit()
        self.address_bar.returnPressed.connect(self.navigate_to_url)
        self.navigation_bar.addSeparator()
        self.navigation_bar.addWidget(self.address_bar)

        # Set the central widget
        self.setCentralWidget(self.browser)

        # Update the address bar when the URL changes
        self.browser.urlChanged.connect(self.update_address_bar)

    def navigate_home(self):
        self.browser.setUrl(QUrl("https://www.wow.com"))

    def navigate_to_url(self):
        url = self.address_bar.text()
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url
        self.browser.setUrl(QUrl(url))

    def update_address_bar(self, qurl):
        self.address_bar.setText(qurl.toString())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    QApplication.setApplicationName("PyQt6 Web Browser")
    window = MainWindow()
    window.show()
    sys.exit(app.exec())