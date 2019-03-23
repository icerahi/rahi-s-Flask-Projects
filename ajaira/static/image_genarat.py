import random, os
import shutil, os

path = r"/home/rahi/Desktop/AjairaHouse/ajaira/static/img"
random_filename = random.choice([
    x for x in os.listdir(path)
    if os.path.isfile(os.path.join(path, x))
])
print(random_filename)




shutil.copy2('/home/rahi/Desktop/AjairaHouse/ajaira/static/img/'+random_filename,
             '/home/rahi/Desktop/AjairaHouse/ajaira/static/login/')

os.rename('/home/rahi/Desktop/AjairaHouse/ajaira/static/login/'+random_filename,
          "/home/rahi/Desktop/AjairaHouse/ajaira/static/login/rahi.png")
