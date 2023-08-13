import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json as js
import random as rd
import yaml

from xml.etree import ElementTree as Et
from matplotlib.animation import FuncAnimation


class SISTEM_FILE_DESCRIPTOR():

    def __init__(self, description_file_type, serialize_mode=False, sistem_name="Test_sistem", simulation_epizode=100) -> None:
        
        #! variable sistem_file_description_type: тип файла с описанием системы [.json, .xml, .yaml]

        self.simulation_epizodes = simulation_epizode
        self.sistem_name = sistem_name

        self.sistem_file_description_type = description_file_type
        self.sistem_file_description_serialize_mode = serialize_mode

        self.sistem_first_link_pitch = 0.0
        self.sistem_first_link_roll = 0.0
        self.sistem_first_link_yaw =  0.0

        self.sistem_second_link_pitch = 0.0
        self.sistem_second_link_roll = 0.0
        self.sistem_second_link_yaw = 0.0

        self.sistem_thred_link_pitch = 0.0
        self.sistem_thred_link_roll = 0.0
        self.sistem_thred_link_yaw = 0.0

        self.sistem_first_link_lenght = 1.0
        self.sistem_second_link_lenght = 1.0
        self.sistem_thred_link_lenght = 1.0

        self.sistem_first_joint = np.array([np.random.normal(5, 1.12),
                                            np.random.normal(5, 1.12),
                                            np.random.normal(5, 1.12)])
        
        self.sistem_second_joint = np.array([np.random.normal(7, 1.12),
                                             np.random.normal(7, 1.12),
                                             np.random.normal(7, 1.12)])
        
        self.sistem_thred_joint = np.array([np.random.normal(9, 1.12),
                                            np.random.normal(9, 1.12),
                                            np.random.normal(9, 1.12)])
        

        self.sistem_information_dictionary = {
            "sistem_propertys": 
            {
                "sistem_link_propertys": 
                {
                    "sistem_first_link_rotation_and_lenght":
                    {   
                        "iteration_0":
                        {
                            "sistem_first_link_pitch": f"Ox---{self.sistem_first_link_pitch}",
                            "sistem_first_link_roll": f"Oy---{self.sistem_first_link_roll}",
                            "sistem_first_link_yaw": f"Oz---{self.sistem_first_link_yaw}",
                            "sistem_first_link_lenght": f"{self.sistem_first_link_lenght}"
                        }
                    },
                    "sistem_second_link_rotation_and_lenght":
                    {   
                        "iteration_0":
                        {
                            "sistem_second_link_pitch": f"Ox---{self.sistem_second_link_pitch}",
                            "sistem_second_link_roll": f"Oy---{self.sistem_second_link_roll}",
                            "sistem_second_link_yaw": f"Oz---{self.sistem_second_link_yaw}",
                            "sistem_second_link_lenght": f"{self.sistem_second_link_lenght}" 
                        }                    
                    },
                    "sistem_thred_link_rotation_and_lenght":
                    {   
                        "iteration_0":
                        {
                            "sistem_thred_link_pitch": f"Ox---{self.sistem_thred_link_pitch}",
                            "sistem_thred_link_roll": f"Oy---{self.sistem_thred_link_roll}",
                            "sistem_thred_link_yaw": f"Oz---{self.sistem_thred_link_yaw}",
                            "sistem_thred_link_lenght": f"{self.sistem_thred_link_lenght}"
                        }
                    }
                },

                "sistem_joint_propertys":
                {
                    "sistem_first_joint_position":
                    {
                        "iteration_0":
                        {
                            "x": f"{self.sistem_first_joint[0]}",
                            "y": f"{self.sistem_first_joint[1]}",
                            "z": f"{self.sistem_first_joint[2]}"
                        }
                    },
                    "sistem_second_joint_position":
                    {
                        "iteration_0":
                        {
                            "x": f"{self.sistem_second_joint[0]}",
                            "y": f"{self.sistem_second_joint[1]}",
                            "z": f"{self.sistem_second_joint[2]}"
                        }
                    },
                    "sistem_thred_joint_position":
                    {
                        "iteration_0":
                        {
                            "x": f"{self.sistem_thred_joint[0]}",
                            "y": f"{self.sistem_thred_joint[1]}",
                            "z": f"{self.sistem_thred_joint[2]}"
                        }
                    }
                }
            }
        }
        



    
    def save_data_in_file(self):

        print(self.sistem_information_dictionary)
        if self.sistem_file_description_type == ".json":
            
            if not(self.sistem_file_description_serialize_mode):
                with open(f"{self.sistem_name}.json", "w") as json_file:
                    js.dump(self.sistem_information_dictionary, json_file)
            else:
                pass
        
        elif self.sistem_file_description_type == ".xml":

            if not(self.sistem_file_description_serialize_mode):
                
                self.sistem_root = Et.Element("sitem_propertys")
                self.sistem_xml_link_prop = Et.SubElement(self.sistem_root, "sistem_link_propertys")
                self.sistem_xml_joint_prop = Et.SubElement(self.sistem_root, "sistem_joint_propertys")

                self.sistem_xml_first_link_prop = Et.SubElement(self.sistem_xml_link_prop, "sistem_firt_link_propertys")
                self.sistem_xml_second_link_prop = Et.SubElement(self.sistem_xml_link_prop, "sistem_second_link_propertys")
                self.sistem_xml_thred_link_prop = Et.SubElement(self.sistem_xml_link_prop, "sistem_thred_link_porpertys")

                self.sistem_xml_first_joint_prop = Et.SubElement(self.sistem_xml_joint_prop, "sistem_first_joint_propertys")
                self.sistem_xml_second_joint_prop = Et.SubElement(self.sistem_xml_joint_prop, "sistem_second_joint_propertys")
                self.sistem_xml_thred_joint_prop = Et.SubElement(self.sistem_xml_joint_prop, "sistem_thred_joint_propertys")

                for sistem_epizode in range(self.simulation_iterator):

                    self.first_link_xml = self.sistem_information_dictionary["sistem_propertys"]["sistem_link_propertys"]["sistem_first_link_rotation_and_lenght"][f"iteration_{sistem_epizode}"]
                    self.second_link_xml = self.sistem_information_dictionary["sistem_propertys"]["sistem_link_propertys"]["sistem_second_link_rotation_and_lenght"][f"iteration_{sistem_epizode}"]
                    self.thred_link_xml = self.sistem_information_dictionary["sistem_propertys"]["sistem_link_propertys"]["sistem_thred_link_rotation_and_lenght"][f"iteration_{sistem_epizode}"]

                    self.first_joint_xml = self.sistem_information_dictionary["sistem_propertys"]["sistem_joint_propertys"]["sistem_first_joint_position"][f"iteration_{sistem_epizode}"]
                    self.second_joint_xml = self.sistem_information_dictionary["sistem_propertys"]["sistem_joint_propertys"]["sistem_second_joint_position"][f"iteration_{sistem_epizode}"]
                    self.thred_joint_xml = self.sistem_information_dictionary["sistem_propertys"]["sistem_joint_propertys"]["sistem_first_joint_position"][f"iteration_{sistem_epizode}"]
                    
                    self.epizode_link_first = Et.SubElement(self.sistem_xml_first_link_prop, f"epizode_{sistem_epizode}")
                    self.epizode_link_second = Et.SubElement(self.sistem_xml_second_link_prop, f"epizode_{sistem_epizode}")
                    self.epizode_link_thred = Et.SubElement(self.sistem_xml_thred_link_prop, f"peizode_{sistem_epizode}")

                    self.epizode_joint_first = Et.SubElement(self.sistem_xml_first_joint_prop, "epizode_{sistem_epizode}")
                    self.epizode_joint_second = Et.SubElement(self.sistem_xml_second_joint_prop, "epizode_{sistem_epizode}")
                    self.epizode_joint_thred = Et.SubElement(self.sistem_xml_thred_joint_prop, "epozodes_{sistem_epizode}")

                    self.epizode_link_first.text = f"\t|\tlink_pitch: {self.first_link_xml['sistem_first_link_pitch']}\t|\tlink_roll: {self.first_link_xml['sistem_first_link_roll']}\t|\tlink_yaw: {self.first_link_xml['sistem_first_link_yaw']}\t|\tlink_lenght: {self.first_link_xml['sistem_first_link_lenght']}"
                    self.epizode_link_second.text = f"\t|\tlink_pitch: {self.second_link_xml['sistem_second_link_pitch']}\t|\tsistem_roll: {self.second_link_xml['sistem_second_link_roll']}\t|\tsistem_yaw: {self.second_link_xml['sistem_second_link_yaw']}\t|\tlink_lenght: {self.second_link_xml['sistem_second_link_lenght']}"
                    self.epizode_link_thred.text = f"\t|\tlink_pitch: {self.thred_link_xml['sistem_thred_link_pitch']}\t|\tlink_roll: {self.thred_link_xml['sistem_thred_link_roll']}\t|\tlink_yaw: {self.thred_link_xml['sistem_thred_link_yaw']}\t|\tlink_lenght: {self.thred_link_xml['sistem_thred_link_lenght']}"

                    self.epizode_joint_first.text = f"\t|\tjoint x: {self.first_joint_xml['x']}\t|\tjoint y: {self.first_joint_xml['y']}\t|\tjoint z: {self.first_joint_xml['z']}"
                    self.epizode_joint_second.text = f"\t|\tjoint x: {self.second_joint_xml['x']}\t|\tjoint y: {self.second_joint_xml['y']}\t|\tjsoint z: {self.second_joint_xml['z']}"
                    self.epizode_joint_thred.text = f"\t|\tjoint x: {self.thred_joint_xml['x']}\t|\tjoint y: {self.thred_joint_xml['y']}\t|\tjoint z: {self.thred_joint_xml['z']}"
            
                self.sistem_result_xml_file_tree = Et.ElementTree(self.sistem_root)
                self.sistem_result_xml_file_tree.write(f"{self.sistem_name}.xml")

            else:
                pass
        
        elif self.sistem_file_description_type == ".yaml":

            if not(self.sistem_file_description_serialize_mode):

                with open(f"{self.sistem_name}.yaml", "w") as yaml_file:
                    yaml.dump(self.sistem_information_dictionary, yaml_file)

            else:
                pass



