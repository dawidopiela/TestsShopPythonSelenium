

def print_color(text, color):
    if color == "g":
        print("\u001b[32;1m" + text + "\u001b[0m")
    elif color == "r":
        print("\u001b[31;1m" + text + "\u001b[0m")
    elif color == "y":
        print("\u001b[33;1m" + text + "\u001b[0m")
    elif color == "b":
        print("\u001b[34;1m" + text + "\u001b[0m")
    elif color == "lb":
        print("\u001b[36;1m" + text + "\u001b[0m")
    elif color == "m":
        print("\u001b[35m" + text + "\u001b[0m")
    else:
        print(text)
