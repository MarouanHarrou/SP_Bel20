import pandas as pd


tableau = {"A":[22, 99, "hezjhre", 1, "Maroc"],
           "B":[21, 9, "oejlkjel, ", 4, "Espagne"],
           "C":[27, 3, "lzjkjekj ", 8, "Turquie"]}


df = pd.DataFrame(tableau)

a = 27

for row in df["A"]:
    
    print(row)