class SISTEM_SIMULATION_MODULE(SISTEM_FILE_DESCRIPTOR):

    def __init__(self, description_file_type, serialize_mode=False, sistem_name="Test_sistem", simulation_epizode=100) -> None:
        
        super().__init__(description_file_type, serialize_mode, sistem_name, simulation_epizode)
        
        self.sistem_first_link_freedom_degree = [rd.choice([0.0, 1.0]), rd.choice([0.0, 1.0]), rd.choice([0.0, 1.0])]
        self.sistem_second_link_freedom_degree = [rd.choice([0.0, 1.0]), rd.choice([0.0, 1.0]), rd.choice([0.0, 1.0])]
        self.sistem_thred_link_freedom_degree = [rd.choice([0.0, 1.0]), rd.choice([0.0, 1.0]), rd.choice([0.0, 1.0])]

        self.figure = plt.figure()
        self.view_3d = self.figure.add_subplot(projection="3d")

        self.simulation_iterator = 1

    def sistem_link_rotation(self):
        
        self.sistem_first_joint.dot(np.array([
            [1, 0, 0],
            [0, np.cos(self.sistem_first_link_pitch), np.sin(self.sistem_first_link_pitch)],
            [0, -np.sin(self.sistem_first_link_pitch), np.cos(self.sistem_first_link_pitch)]
        ]))
        self.sistem_first_joint.dot(np.array([
            [np.cos(self.sistem_first_link_roll), 0, np.sin(self.sistem_first_link_roll)],
            [0, 1, 0],
            [-np.sin(self.sistem_first_link_roll), 0, np.cos(self.sistem_first_link_roll)]
        ]))
        self.sistem_first_joint.dot(np.array([
            [np.cos(self.sistem_first_link_yaw), np.sin(self.sistem_first_link_yaw), 0],
            [-np.sin(self.sistem_first_link_yaw), np.cos(self.sistem_first_link_yaw), 0],
            [0, 0, 1]
        ]))
        self.sistem_second_joint.dot(np.array([
            [1, 0, 0],
            [0, np.cos(self.sistem_second_link_pitch), np.sin(self.sistem_second_link_pitch)],
            [0, -np.sin(self.sistem_second_link_pitch), np.cos(self.sistem_second_link_pitch)]
        ]))
        self.sistem_second_joint.dot(np.array([
            [np.cos(self.sistem_second_link_roll), 0, np.sin(self.sistem_second_link_roll)],
            [0, 1, 0],
            [-np.sin(self.sistem_second_link_roll), 0, np.cos(self.sistem_second_link_roll)]
        ]))
        self.sistem_second_joint.dot(np.array([
            [np.cos(self.sistem_second_link_yaw), np.sin(self.sistem_second_link_yaw), 0],
            [-np.sin(self.sistem_second_link_yaw), np.cos(self.sistem_second_link_yaw), 0],
            [0, 0, 1]
        ]))

        self.sistem_thred_joint.dot(np.array([
            [1, 0, 0],
            [0, np.cos(self.sistem_thred_link_pitch), np.sin(self.sistem_thred_link_pitch)],
            [0, -np.sin(self.sistem_thred_link_pitch), np.cos(self.sistem_thred_link_pitch)]
        ]))
        self.sistem_thred_joint.dot(np.array([
            [np.cos(self.sistem_thred_link_roll), 0, np.sin(self.sistem_thred_link_roll)],
            [0, 1, 0],
            [-np.sin(self.sistem_thred_link_roll), 0, np.cos(self.sistem_thred_link_roll)]
        ]))
        self.sistem_thred_joint.dot(np.array([
            [np.cos(self.sistem_thred_link_yaw), np.sin(self.sistem_thred_link_yaw), 0],
            [-np.sin(self.sistem_thred_link_yaw), np.cos(self.sistem_thred_link_yaw), 0],
            [0, 0, 1]
        ]))

    def run_simulation(self):

        def animation(simulation_time):
            self.view_3d.clear()
            self.view_3d.quiver(0, 0, 0, self.sistem_first_joint[0], self.sistem_first_joint[1], self.sistem_first_joint[2], color="gray")
            self.view_3d.quiver(0, 0, 0, 3, 0, 0, color="blue")
            self.view_3d.quiver(0, 0, 0, 0, 3, 0, color="red")
            self.view_3d.quiver(0, 0, 0, 0, 0, 3, color="green")

            self.view_3d.quiver(self.sistem_first_joint[0], self.sistem_first_joint[1], self.sistem_first_joint[2],
                                self.sistem_second_joint[0], self.sistem_second_joint[1], self.sistem_second_joint[2], color="gray")
            self.view_3d.quiver(self.sistem_first_joint[0], self.sistem_first_joint[1], self.sistem_first_joint[2], 3, 0, 0, color="blue")
            self.view_3d.quiver(self.sistem_first_joint[0], self.sistem_first_joint[1], self.sistem_first_joint[2], 0, 3, 0, color="red")
            self.view_3d.quiver(self.sistem_first_joint[0], self.sistem_first_joint[1], self.sistem_first_joint[2], 0, 0, 3, color="green")

            self.view_3d.quiver(self.sistem_second_joint[0], self.sistem_second_joint[1], self.sistem_second_joint[2],
                                self.sistem_thred_joint[0], self.sistem_thred_joint[1], self.sistem_thred_joint[2], color="gray")
            self.view_3d.quiver(self.sistem_second_joint[0], self.sistem_second_joint[1], self.sistem_second_joint[2], 3, 0, 0, color="blue")
            self.view_3d.quiver(self.sistem_second_joint[0], self.sistem_second_joint[1], self.sistem_second_joint[2], 0, 3, 0, color="red")
            self.view_3d.quiver(self.sistem_second_joint[0], self.sistem_second_joint[1], self.sistem_second_joint[2], 0, 0, 3, color="green")

            self.sistem_first_link_lenght = rd.randint(-1, 1)
            self.sistem_second_link_lenght = rd.randint(-1, 1)
            self.sistem_thred_link_lenght = rd.randint(-1, 1)

            self.sistem_first_link_pitch = float(rd.randint(-5, 5)) * np.random.normal(1.25) * self.sistem_first_link_freedom_degree[0]
            self.sistem_first_link_roll = float(rd.randint(-5, 5)) * np.random.normal(1.25) * self.sistem_first_link_freedom_degree[1]
            self.sistem_first_link_yaw = float(rd.randint(-5, 5)) * np.random.normal(1.25) * self.sistem_first_link_freedom_degree[2]

            self.sistem_second_link_pitch = float(rd.randint(-5, 5)) * np.random.normal(1.25) * self.sistem_second_link_freedom_degree[0]
            self.sistem_second_link_roll = float(rd.randint(-5, 5)) * np.random.normal(1.25) * self.sistem_second_link_freedom_degree[1]
            self.sistem_second_link_yaw = float(rd.randint(-5, 5)) * np.random.normal(1.25) * self.sistem_second_link_freedom_degree[2]

            self.sistem_thred_link_pitch = float(rd.randint(-5, 5)) * np.random.normal(1.25) * self.sistem_thred_link_freedom_degree[0]
            self.sistem_thred_link_roll = float(rd.randint(-5, 5)) * np.random.normal(1.25) * self.sistem_thred_link_freedom_degree[0]
            self.sistem_thred_link_yaw = float(rd.randint(-5, 5)) * np.random.normal(1.25) * self.sistem_thred_link_freedom_degree[0]

            self.sistem_link_rotation()
            self.sistem_first_joint += self.sistem_first_link_lenght
            self.sistem_second_joint += self.sistem_second_link_lenght
            self.sistem_thred_joint += self.sistem_thred_link_lenght

            self.sistem_information_dictionary["sistem_propertys"]["sistem_link_propertys"]["sistem_first_link_rotation_and_lenght"][f"iteration_{self.simulation_iterator}"] = {
                "sistem_first_link_pitch": f"Ox---{self.sistem_first_link_pitch}",
                "sistem_first_link_roll": f"Oy---{self.sistem_first_link_roll}",
                "sistem_first_link_yaw": f"Oz---{self.sistem_first_link_roll}",
                "sistem_first_link_lenght": f"{self.sistem_first_link_lenght}" 
            }
            self.sistem_information_dictionary["sistem_propertys"]["sistem_link_propertys"]["sistem_second_link_rotation_and_lenght"][f"iteration_{self.simulation_iterator}"] = {
                "sistem_second_link_pitch": f"Ox---{self.sistem_second_link_pitch}",
                "sistem_second_link_roll": f"Oy---{self.sistem_second_link_roll}",
                "sistem_second_link_yaw": f"Oz---{self.sistem_second_link_roll}",
                "sistem_second_link_lenght": f"{self.sistem_second_link_lenght}" 
            }
            self.sistem_information_dictionary["sistem_propertys"]["sistem_link_propertys"]["sistem_thred_link_rotation_and_lenght"][f"iteration_{self.simulation_iterator}"] = {
                "sistem_thred_link_pitch": f"Ox---{self.sistem_thred_link_pitch}",
                "sistem_thred_link_roll": f"Oy---{self.sistem_thred_link_roll}",
                "sistem_thred_link_yaw": f"Oz---{self.sistem_thred_link_roll}",
                "sistem_thred_link_lenght": f"{self.sistem_thred_link_lenght}" 
            }
            self.sistem_information_dictionary["sistem_propertys"]["sistem_joint_propertys"]["sistem_first_joint_position"][f"iteration_{self.simulation_iterator}"] = {
                "x": f"{self.sistem_first_joint[0]}",
                "y": f"{self.sistem_first_joint[1]}",
                "z": f"{self.sistem_first_joint[2]}"
            }
            print(self.sistem_information_dictionary["sistem_propertys"]["sistem_joint_propertys"]["sistem_first_joint_position"][f"iteration_{self.simulation_iterator}"])
            self.sistem_information_dictionary["sistem_propertys"]["sistem_joint_propertys"]["sistem_second_joint_position"][f"iteration_{self.simulation_iterator}"] = {
                "x": f"{self.sistem_second_joint[0]}",
                "y": f"{self.sistem_second_joint[1]}",
                "z": f"{self.sistem_second_joint[2]}"
            }
            self.sistem_information_dictionary["sistem_propertys"]["sistem_joint_propertys"]["sistem_thred_joint_position"][f"iteration_{self.simulation_iterator}"] = {
                "x": f"{self.sistem_thred_joint[0]}",
                "y": f"{self.sistem_thred_joint[1]}",
                "z": f"{self.sistem_thred_joint[2]}"
            }
            self.simulation_iterator += 1
        simulation_demo = FuncAnimation(self.figure, animation, interval=100)
        plt.show()

if __name__ == "__main__":
    sim = SISTEM_SIMULATION_MODULE(description_file_type=".xml")
    sim.run_simulation()
    sim.save_data_in_file()








            









                    



                    


