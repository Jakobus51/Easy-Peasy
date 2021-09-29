import numpy as np
import pandas as pd
import bs4
import time
import csv
import requests
import json
import threading
import sys
import Definitions as defi
import xlsxwriter



def getResults(order):
	tic = time.perf_counter()
	print("\n{} package: {}".format(order.package, order.fileName))		

	if(order.package == "Sample" or order.package == "Complete"):
			products = Complete(order)
	if(order.package == "Advanced"):
			products = Advanced(order)
	if(order.package == "Basic"):
			products = Basic(order)

	products = products.sort_values(by=["Originele Product", "Resultaten-Zoekvolume Ratio \n(1 Maand)"], ascending=[True, False])

	#write to an excel
	defi.writeExcel(order, products)
	
	order.totalTimeResearch = time.perf_counter()-tic 
	order.averageTime = order.totalTimeResearch/ order.numberOfProductsScript

	print()
	print(f"Runtime: {order.totalTimeResearch:0.2f} seconds")
	print(f"Average time per product: {order.averageTime:0.2f} seconds")	




def Basic(order):
	ticLocal = time.perf_counter()
	column_names =["Originele Product",					
					"Resultaten op Bol",
					"Zoekvolume \n(1 Maand)",
					"Zoekvolume \n(3 Maanden)",					
					"Resultaten-Zoekvolume Ratio \n(1 Maand)",
					"Resultaten-Zoekvolume Ratio \n(3 Maanden)"]

	products = pd.read_csv("C:/Users/Jakob/Documents/EasyPeasy/Resultaten/{}/{}.csv".format(order.fileName,order.fileName), names=column_names)
	accestoken = defi.GetAccessToken()
	accestokenStartTime = time.perf_counter()

	count= 1
	order.numberOfProductsScript =  len(products["Originele Product"])
	print("Number of products: {}\n".format(order.numberOfProductsScript))

	for product in products["Originele Product"]:

		#Get new token after 260 seconds
		if time.perf_counter() - accestokenStartTime >260:
			accestokenStartTime = time.perf_counter()
			accestoken = defi.GetAccessToken()

		tictic = time.perf_counter()

		#Get Bol results
		bolResults = defi.GetBolResult(product)
		products.loc[(products["Originele Product"] == product), "Resultaten op Bol"] = bolResults[0]

		#1 Month results
		searchResults1Month = defi.GetSearchResults(accestoken, product, "DAY", 30)
		products.loc[products["Originele Product"] == product, "Zoekvolume \n(1 Maand)"] = searchResults1Month["searchTerms"]["total"]

		#3 Month results
		searchResults3Month = defi.GetSearchResults(accestoken, product, "DAY", 90)
		products.loc[products["Originele Product"] == product, "Zoekvolume \n(3 Maanden)"] = searchResults3Month["searchTerms"]["total"]

		toctoc = time.perf_counter()
		print( "{} ({:.1f} %) - Product time: {:.2f} seconds, Total time: {:.2f} seconds".format(product, ((count/ order.numberOfProductsScript) * 100), (toctoc-tictic), (toctoc - ticLocal)))
		count +=1	

	
	products["Resultaten op Bol"] = pd.to_numeric(products["Resultaten op Bol"])
	products["Zoekvolume \n(1 Maand)"] = pd.to_numeric(products["Zoekvolume \n(1 Maand)"])
	products["Zoekvolume \n(3 Maanden)"] = pd.to_numeric(products["Zoekvolume \n(3 Maanden)"])	

	#Make ratio's
	products["Resultaten-Zoekvolume Ratio \n(1 Maand)"] = (products["Zoekvolume \n(1 Maand)"] / products["Resultaten op Bol"]).round(decimals = 2)
	products["Resultaten-Zoekvolume Ratio \n(3 Maanden)"] = (products["Zoekvolume \n(3 Maanden)"] / products["Resultaten op Bol"]).round(decimals = 2)

	return products	
	


