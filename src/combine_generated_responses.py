import os
import pandas as pd
import json
import re

# Declare paper parent folder dir 
paper_parent_folder = "../data/papers"

folders = [name for name in os.listdir(paper_parent_folder) if os.path.isdir(
    os.path.join(paper_parent_folder, name))]


def read_json_dict(dict_path):
    with open(dict_path, "r") as f:
        data = json.load(f)
    return data['QUESTIONS']["QUESTIONS"]

commands_file = "../data/llm_simulation_commands.txt"
with open(commands_file, "r", encoding="utf-8") as f:
    commands = f.read()

commands = [i.strip() for i in commands.split('\n') if i.strip() != ""]

model_pair_dict = {'index_model_pair': [], 'relevance_model': [], "answer_model": []}

for s in commands:
    model_pair_dict['relevance_model'].append(re.search(r'--relevance-model (\S+)', s).group(1))
    model_pair_dict['answer_model'].append(re.search(r'--answer-model (\S+)', s).group(1))
    model_pair_dict['index_model_pair'].append(int(re.search(r'out_err/(\d+)\.out', s).group(1)))

model_pair_df = pd.DataFrame(model_pair_dict)

# Depends on questions sorted from MetabeeAI 
questions = ["design", "population", "welfare"]



final_data = {'index_model_pair': [], "question": [], "paper_id": [], 'answer_rev3': []}

to_retrive_info = ['answer', "reason", "chunk_ids", 'relevance_prompt_tokens', 'relevance_completion_tokens', 'answer_prompt_tokens', 'answer_completion_tokens']
for t in to_retrive_info:
    final_data[t] = []


paper_ids_intersection = folders
# Get the actual model-pair indices from llm_simulation_commands.txt
pair_indices = model_pair_df["index_model_pair"].unique()

print("Model pairs to merge:", pair_indices)
print("Number of pairs:", len(pair_indices))

for indx_model_pair in pair_indices:

    files_found = 0

    for f in paper_ids_intersection:

        # Generated answer from this model pair
        to_check_file = (
            f"../data/papers/{f}/answers/"
            f"{indx_model_pair}_answers.json"
        )

        # Golden/reference answer
        golden_file = (
            f"../data/papers/{f}/answers_extended.json"
        )

        if os.path.exists(to_check_file) and os.path.exists(golden_file):

            files_found += 1

            # Generated answers
            data_here = read_json_dict(to_check_file)

            # Golden answers
            with open(golden_file, "r", encoding="utf-8") as gf:
                golden_data = json.load(gf)["QUESTIONS"]

            for q in questions:

                final_data["index_model_pair"].append(indx_model_pair)
                final_data["question"].append(q)
                final_data["paper_id"].append(f)

                # Golden/reference answer
                final_data["answer_rev3"].append(
                    golden_data[q]["user_answer_positive"]
                )

                # Generated answer + token information
                for t in to_retrive_info:
                    final_data[t].append(
                        data_here[q].get(t)
                    )

    print(
        f"Pair {indx_model_pair}: "
        f"{files_found}/{len(paper_ids_intersection)} answer files found"
    )


# Convert everything to dataframe
final_df = pd.DataFrame(final_data)

# Add relevance model + answer model names
final_df = final_df.merge(
    model_pair_df,
    on="index_model_pair",
    how="left"
)

# Sort nicely
final_df = final_df.sort_values(
    ["index_model_pair", "paper_id", "question"]
).reset_index(drop=True)


# Save
output_path = "../data/llm_simulation_results_primate_welfare.csv"

final_df.to_csv(output_path, index=False)

print("\nSaved:", output_path)
print("Total rows:", len(final_df))
print("Pairs:", final_df["index_model_pair"].nunique())
print("Papers:", final_df["paper_id"].nunique())
print("\nRows per pair:")
print(final_df.groupby("index_model_pair").size())


print("\nRows by pair and question:")
print(
    final_df.groupby(
        ["index_model_pair", "question"]
    ).size().unstack()
)
