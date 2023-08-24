import numpy as np
import pandas as pd
import json as js
import yaml
import os

from xml.etree import ElementTree as Et

#===================================
class COPTER_SISTEM_FILE_DESCRIPTOR():

    def __init__(self, file_type=".xml", serialize_mode=False) -> None:
        
        self.file_type = file_type
        self.serialise_mode = serialize_mode
        self.info_files_directory = "C:\Users\1\Desktop\Multi_compter_projects"
        os.path.join(self.info_files_directory, "info_files")
        
    
    def create_pandas_data_frame(self, data_dict, n):

        self.dataframe = pd.DataFrame()
        for (item) in data_dict.keys():
            
            if data_dict[item].shape == (n, 3) or data_dict[item].shape == (n, 4):

                for index in range(data_dict[item].shape[1]):
                    self.dataframe[item + f"_[{index}ax]"] = data_dict[item][:, index]

            else:
                self.dataframe[item] = data_dict[item]


    def save_data_in_file(self, data_dict, n):

        if self.file_type == "nan" or self.file_type == "Nan" or self.file_type == "n" or self.file_type == "N":
            
            if not(self.serialise_mode):
                self.copter_info_root = Et.Element("copter_info")

                with open("copter_info_files/info.json") as json_file:
                    js.dump(data_dict, json_file)
                
                with open("copter_info_files/info.yaml") as yaml_file:
                    yaml.dump(data_dict, yaml_file)
                
                for item in data_dict.keys():

                    self.copter_sub_info = Et.SubElement(self.copter_info_root, f"{item}")
                    if data_dict[item].shape == (n, 3) or data_dict[item].shape == (n, 4):
                    
                        for index in range(data_dict[item].shape[0]):
                            self.copter_sub_sub_item = Et.SubElement(self.copter_sub_info, f"{item} + _[{index}ax]")
                            self.copter_sub_sub_item.text = f"{data_dict[item][item]}"
                
                    else:
                        self.copter_sub_sub_item = Et.SubElement(self.copter_sub_info, f"{item}")
                        self.copter_sub_sub_item.text = f"{data_dict[item]}"
                    self.copter_info_tree = Et.ElementTree(self.copter_info_root)
                    self.copter_info_tree.write("copter_info_files/info.xml")
            else:
                pass



        elif self.file_type == ".json":
            
            if not(self.serialise_mode):
                with open("copter_info_files/info.json", "w") as json_file:
                    js.dump(data_dict, json_file)
            else:
                pass
        
        elif self.file_type == ".yaml":
            
            if not(self.serialise_mode):
                with open("copter_info_files/info.yaml", "w") as yaml_file:
                    yaml.dump(data_dict, yaml_file)
            else:
                pass
        
        elif self.file_type == ".xml":
            if not(self.serialise_mode):
                self.copter_info_root = Et.Element("copter_info")

                for item in data_dict.keys():
                    
                    self.copter_sub_info = Et.SubElement(self.copter_info_root, f"{item}")
                    if data_dict[item].shape == (n, 3) or data_dict[item].shape == (n, 4):
                        
                        for index in range(data_dict[item].shape[0]):
                            self.copter_sub_sub_item = Et.SubElement(self.copter_sub_info, f"{item} + _[{index}ax]")
                            self.copter_sub_sub_item.text = f"{data_dict[item][item]}"
                    
                    else:
                        self.copter_sub_sub_item = Et.SubElement(self.copter_sub_info, f"{item}")
                        self.copter_sub_sub_item.text = f"{data_dict[item]}"
            
            else:
                pass
        

                    
        
        
    
    def save_dataframe_in_csv(self):
        self.dataframe.to_csv("copter_info_files/copter_info.csv")