def find_indexes_in_list(data, key):
    temp_list = []

    for index, value in enumerate(data):
        if data[index] == key:
            temp_list.append(index)
    
    return temp_list