def Advanced(order):
	ticLocal = time.perf_counter()
	
	column_names =["Originele Product",
					"Resultaten op Bol",
					"Zoekvolume \n(1 Maand)",
					"Zoekvolume \n(3 Maanden)",
					"Zoekvolume \n(12 Maanden)",
					"Resultaten-Zoekvolume Ratio \n(1 Maand)",
					"Resultaten-Zoekvolume Ratio \n(3 Maanden)",
					"Resultaten-Zoekvolume Ratio \n(12 Maanden)",
					"Hoeveelheid Reviews \n(Gecombineerd)",
					"Hoeveelheid Reviews \n(1ste Product)",
					"Hoeveelheid Reviews \n(2de Product)",
					"Hoeveelheid Reviews \n(3de Product)"]

	products = pd.read_csv("C:/Users/Jakob/Documents/EasyPeasy/Resultaten/{}/{}.csv".format(order.fileName,order.fileName), names=column_names)
	accestoken = defi.GetAccessToken()
	accestokenStartTime = time.perf_counter()

	count= 1
	order.numberOfProductsScript =  len(products["Originele Product"])
	print("Number of products: {}\n".format(order.numberOfProductsScript))

	for product in products["Originele Product"]:
		#Get new token after 260 seconds
		if time.perf_counter() - accestokenStartTime >260:
			accestokenStartTime = time.perf_counter()
			accestoken = defi.GetAccessToken()

		tictic = time.perf_counter()


		bolResults = defi.GetBolResult(product)
		products.loc[(products["Originele Product"] == product), "Resultaten op Bol"] = bolResults[0]

		#First do all 1 month results
		searchResults1Month = defi.GetSearchResults(accestoken, product, "DAY", 30)
		products.loc[products["Originele Product"] == product, "Zoekvolume \n(1 Maand)"] = searchResults1Month["searchTerms"]["total"]

		#Second do all 3 month results
		searchResults3Month = defi.GetSearchResults(accestoken, product, "DAY", 90)
		products.loc[products["Originele Product"] == product, "Zoekvolume \n(3 Maanden)"] = searchResults3Month["searchTerms"]["total"]
						
		#Thirdly do all 12 month results
		searchResults12Month = defi.GetSearchResults(accestoken, product, "MONTH", 12)
		products.loc[products["Originele Product"] == product, "Zoekvolume \n(12 Maanden)"] = searchResults12Month["searchTerms"]["total"]

		#Review scores
		products.loc[(products["Originele Product"] == product), "Hoeveelheid Reviews \n(1ste Product)"] = bolResults[1]
		products.loc[(products["Originele Product"] == product), "Hoeveelheid Reviews \n(2de Product)"] = bolResults[2]
		products.loc[(products["Originele Product"] == product), "Hoeveelheid Reviews \n(3de Product)"] = bolResults[3]

		toctoc = time.perf_counter()
		print( "{} ({:.1f} %) - Product time: {:.2f} seconds, Total time: {:.2f} seconds".format(product, ((count/order.numberOfProductsScript) * 100), (toctoc-tictic), (toctoc - ticLocal)))
		count +=1	

	products["Resultaten op Bol"] = pd.to_numeric(products["Resultaten op Bol"])
	products["Zoekvolume \n(1 Maand)"] = pd.to_numeric(products["Zoekvolume \n(1 Maand)"])
	products["Zoekvolume \n(3 Maanden)"] = pd.to_numeric(products["Zoekvolume \n(3 Maanden)"])
	products["Zoekvolume \n(12 Maanden)"] = pd.to_numeric(products["Zoekvolume \n(12 Maanden)"])

	products["Hoeveelheid Reviews \n(1ste Product)"] = pd.to_numeric(products["Hoeveelheid Reviews \n(1ste Product)"])
	products["Hoeveelheid Reviews \n(2de Product)"] = pd.to_numeric(products["Hoeveelheid Reviews \n(2de Product)"])
	products["Hoeveelheid Reviews \n(3de Product)"] = pd.to_numeric(products["Hoeveelheid Reviews \n(3de Product)"])	

	#Make ratio's
	products["Resultaten-Zoekvolume Ratio \n(1 Maand)"] = (products["Zoekvolume \n(1 Maand)"] / products["Resultaten op Bol"]).round(decimals = 2)
	products["Resultaten-Zoekvolume Ratio \n(3 Maanden)"] = (products["Zoekvolume \n(3 Maanden)"] / products["Resultaten op Bol"]).round(decimals = 2)
	products["Resultaten-Zoekvolume Ratio \n(12 Maanden)"] = (products["Zoekvolume \n(12 Maanden)"] / products["Resultaten op Bol"]).round(decimals = 2)
	products["Hoeveelheid Reviews \n(Gecombineerd)"] = products["Hoeveelheid Reviews \n(1ste Product)"] + products["Hoeveelheid Reviews \n(2de Product)"] + products["Hoeveelheid Reviews \n(3de Product)"]

	return products

	


