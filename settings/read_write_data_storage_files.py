file_path = 'settings/settings.txt'


def edit_volume_in_settings_file(volume):
    data = read_settings_file()
    data[0] = "Volume = " + str(volume) + "\n"
    with open(file_path, 'w', encoding='utf-8') as file: 
        file.writelines(data)


def read_volume_from_settings():
    data = read_settings_file()
    return float(data[0][9:12])


def read_editors():
    return read_values_from_settings(1)


def read_voice_command_users():
    return read_values_from_settings(2)


def read_users_to_join_call_with():
    return read_values_from_settings(3)


def read_default_channel_to_message_to():
    return read_values_from_settings(4)


def read_default_channel_to_send_deleted_message_to():
    return read_values_from_settings(5)[0]


def add_to_editors(id):
    add_id_to_settings(id, 1)


def add_to_voice_command_users(id):
    add_id_to_settings(id, 2)


def add_to_users_to_join_call_with(id):
    add_id_to_settings(id, 3)


def delete_from_editors(id):
    delete_id_from_settings(id, 1, "Editors = ")


def delete_from_voice_command_users(id):
    delete_id_from_settings(id, 2, "Voice Command Users = ")


def delete_from_users_to_join_call_with(id):
    delete_id_from_settings(id, 3, "Join Call With Users = ")



def add_id_to_settings(id, row_in_settings_file):
    if is_id_in_settings(id, row_in_settings_file):
        pass

    data = read_settings_file()
    removed_new_line = data[row_in_settings_file].strip()
    data[row_in_settings_file] = removed_new_line + ", " + str(id) + "\n"
    with open(file_path, 'w', encoding='utf-8') as file: 
        file.writelines(data)


def delete_id_from_settings(id, row_in_settings_file, string):
    id = str(id)
    lines = read_settings_file()

    try:
        line = lines[row_in_settings_file]
        values = line.strip().split("= ")[1].split(", ")
        values.remove(id)
        new_line = string + ', '.join(values) + '\n'
        lines[row_in_settings_file] = new_line
    except Exception as e:
        print(e)

    with open(file_path, 'w') as file:
        file.writelines(lines)


def read_values_from_settings(row_in_settings_file):
    lines = read_settings_file()
    line = lines[row_in_settings_file]
    values = line.strip().split("= ")[1].split(", ")
    numeric_array = [int(numeric_string) for numeric_string in values]
    return numeric_array


def read_settings_file():
    with open(file_path, 'r', encoding='utf-8') as file: 
        data = file.readlines() 
    return data


def is_id_in_settings(id, row_in_settings_file):
    values = read_values_from_settings(row_in_settings_file)
    if id in values:
        return True