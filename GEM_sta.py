from cobra.io import read_sbml_model
import pandas as pd
import os
import glob
import sys
import re

# 定义一个函数来计算每个GEM模型的指标
def calculate_metrics(model):
    gene_count = len(model.genes)
    metabolite_count = len(model.metabolites)
    reaction_count = len(model.reactions)
    solution = model.optimize()
    product_count = len([rxn.id for rxn in model.reactions if solution.fluxes[rxn.id] > 0])
    carbon_exchange_reactions = len([ex for ex in model.exchanges if 'C' in ex.check_mass_balance()])
    nitrogen_exchange_reactions = len([ex for ex in model.exchanges if 'N' in ex.check_mass_balance()])
    return {
        'Model': os.path.splitext(os.path.basename(xml_file))[0],
        'Gene Count': gene_count,
        'Metabolite Count': metabolite_count,
        'Reaction Count': reaction_count,
        'Product Count': product_count,
        'Carbon Exchange Reactions': carbon_exchange_reactions,
        'Nitrogen Exchange Reactions': nitrogen_exchange_reactions
    }

# 初始化一个空的 DataFrame 来存储结果
all_results = pd.DataFrame(columns=['Filename', 'Gene Count', 'Metabolite Count', 'Reaction Count', 'Product Count', 'Carbon Exchange Reactions', 'Nitrogen Exchange Reactions'])

# 遍历目录下的所有 XML 文件
directory_path = sys.argv[1]

for xml_file in glob.glob(os.path.join(directory_path, '*.xml')):
    model = read_sbml_model(xml_file)
    result = calculate_metrics(model)
    result = pd.DataFrame(result,index=[0])
    all_results = pd.concat([all_results, result], ignore_index=True)

# Save the overall results to a CSV file
output_filename = sys.argv[2]
all_results.to_csv(output_filename, index=False)
