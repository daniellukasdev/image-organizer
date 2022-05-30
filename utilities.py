# Some various utility/helper functions


# Intelligent Print Function
def intPrint(type = '', importance = 0, message = ''):
    background = ''
    color = ''
    reset = '\u001b[0m'
    if type == "variable":
        color = '\u001b[32;1m' # green
    elif type == "function":
        color = '\u001b[33;1m' # yellow
    elif type == "error":
        color = '\u001b[31;1m' # red
    elif type == "info":
        color = '\u001b[34;1m' # blue
    elif type == "event":
        color = '\u001b[35;1m' # magenta
    elif type == "test":
        color = '\u001b[37;1m' # white
        background = '\u001b[41;1m' # red
    else:
        color = '\u001b[37;1m' # white

    if importance == 0:
        return print(message)
    elif importance == 1:
        return print(f"{color} {message} {reset}" )
    elif importance == 2:
        return print(f"{background} {message} {reset}" )