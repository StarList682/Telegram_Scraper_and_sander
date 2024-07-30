import sys
import asyncio
from telethon import TelegramClient
from PyQt5 import QtWidgets, QtGui, QtCore

class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()
        
        self.setWindowTitle("Telegram Scraper")
        self.setGeometry(100, 100, 600, 500)

        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        
        layout = QtWidgets.QVBoxLayout()

        self.setStyleSheet("""
            QMainWindow {
                background-color: #2E3440;
            }
            QLabel {
                color: #D8DEE9;
                font-size: 14pt;
                margin-bottom: 10px;
            }
            QLineEdit {
                background-color: #3B4252;
                color: #D8DEE9;
                border: 1px solid #4C566A;
                border-radius: 5px;
                padding: 10px;
                font-size: 12pt;
                margin-bottom: 20px;
            }
            QPushButton {
                background-color: #5E81AC;
                color: #ECEFF4;
                border: none;
                border-radius: 5px;
                padding: 10px;
                font-size: 12pt;
                margin-top: 20px;
            }
            QPushButton:hover {
                background-color: #81A1C1;
            }
        """)

        self.api_id_label = QtWidgets.QLabel("API ID")
        layout.addWidget(self.api_id_label)
        self.api_id_input = QtWidgets.QLineEdit(self)
        self.api_id_input.setPlaceholderText("Enter API ID")
        layout.addWidget(self.api_id_input)

        self.api_hash_label = QtWidgets.QLabel("API Hash")
        layout.addWidget(self.api_hash_label)
        self.api_hash_input = QtWidgets.QLineEdit(self)
        self.api_hash_input.setPlaceholderText("Enter API Hash")
        layout.addWidget(self.api_hash_input)

        self.phone_label = QtWidgets.QLabel("Phone Number")
        layout.addWidget(self.phone_label)
        self.phone_input = QtWidgets.QLineEdit(self)
        self.phone_input.setPlaceholderText("Enter Phone Number")
        layout.addWidget(self.phone_input)

        self.chat_id_label = QtWidgets.QLabel("Chat ID")
        layout.addWidget(self.chat_id_label)
        self.chat_id_input = QtWidgets.QLineEdit(self)
        self.chat_id_input.setPlaceholderText("Enter Chat ID")
        layout.addWidget(self.chat_id_input)

        self.message_label = QtWidgets.QLabel("Message")
        layout.addWidget(self.message_label)
        self.message_input = QtWidgets.QLineEdit(self)
        self.message_input.setPlaceholderText("Enter Message")
        layout.addWidget(self.message_input)

        self.scrape_button = QtWidgets.QPushButton("Scrape and Send", self)
        layout.addWidget(self.scrape_button)
        self.scrape_button.clicked.connect(self.start_scraping)

        central_widget.setLayout(layout)

        self.show()
    
    def start_scraping(self):
        api_id = int(self.api_id_input.text())
        api_hash = self.api_hash_input.text()
        phone = self.phone_input.text()
        chat_id = self.chat_id_input.text()
        message = self.message_input.text()
        
        client = TelegramClient(phone, api_id, api_hash)
        
        asyncio.run(self.scrape_and_send(client, phone, chat_id, message))
    
    async def scrape_and_send(self, client, phone, chat_id, message):
        try:

            await client.start(phone)
            if not await client.is_user_authorized():
                code = input("Enter the verification code: ")
                await client.sign_in(phone, code)
            
            participants = await client.get_participants(chat_id)
            for user in participants:
                try:
                    await client.send_message(user.id, message)
                    print(f'Message sent to {user.username}')
                except Exception as e:
                    print(f'Could not send message to {user.username}: {e}')
        except Exception as e:
            print(f'An error occurred: {e}')
        finally:
            await client.disconnect()

app = QtWidgets.QApplication([])
window = Ui()
app.exec_()
