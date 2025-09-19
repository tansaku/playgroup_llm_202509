import math
from collections import Counter

import numpy as np
import scipy.stats

# In [13]: arr3=np.array([[20, 20], [10, 30]])
# In [14]: scipy.stats.fisher_exact(arr3)
# Out[14]: SignificanceResult(statistic=np.float64(3.0), pvalue=np.float64(0.03683483307622307))

# arr is 2d, row0 is pos and neg results, row1 is pos and neg results


def do_fisher_exact(exp0_pos, exp0_neg, exp1_pos, exp1_neg):
    """Take binary results from two experiments and do a Fisher exact test
    p=1 suggests the two experiments come from the same distribution,
    p=0 suggests the two experiments come from different distributions"""
    arr = np.array([[exp0_pos, exp0_neg], [exp1_pos, exp1_neg]])
    return scipy.stats.fisher_exact(arr)


def summarise_results(rr_trains):
    print(
        f"Got {sum([rr[0].transform_ran_and_matched_for_all_inputs for rr in rr_trains])} of {len(rr_trains)} runs correct"
    )
    total_success = sum(
        [rr[0].transform_ran_and_matched_for_all_inputs for rr in rr_trains]
    )
    total_n = len(rr_trains)
    percent_success = total_success / total_n
    print(
        f"Total success: {total_success}, total n: {total_n}, percentage: {percent_success:.0%}"
    )
    # 2sd is 95.5% of confidence interval
    # 1.96 is the z-score for 95% confidence interval
    sd_95_error_interval = (
        math.sqrt(total_n * (percent_success * (1 - percent_success))) * 1.96
    )
    print(
        f"95% (1.96 SD) CI error interval: {sd_95_error_interval:0.2f} i.e. {total_success - sd_95_error_interval:0.2f} to {total_success + sd_95_error_interval:0.2f}"
    )


def summarise_llm_responses(llm_responses):
    cnt_provider = Counter([response.provider for response in llm_responses])
    print(f"Provider counts: {cnt_provider}")

    all_token_usages = [
        llm_response.usage.total_tokens for llm_response in llm_responses
    ]

    print(
        f"Max token usage on a call was {max(all_token_usages):,}, "
        f"Median token usage on a call was {sorted(all_token_usages)[int(len(all_token_usages) / 2)]:,}"
    )


if __name__ == "__main__":
    print("Made up results...")
    from utils import RunResult

    rr_trains = [
        [RunResult(True, True, True, True, 1.0)],
        [RunResult(False, False, False, False, 0.0)],
    ]
    summarise_results(rr_trains)

    # p==1 so come from the same distribution
    res = do_fisher_exact(500, 500, 500, 500)
    print(res)

    # res = do_fisher_exact(65, 300-65, 77, 300-77)
    res = do_fisher_exact(32, 50 - 32, 43, 50 - 43)
    print(res)
