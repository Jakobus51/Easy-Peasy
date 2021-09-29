import glob
import os

#Initialize your order
class Order:	

	def __init__(self, name, company, date, package, numberOfProducts ):
		self.name = name
		self.company = company  
		self.date = date
		self.package = package
		self.numberOfProducts = numberOfProducts

		#this is the amount of products that are in the csv
		self.numberOfProductsScript = ""
		self.setInvoiceNumber()
		self.setMoney(package, numberOfProducts)
		self.total = round(self.amount + self.tax, 2)
		self.fileName = "{} ({})".format(self.company, self.date)
		self.setColour(package)
		self.averageTime = ""		
		self.totalTimeResearch = ""

	def setInvoiceNumber(self):
		#Gets the latest file in the given directory
		list_of_files = glob.glob("C:/Users/Jakob/Documents/EasyPeasy/Boekhouding/Facturen Uit/*") 
		latest_file = max(list_of_files, key=os.path.getctime)		

		#retrieves the invoice number from the latest file in the directory and adds one
		self.invoiceNumber = int(latest_file[latest_file.index("Uit")+4: latest_file.index("Uit")+9]) +1

	def setColour(self, package):
		if(package == "Sample" or package == "Complete"):
			self.colour = "#EE6CDA"
		if(package == "Advanced"):
			self.colour = "#6C84EE"
		if(package == "Basic"):
			self.colour = "#0ED1B3"	


	#Set tax and invoice amount
	def setMoney(self, package, numberOfProducts):
		if(package == "Sample"):
			self.amount = 0
			self.tax = 0  

		if(package == "Basic" and numberOfProducts == 25 ):
			self.amount = 19.95
			self.tax = 4.19        
		if(package == "Basic" and numberOfProducts == 50 ):
			self.amount = 29.95
			self.tax = 6.29        
		if(package == "Basic" and numberOfProducts == 100 ):
			self.amount = 49.95
			self.tax = 10.49        

		if(package == "Advanced" and numberOfProducts == 25 ):
			self.amount = 29.95
			self.tax = 6.29        
		if(package == "Advanced" and numberOfProducts == 50 ):
			self.amount = 49.95
			self.tax = 10.49
		if(package == "Advanced" and numberOfProducts == 100 ):
			self.amount = 79.95
			self.tax = 16.79
			
		if(package == "Complete" and numberOfProducts == 25 ):
			self.amount = 39.95
			self.tax = 8.39        
		if(package == "Complete" and numberOfProducts == 50 ):
			self.amount = 69.95
			self.tax = 14.69       
		if(package == "Complete" and numberOfProducts == 100 ):
			self.amount = 99.95
			self.tax = 20.99
