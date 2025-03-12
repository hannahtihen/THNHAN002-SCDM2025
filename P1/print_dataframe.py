import pandas as pd

CTD_Data = pd.read_csv("CTD_Data.dat", delim_whitespace=True)
CTD_Data_dataframe = pd.DataFrame(CTD_Data)


print(CTD_Data_dataframe)
