file_path = '/home/fletcher/FLARE_ws/src/rover/urdf/rover plus 1.urdf'
new_content = ""
with open(file_path, 'r') as file:
    for line in file:
        new_line = ""
        if '+' in line:
            print(line)
            end_ind = line.index('+')   # Index of the plus sign
            for char in range(end_ind, 0, -1):
                if line[char] == ' ' or line[char] == '"':
                    print(char)
                    start_ind = char + 1
                    break
            
            value = line[start_ind:end_ind]
            value = float(value)
            new_value = value + 1
            print("old",value)
            print("new",new_value)
            new_value_str = str(new_value)
            i = 0
            for char in range(0, len(line)):
                if start_ind <= char < end_ind + 2:
                    if i < len(new_value_str):
                        new_line += new_value_str[i]
                        i += 1
                else:
                    new_line += line[char]
            print(new_line)
            new_content += new_line
        else:
            new_content += line

f = open("urdf/translation.urdf", "w")
f.write(new_content)
f.close()

