# this file is constructed purely to test our rest api

import requests  # this helps us to send request like post, get etc.,

# base url
BASE = "http://127.0.0.1:5000/"

# this below is a put request - to put data inside the object created in the ""main.py"" named video ={}
# response = requests.put(BASE + "video/1", {"likes":10}) 
# print(response.json())

# sending a GET request to the BASE url mentioned above + teh helloworld
# response = requests.get(BASE + "helloworld/Sparsh") 
# print(response.json()) # .json() is used to convert the response which will be in object form to json readable format

# sending  a POST request to the BASE url above
# respon = requests.post(BASE + "helloworld")
# print(respon.json()) 

# adding data in database with for loop
# data = [{"name": "Sparsh", "likes":107, "views": 10000}, {"name": "Sparsh S", "likes":150, "views": 50000}, {"name": "Sparsh H", "likes":130, "views": 15000},]

# for i in range(len(data)):
#     response = requests.put(BASE + "video/" + str(i), data[i])  
#     print(response.json())
    

# input() # so we can pause it and press enter
# response = requests.delete(BASE + "video/0") 
# print(response)  # i we're not retuning any json file so we dont need to put response.json() here

# to update values from database
# response = requests.patch(BASE + "video/2", {"views": 5230000}) 
# print(response.json())
# input()


# to check abort function 
response = requests.get(BASE + "video/2") 
print(response.json())

# to delee from database
# response = requests.delete(BASE + "video/2") 
# print(response.json())