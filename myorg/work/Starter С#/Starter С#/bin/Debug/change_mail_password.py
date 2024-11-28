import sys

var = sys.argv[1]
data = []
new_passwoed = var
with open(r"settings.py", "r") as file:
    lines = file.readlines()
    for line in lines:
        data.append(line)

    for i in range(len(data)):
        if data[i][:19] == "EMAIL_HOST_PASSWORD":
            print(data[i][23:-2])
            old_password = (data[i][23:-1])
            data[i] = "EMAIL_HOST_PASSWORD = '" + new_passwoed + "'" + '\n'
            print(data[i])

with open(r"settings1.py", "w") as file:
    for line in data:                             
        file.write(line)


with open(r"settings.py", "r") as file:
    with open(r"settings1.py", "r") as file1:
        one = file.readlines()
        two = file1.readlines()
        for i in range(len(one)):
            if one[i] == two[i]:
                print('True')
            else:
                print(one[i])
                print(two[i])
