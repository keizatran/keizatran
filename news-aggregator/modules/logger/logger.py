import logging 

def logger(name):
	"""
	
	Function to create as a logger instance, act as 'print' function with logging capability.

	Logged info is stored in scraping.log file.

	"""

	#now we will Create and configure logger 
	logging.basicConfig(filename=f"log/{name}.log", 
						format='%(asctime)s %(message)s', 
						filemode='a') 

	#Let us Create an object 
	logger=logging.getLogger()

	logger.addHandler(logging.StreamHandler()) # add StreamHandler for print capability

	#Now we are going to Set the threshold of logger to DEBUG 
	logger.setLevel(logging.INFO)

	return logger