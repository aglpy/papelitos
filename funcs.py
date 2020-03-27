from colorama import init, Fore, Back, Style
init(autoreset=True)

__colors = "BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE"
__colors_ref = dict(zip(__colors.lower().split(", "), __colors.split(", ")))
__colors = __colors.lower().split(", ")
__styles_ref = {"0":"DIM", "1":"NORMAL", "2":"BRIGHT", "reset":"RESET_ALL"}
__resets_ref = {"f":"RESET", "b":"RESET", "s":"RESET_ALL"}
__modes_ref = {"f":"Fore", "b":"Back", "s":"Style"}
__references = {"f":"__colors_ref", "b":"__colors_ref", "s":"__styles_ref"}
__f_tags = list(map(lambda x: f"f {x}>", __colors))
__b_tags = list(map(lambda x: f"b {x}>", __colors))
__s_tags = ["s 0>","s 1>","s 2>"]
__reset_tags = ["/f>", "/b>", "/s>"]
__all_tags = __f_tags + __b_tags + __s_tags + __reset_tags

def __tag2ref(tag):
    # This function return the colorama tag from a friendly tag given
    if tag.startswith("/"):
        return eval(f"{__modes_ref.get(tag[1])}.{__resets_ref.get(tag[1])}")
    mode, value = tag.split()
    return eval(f"{__modes_ref.get(mode)}.{eval(__references.get(mode)).get(value)}")

def fprint(text):
    # This function format the text given with colors and bold
    # The text can be inside tags like <f color>text</f> to change text color
    # Inside tags like <b color>text</b> to change background color
    # Inside tags like <s n>text</s> to change bold level
    # Supported colors are black, red, green, yellow, blue, magenta, cyan and white
    # Supported bold levels are 1, 2 and 3
    # If a tag is started without close other tag of same type, the new type is applied
    # If a tag is not closed it is applied to the end of the text
    if type(text) != str:
        print(text)
        return text
    formatted = ""
    clean = ""
    while "<" in text:
        i = text.index("<") + 1
        formatted, clean, text = formatted + text[:i], clean + text[:i], text[i:]
        if any(text.startswith(x) for x in __all_tags):
            formatted, clean = formatted[:-1], clean[:-1]
            i = text.index(">")
            tag, text = text[:i], text[i+1:]
            formatted += __tag2ref(tag)
    print(formatted + text)
    return clean + text

