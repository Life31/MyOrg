import sys

new_passwoed = sys.argv[1]
data = []

with open(r"../yatube/settings.py", "r") as file:
    lines = file.readlines()
    for line in lines:
        data.append(line)

    for i in range(len(data)):
        if data[i][:19] == "EMAIL_HOST_PASSWORD":
            old_password = (data[i][23:-1])
            data[i] = "EMAIL_HOST_PASSWORD = '" + new_passwoed + "'" + '\n'
            print(data[i])

with open(r"../yatube/settings.py", "w") as file:
    for line in data:                             
        file.write(line)