def Complete(order):
	ticLocal = time.perf_counter()

	column_names =["Originele Product",
					"Gerelateerde Zoekterm",
					"Resultaten op Bol",
					"Zoekvolume \n(1 Maand)",
					"Zoekvolume \n(3 Maanden)",
					"Zoekvolume \n(12 Maanden)",
					"Resultaten-Zoekvolume Ratio \n(1 Maand)",
					"Resultaten-Zoekvolume Ratio \n(3 Maanden)",
					"Resultaten-Zoekvolume Ratio \n(12 Maanden)",
					"Hoeveelheid Reviews \n(Gecombineerd)",
					"Hoeveelheid Reviews \n(1ste Product)",
					"Hoeveelheid Reviews \n(2de Product)",
					"Hoeveelheid Reviews \n(3de Product)"]

	products = pd.read_csv("C:/Users/Jakob/Documents/EasyPeasy/Resultaten/{}/{}.csv".format(order.fileName,order.fileName), names=column_names)
	accestoken = defi.GetAccessToken()
	accestokenStartTime = time.perf_counter()	

	count= 1
	order.numberOfProductsScript =  len(products["Originele Product"])
	print("Number of products: {}\n".format(order.numberOfProductsScript))
	
	for product in products["Originele Product"]:	
		#Get new token after 260 seconds
		if time.perf_counter() - accestokenStartTime >260:
			accestokenStartTime = time.perf_counter()
			accestoken = defi.GetAccessToken()
			

		tictic = time.perf_counter()
		#Synonym of the original is the original, Needs to be added to let the GetBolResults work
		products.loc[products["Originele Product"] == product, "Gerelateerde Zoekterm"] = product
		bolResultsOriginal = defi.GetBolResult(product)

		products.loc[(products["Originele Product"] == product) & (products["Gerelateerde Zoekterm"] == product), "Resultaten op Bol"] = bolResultsOriginal[0]
		
		#Review scores of original product
		products.loc[(products["Originele Product"] == product) & (products["Gerelateerde Zoekterm"] == product), "Hoeveelheid Reviews \n(1ste Product)"] = bolResultsOriginal[1]
		products.loc[(products["Originele Product"] == product) & (products["Gerelateerde Zoekterm"] == product), "Hoeveelheid Reviews \n(2de Product)"] = bolResultsOriginal[2]
		products.loc[(products["Originele Product"] == product) & (products["Gerelateerde Zoekterm"] == product), "Hoeveelheid Reviews \n(3de Product)"] = bolResultsOriginal[3]

		#First do all 1 month results
		#Togheter with bol results and review scores
		searchResults1Month = defi.GetSearchResults(accestoken, product, "DAY", 30)
		products.loc[(products["Originele Product"] == product) & (products["Gerelateerde Zoekterm"] == product), "Zoekvolume \n(1 Maand)"] = searchResults1Month["searchTerms"]["total"]

		#check if related searchterms exist
		try:
			if(len(searchResults1Month["searchTerms"]["relatedSearchTerms"]) !=0):
				for i in range(min(4, len(searchResults1Month["searchTerms"]["relatedSearchTerms"]))):		
					searchVolume = searchResults1Month["searchTerms"]["relatedSearchTerms"][i]["total"]
					searchTerm = searchResults1Month["searchTerms"]["relatedSearchTerms"][i]["searchTerm"]

					bolResults = defi.GetBolResult(searchTerm)
					newRow = {"Originele Product": product,
							  "Gerelateerde Zoekterm" : searchTerm,
							  "Zoekvolume \n(1 Maand)": searchVolume ,
							  "Resultaten op Bol":bolResults[0],
							 "Hoeveelheid Reviews \n(1ste Product)":bolResults[1],
							 "Hoeveelheid Reviews \n(2de Product)":bolResults[2],
							 "Hoeveelheid Reviews \n(3de Product)":bolResults[3]						  
							  }
					products = products.append(newRow, ignore_index=True)
		except:
			continue

		#Second do all 3 month results
		searchResults3Month = defi.GetSearchResults(accestoken, product, "DAY", 90)
		products.loc[(products["Originele Product"] == product) & (products["Gerelateerde Zoekterm"] == product), "Zoekvolume \n(3 Maanden)"] = searchResults3Month["searchTerms"]["total"]
		try:
			if(len(searchResults1Month["searchTerms"]["relatedSearchTerms"]) !=0):
				for i in range(min(8, len(searchResults3Month["searchTerms"]["relatedSearchTerms"]))):	
					searchTerm = searchResults3Month["searchTerms"]["relatedSearchTerms"][i]["searchTerm"]
					searchVolume = searchResults3Month["searchTerms"]["relatedSearchTerms"][i]["total"]
					products.loc[(products["Originele Product"] == product) & (products["Gerelateerde Zoekterm"] == searchTerm), "Zoekvolume \n(3 Maanden)"] = searchVolume
		except:
			continue

		#Thirdly do all 12 month results
		searchResults12Month = defi.GetSearchResults(accestoken, product, "MONTH", 12)
		products.loc[(products["Originele Product"] == product) & (products["Gerelateerde Zoekterm"] == product), "Zoekvolume \n(12 Maanden)"] = searchResults12Month["searchTerms"]["total"]

		try:
			if(len(searchResults1Month["searchTerms"]["relatedSearchTerms"]) !=0):
				for i in range(min(12, len(searchResults12Month["searchTerms"]["relatedSearchTerms"]))):	
					searchTerm = searchResults12Month["searchTerms"]["relatedSearchTerms"][i]["searchTerm"]
					searchVolume = searchResults12Month["searchTerms"]["relatedSearchTerms"][i]["total"]
					products.loc[(products["Originele Product"] == product) & (products["Gerelateerde Zoekterm"] == searchTerm), "Zoekvolume \n(12 Maanden)"] = searchVolume
		except:
			continue
	
		toctoc = time.perf_counter()
		print( "{} ({:.1f} %) - Product time: {:.2f} seconds, Total time: {:.2f} seconds".format(product, ((count/order.numberOfProductsScript) * 100), (toctoc-tictic), (toctoc - ticLocal)))
		count +=1
	

	products["Resultaten op Bol"] = pd.to_numeric(products["Resultaten op Bol"])
	products["Zoekvolume \n(1 Maand)"] = pd.to_numeric(products["Zoekvolume \n(1 Maand)"])
	products["Zoekvolume \n(3 Maanden)"] = pd.to_numeric(products["Zoekvolume \n(3 Maanden)"])
	products["Zoekvolume \n(12 Maanden)"] = pd.to_numeric(products["Zoekvolume \n(12 Maanden)"])	

	products["Hoeveelheid Reviews \n(1ste Product)"] = pd.to_numeric(products["Hoeveelheid Reviews \n(1ste Product)"])
	products["Hoeveelheid Reviews \n(2de Product)"] = pd.to_numeric(products["Hoeveelheid Reviews \n(2de Product)"])
	products["Hoeveelheid Reviews \n(3de Product)"] = pd.to_numeric(products["Hoeveelheid Reviews \n(3de Product)"])	

	#Make ratio's
	products["Resultaten-Zoekvolume Ratio \n(1 Maand)"] = (products["Zoekvolume \n(1 Maand)"] / products["Resultaten op Bol"]).round(decimals = 2)
	products["Resultaten-Zoekvolume Ratio \n(3 Maanden)"] = (products["Zoekvolume \n(3 Maanden)"] / products["Resultaten op Bol"]).round(decimals = 2)
	products["Resultaten-Zoekvolume Ratio \n(12 Maanden)"] = (products["Zoekvolume \n(12 Maanden)"] / products["Resultaten op Bol"]).round(decimals = 2)
	products["Hoeveelheid Reviews \n(Gecombineerd)"] = products["Hoeveelheid Reviews \n(1ste Product)"] + products["Hoeveelheid Reviews \n(2de Product)"] + products["Hoeveelheid Reviews \n(3de Product)"]

	return products