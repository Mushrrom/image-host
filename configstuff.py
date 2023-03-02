# I wish this wasn't necessary, and i will figure out a better way to do this.
import os


# For some reason wsgi can't use dotenv and its annoying

def configsutff():
    os.environ["images_path"] = "images"
    os.environ["main_path"] = "."  # wsgi cant do local reading. And I am not manually setting this in each file
    os.environ["URL"] = "127.0.0.1:5000"
    os.environ["data_path"] = "./data"

