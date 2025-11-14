import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

class main(QMainWindow):
    def __init__(self):
        super(main, self).__init__()
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('https://www.google.com/'))
        self.setCentralWidget(self.browser)
        self.showMaximized()

        #nav
        nav = QToolBar()
        self.addToolBar(nav)

        back = QAction('Back', self)
        back.triggered.connect(self.browser.back)
        nav.addAction(back)

        forward = QAction('Forward', self)
        forward.triggered.connect(self.browser.forward)
        nav.addAction(forward)

        rl = QAction('Reload', self)
        rl.triggered.connect(self.browser.reload)
        nav.addAction(rl)

        home = QAction('Home', self)
        home.triggered.connect(self.navigate_home)
        nav.addAction(home)

        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigate_url)
        nav.addWidget(self.url_bar)

        self.browser.urlChanged.connect(self.update)

        self.download_button = QPushButton("Download 0%")
        self.download_button.setFixedWidth(120)
        nav.addWidget(self.download_button)

        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #3f3478,
                    stop:1 #3f3478
                );
                background-repeat: no-repeat;
                color: black;
                border: transparent;
                font-family: 'Segoe UI';
            }
        QMainWindow{
            background: #2c255c;                   
        }
        QLineEdit {
            background: #2c255c;
            color: white;
            border: 2px solid #5c4fb2;
            border-radius: 12px;
            padding: 6px 10px;
            min-height: 28px;
            font-size: 14px;
        }
        QLineEdit:focus {
            border: 2px solid #8c7fff;
            background: #3a3278;
        }
""")

    # Styling opsional
        self.download_button.setStyleSheet("""
        QPushButton {
            background-color: #2c255c;
            border-radius: 8px;
            padding: 5px;
            color: white;
        }
    """)

        profile = self.browser.page().profile()
        profile.downloadRequested.connect(self.on_download)

    def on_download(self, download):
        path, _ = QFileDialog.getSaveFileName(
            self, "Save File", download.downloadFileName()
        )

        if not path:
            return

        download.setPath(path)
        download.accept()

        download.downloadProgress.connect(self.update_download_progress)

        download.finished.connect(lambda: self.download_button.setText("Download Done"))

    def update_download_progress(self, received, total):
        if total > 0:
            percent = int((received / total) * 100)
            self.download_button.setText(f"Downloading {percent}%")


    def navigate_home(self):
        self.browser.setUrl(QUrl('https://google.com'))
    
    def navigate_url(self):
        url = self.url_bar.text()
        self.browser.setUrl(QUrl(url))

    def update(self, url):
        self.url_bar.setText(url.toString())

app = QApplication(sys.argv)
QApplication.setApplicationName('RangS Browser')
window = main()
app.exec_()
