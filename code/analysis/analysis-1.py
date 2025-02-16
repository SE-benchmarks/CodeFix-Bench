import os
import json
import pdb

artifacts_folder = (
    "/Users/azeem/workspace/code/personal/swe-paper-2024/final/paper-artifacts"
)

with open(f"{artifacts_folder}/entries.json", "r") as file:
    all_entries = json.load(file)

# with open(f"{artifacts_folder}/historical.json", "r") as file:
#     all_historical = json.load(file)

# with open(f"{artifacts_folder}/random.json", "r") as file:
#     all_randoms = json.load(file)

# with open(f"{artifacts_folder}/meta.json", "r") as file:
#     all_meta = json.load(file)

# with open(f"{artifacts_folder}/tf-idf.json", "r") as file:
#     all_tf_idf = json.load(file)

# with open(f"{artifacts_folder}/vsm-cos.json", "r") as file:
#     all_vsm_cos = json.load(file)

# with open(f"{artifacts_folder}/bm25.json", "r") as file:
#     all_bm_25 = json.load(file)

with open(f"{artifacts_folder}/llm-results/task-run-3.json", "r") as file:
    all_llm = json.load(file)


def compute_map_score(ground_truth, attempt):
    test_files = [i["file"] for i in attempt["results"]]
    total_precision = 0.0
    found_count = 0

    for i, gt_item in enumerate(ground_truth):
        if gt_item in test_files:
            index = test_files.index(gt_item)
            precision = (i + 1) / (index + 1)
            total_precision += precision
            found_count += 1.0

    return total_precision / len(ground_truth) if found_count > 0 else 0.0


def compute_mrr_score(ground_truth, attempt):
    test_files = [i["file"] for i in attempt["results"]]

    for index, t_file in enumerate(test_files):
        if t_file in ground_truth:
            return 1.0 / (index + 1)

    return 0


def is_top_k(ground_truth, attempt, k):
    test_files = [i["file"] for i in attempt["results"]][:k]
    for item in ground_truth:
        if item in test_files:
            return 1
    return 0


top_1 = 0
top_3 = 0
top_5 = 0

map_score = 0
mrr_score = 0

count_total = 0
for idx, entry in enumerate(all_entries):
    ground_truth = entry["files"]
    pr = entry["pr"]

    if pr not in all_llm:
        continue

    count_total += 1

    # meta = all_meta[pr]
    # historical = all_historical[pr]
    # randoms = all_randoms[pr]
    # tf_idf = all_tf_idf[pr]
    # vsm_cos = all_vsm_cos[pr]
    # bm_25 = all_bm_25[pr]
    llm = all_llm[pr]

    # TODO: Set the target benchmark here
    benchmark = llm

    if is_top_k(ground_truth, benchmark, 1):
        top_1 += 1
    if is_top_k(ground_truth, benchmark, 3):
        top_3 += 1
    if is_top_k(ground_truth, benchmark, 5):
        top_5 += 1

    map_score += compute_map_score(ground_truth, benchmark)
    mrr_score += compute_mrr_score(ground_truth, benchmark)


top1_score = round(top_1 * 100.0 / count_total, 2)
top3_score = round(top_3 * 100.0 / count_total, 2)
top5_score = round(top_5 * 100.0 / count_total, 2)
map_score = round(map_score / count_total, 2)
mrr_score = round(mrr_score / count_total, 2)



print(map_score)
print(mrr_score)
print(top1_score)
print(top3_score)
print(top5_score)