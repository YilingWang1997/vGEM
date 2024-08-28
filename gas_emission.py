from cobra.io import read_sbml_model
import pandas as pd
import os
import glob
import sys
import re

#calculate emissions
def calculate_emissions(model, reaction_ids):
    emissions = {}
    for gas, reaction_id in reaction_ids.items():
        try:
            model.optimize()
            flux = model.reactions.get_by_id(gas).flux
            emissions[gas] = flux  
        except KeyError:
            emissions[gas] = 0
            print(gas)
    return emissions

def process_directory(directory_path):
    # 定义气体反应ID
    reaction_ids = {
        'EX_co2_e': 'R_EX_co2_e',
        'EX_ch4s_e': 'R_EX_ch4s_e',
        'EX_nh4_e': 'R_EX_nh4_e',
        'EX_no2_e': 'R_EX_no2_e', 
        'EX_no3_e': 'R_EX_no3_e'
    }

    # 初始化一个空的 DataFrame 来存储结果
    all_results = pd.DataFrame(columns=['Filename', 'EX_co2_e','EX_ch4s_e','EX_nh4_e','EX_no2_e', 'EX_no3_e'])

    # 遍历目录下的所有 XML 文件
    for xml_file in glob.glob(os.path.join(directory_path, '*.xml')):
        model = read_sbml_model(xml_file)
        emissions = calculate_emissions(model, reaction_ids)

        # 将结果添加到 DataFrame
        result = [os.path.basename(xml_file), emissions['EX_co2_e'], emissions['EX_ch4s_e'], emissions['EX_nh4_e'], emissions['EX_no2_e'], emissions['EX_no3_e']]
        result = pd.DataFrame(result, index=['Filename', 'EX_co2_e','EX_ch4s_e','EX_nh4_e','EX_no2_e', 'EX_no3_e'])
        all_results = pd.concat([all_results, result.T], ignore_index=True)

    return all_results


# Define the directory containing XML files
directory_path = sys.argv[1]
results = process_directory(directory_path)    

# Save the overall results to a CSV file
output_filename = sys.argv[2]
results.to_csv(output_filename, index=False)
