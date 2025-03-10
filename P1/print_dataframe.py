import pandas as pd
ctd_file = pd.read_csv("../../Desktop/AOS_Coursework/1_Foundational_Modules/1_SCDM_Scientific_Computing_Data_Management/2_Data_camp/1_Phyton_Practical/3_Phyton_Assignments/P1/CTDdata.csv", delimiter=";")
ctd_dataframe = pd.DataFrame(ctd_file)
print(ctd_dataframe)
