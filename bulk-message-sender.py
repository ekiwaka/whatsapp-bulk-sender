import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep

class WhatsAppBulkSender:
    def __init__(self):
        self.driver = None
        self.contacts = []

    def initialize_driver(self):
        try:
            self.driver = webdriver.Chrome()  # Change the path if using a different browser driver
            self.driver.get("https://web.whatsapp.com")
            input("Scan the QR code and press Enter to continue...")
        except Exception as e:
            print("Error initializing the browser:", str(e))

    def read_excel_sheet(self, file_path):
        try:
            df = pd.read_excel(file_path)
            self.contacts = df['Contact'].tolist()
        except Exception as e:
            print("Error reading Excel sheet:", str(e))

    def send_messages(self, message):
        try:
            for contact_number in self.contacts:
                self.send_message(contact_number, message)
                sleep(5)  # Add a delay to prevent detection as a bot
        except Exception as e:
            print("Error sending messages:", str(e))

    def send_message(self, contact_number, message):
        try:
            self.driver.get(f"https://web.whatsapp.com/send?phone={contact_number}&text={message}")
            sleep(5)  # Wait for the chat to load
            send_button = self.driver.find_element_by_xpath('//span[@data-icon="send"]')
            send_button.click()
        except Exception as e:
            print("Error sending message:", str(e))

    def close(self):
        if self.driver:
            self.driver.quit()

# Usage
sender = WhatsAppBulkSender()
try:
    sender.initialize_driver()
    sender.read_excel_sheet('contacts.xlsx')  # Provide the path to the Excel file
    message = "Hello! This is a sample message."
    sender.send_messages(message)
finally:
    sender.close()
