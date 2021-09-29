import numpy as np
import pandas as pd
import bs4
import time
import csv


import requests
import json
import threading
import sys

import ProductResearcherV3
import Classes
import Definitions


invoice = True
numberOfProducts = 100 #25, 50, 100

research = False
name = "Daniel"
company = "Consultancy group"
date  = "28-09-2021"
package = "Basic" #Basic, Advanced, Complete, Sample

#Creates the order with all atributes needed throughout the script
Order = Classes.Order( name, company, date, package, numberOfProducts)

#Creates folder if not yet exists 
Definitions.setAndFillFolder(Order)   

if(invoice):
    Definitions.generateInvoice(Order)

if (research):  
    ProductResearcherV3.getResults(Order)

sys.exit("Lekker gewerkt pik! \n{} package: {}".format(Order.package, Order.fileName))


