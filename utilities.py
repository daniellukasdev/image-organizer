# Some various utility/helper functions


# Intelligent Print Function
def intPrint(type = '', importance = 0, message = ''):
    background = ''
    color = ''
    reset = '\u001b[0m'
    if type == "variable":
        background = '\u001b[42;1m' # green
        color = '\u001b[32;1m' # green
    elif type == "function":
        background = '\u001b[43;1m' # yellow
        color = '\u001b[33;1m' # yellow
    elif type == "error":
        background = '\u001b[41;1m' # red
        color = '\u001b[30;1m' # red
    elif type == "info":
        background = '\u001b[44;1m' # blue
        color = '\u001b[34;1m' # blue
    elif type == "event":
        background = '\u001b[45;1m' # magenta
        color = '\u001b[35;1m' # magenta
    elif type == "test":
        background = '\u001b[41;1m' # red
        color = '\u001b[37;1m' # white
    else:
        color = '\u001b[37;1m' # white

    if importance == 0:
        return print(message)
    elif importance == 1:
        return print(f"{color} {message} {reset}" )
    elif importance == 2:
        return print(f"{background}{color} {message} {reset}" )