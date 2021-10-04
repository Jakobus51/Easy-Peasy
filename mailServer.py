from imap_tools import MailBox, AND
import datetime
import bs4
from bs4 import BeautifulSoup as soup
import os
import Classes
import re

def getMails(date, orders):

    # get list of email subjects from INBOX folder
    with MailBox("mail.easypeasytechnology.com").login("info@EasyPeasyTechnology.com", "SqueezyLemon15?") as mailbox:
        print("Succesfully logged into mailbox.")
        
        #Fetch all free samples
        for msg in  mailbox.fetch(AND(date_gte=date, subject="Free Sample (Forms)")):

            cleantext = soup(msg.html, "html.parser").text
            cleantext = os.linesep.join([s for s in cleantext.splitlines() if s]) 
            text = cleantext.split("\r\n")
            text.pop()

            name = text[2]
            company = text[4]
            email = text[6]
            productList = text[8:]
            dateOrder = msg.date.date()
            package = "Sample"
            numberOfProducts = 10

            order = Classes.Order(name, company, email, dateOrder, package, numberOfProducts, productList, "")
            orders.append(order)
        numberOfFreeSamples = len(orders)
        print("({}) free sample orders retrieved.".format(numberOfFreeSamples))
           
        #Fetch all Orders        
        for msg in  mailbox.fetch(AND(date_gte=date, subject="Order (Forms)")):

            cleantext = soup(msg.html, "html.parser").text
            cleantext = os.linesep.join([s for s in cleantext.splitlines() if s]) 
            text = cleantext.split("\r\n")
            text.pop()

            name = text[2]
            company = text[4]
            email = text[6]
            package = text[8]
            numberOfProducts = int(text[10])
            message = text[14:]
            dateOrder = msg.date.date()
           
            order = Classes.Order(name, company, email, dateOrder, package, numberOfProducts, "", message)
            orders.append(order)
        numberOfOrders = len(orders) #- numberOfFreeSamples
        print("({}) real orders retrieved.".format(numberOfOrders))
        print("All mails fetched from {} onwards.\r\n".format(date))
        print("="*100)
        print()


    
    