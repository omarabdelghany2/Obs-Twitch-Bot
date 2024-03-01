import toml 

current_value = 0

def add_number(number):
        global current_value
        current_value = max(0, current_value + number)


print(current_value)


add_number(-2)


print(current_value)