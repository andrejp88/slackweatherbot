import urllib.request
import shutil

ref = {"ubc"       : """http://www.cleardarksky.com/c/Vancouvercsk.gif?c=1598447""",
       "porteau"   : """http://www.cleardarksky.com/c/SqmshBCcsk.gif?c=1598447""",
       "macmillan" : """http://www.cleardarksky.com/c/GrnMcMlnObBCcsk.gif?c=2023238""",
       "kobau"     : """http://www.cleardarksky.com/c/MtKbSpBCcsk.gif?c=2541607""",
       "mitchell"  : """http://www.cleardarksky.com/c/MtchSchORcsk.gif?c=2541607""",
       "boundary"  : """http://www.cleardarksky.com/c/BndryByBCcsk.gif?c=2541607"""}

def fetch_image(loc):
    try:
        with urllib.request.urlopen(ref[loc]) as response:
            return response.read()
    except:
        return None

def fetch_image_url(loc):
    return ref[loc]
