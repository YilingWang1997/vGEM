from cobra.io import read_sbml_model
import pandas as pd
import os
import glob
import sys
import re

# Function to calculate uptake or secretion flux
def calculate_flux(reaction_id, model):
    try:
        flux = model.reactions.get_by_id(reaction_id).flux
        return flux if flux < 0 else 0, flux if flux > 0 else 0
    except KeyError:
        return 0, 0

# 定义一个函数来计算CUE
def calculate_cue(model, solution, cue_details_path, carbon_content, xml_file):
    # 这里添加CUE的计算逻辑
    # 示例：CUE = 目标反应的流量 / 摄入碳源的流量
    # 需要根据您的模型和需求进行调整
    uptake_fluxes = {}
    secretion_fluxes = {}
    for compound, c_content in carbon_content.items():
        reaction_id = f'EX_{compound}'
        uptake, secretion = calculate_flux(reaction_id, model)
        uptake_fluxes[compound] = uptake * c_content
        secretion_fluxes[compound] = secretion * c_content

    # Calculate CUE
    numerator = abs(sum(uptake_fluxes.values())) - sum(secretion_fluxes.values())
    denominator = abs(sum(uptake_fluxes.values()))
    cue = numerator / denominator if denominator != 0 else 0

    result_df = pd.DataFrame({
        'Model': [os.path.basename(xml_file)] * len(carbon_content),
        'Compound': list(carbon_content.keys()),
        'Uptake Flux': list(uptake_fluxes.values()),
        'Secretion Flux': list(secretion_fluxes.values())
    })
    xml_file_basename = os.path.splitext(os.path.basename(xml_file))[0]
    cue_details_filename = "{}_{}.csv".format(carbon_source, xml_file_basename)
    cue_details = os.path.join(cue_details_path, cue_details_filename)
    result_df.to_csv(cue_details, index=False)
    return cue

def run_simulation_with_single_carbon_source(model, carbon_source, cue_details_path, carbon_content, xml_file):
    # 关闭所有碳源
    for exchange in model.exchanges:
        if 'C' in exchange.check_mass_balance():
            exchange.lower_bound = 0

    # 开启指定碳源
    if carbon_source in model.reactions:
        model.reactions.get_by_id(carbon_source).lower_bound = -1000

    # 运行模拟
    solution = model.optimize()

    # 收集统计信息
    gene_count = len(model.genes)
    metabolite_count = len(model.metabolites)
    reaction_count = len(model.reactions)
    product_count = len(solution.fluxes[solution.fluxes > 0])
    carbon_exchange_reactions = len([ex for ex in model.exchanges if 'C' in ex.check_mass_balance()])
    
    # 计算CUE
    cue = calculate_cue(model, solution, cue_details_path, carbon_content, xml_file)

    return {
        'Model': os.path.splitext(os.path.basename(xml_file))[0],
        'CUE': cue,
        'Carbon Source': carbon_source,
        'Objective Value': solution.objective_value,
        'Gene Count': gene_count,
        'Metabolite Count': metabolite_count,
        'Reaction Count': reaction_count,
        'Product Count': product_count,
        'Carbon Exchange Reactions': carbon_exchange_reactions
    }



# Create an empty DataFrame to store all results
all_results = pd.DataFrame(columns=['Model', 'CUE', 'Carbon Source', 'Objective Value', 'Gene Count', 'Metabolite Count', 'Reaction Count', 'Product Count', 'Carbon Exchange Reactions'])

# Define the directory containing XML files
directory_path = sys.argv[1]
cue_details_path = os.path.join(directory_path, "cue_details")

if not os.path.exists(cue_details_path):
    os.makedirs(cue_details_path)

# List XML files in the directory
xml_files = glob.glob(os.path.join(directory_path, '*.xml'))

# Loop through each XML file
for xml_file in xml_files:
    # Load your COBRA model
    model = read_sbml_model(xml_file)

    # Carbon content for each compound
    carbon_content = {
        'glc__D_e': 6,  # D-Glucose
        'fum_e': 4,     # Fumarate
        'ac_e': 2,      # Acetate
        'acald_e': 2,   # Acetaldehyde
        'akg_e': 5,     # 2-Oxoglutarate
        'etoh_e': 2,    # Ethanol
        'for_e': 1,     # Formate
        'fru_e': 6,     # D-Fructose
        'gln__L_e': 5,  # L-Glutamine
        'glu__L_e': 5,  # L-Glutamate
        'lac__D_e': 3,  # D-lactate
        'mal__L_e': 4,  # L-Malate
        'pyr_e': 3,     # Pyruvate
        'succ_e': 4     # Succinate
    }

    for compound, c_content in carbon_content.items():
        carbon_source = f'EX_{compound}'
        result = run_simulation_with_single_carbon_source(model, carbon_source, cue_details_path, carbon_content, xml_file)
        result = pd.DataFrame(result,index=[0])
        all_results = pd.concat([all_results, result], ignore_index=True)

# Save the overall results to a CSV file
output_filename = sys.argv[2]
all_results.to_csv(output_filename, index=False)
