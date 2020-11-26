with open("result.csv", 'r+') as file:
    string = file.read().replace("\n\n", "\n")
    file.seek(0)  
    file.truncate() 
    file.write(string)
