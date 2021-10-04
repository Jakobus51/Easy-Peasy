import numpy as np
import time
import csv
import json
import threading
import sys
import datetime

import ProductResearcherV3
import Classes
import Definitions
import mailServer

ordersMail = True
research = True
orders = []

if (ordersMail):
    date = datetime.date(2021, 9, 27)    
    mailServer.getMails(date, orders)

else:      
    name = "Jakob"
    company = "Pandas"
    email = "paarsbadpak@hotmail.nl"
    date  = "01-10-2021"
    package = "Basic" #Basic, Advanced, Complete, Sample
    numberOfProducts = 25 #25, 50, 100
    order = Classes.Order_custom( name, company, email, date, package, numberOfProducts)
    orders.append(order)



#Loop through all orders
for order in orders:
    print("Processing: {} {} - {}\r\n".format(order.fileName, order.package, order.numberOfProducts))
    #Creates folder if not yet exists 
    Definitions.setAndFillFolder(order)
    Definitions.addInstruction(order)

    if(order.generateInvoice):
        print("Generating Invoice:")
        Definitions.generateInvoice(order)

    if (research):  
        ProductResearcherV3.getResults(order)

    print("Run Complete: {} {} - {}\r\n".format(order.fileName, order.package, order.numberOfProducts))
    print("="*100)
    print()

sys.exit("Lekker gewerkt pik!")