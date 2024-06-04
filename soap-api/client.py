from zeep import Client

# WSDL URL of the SOAP service
wsdl = 'http://localhost:8000/soap?wsdl'

# Create a zeep client
client = Client(wsdl=wsdl)

# Call the SOAP method
response = client.service.say_hello("John")

# Print the response
print(response)
