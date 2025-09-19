

%run method1_text_prompt.py -t baseline.j2 -p 08ed6ac7 -i 100
Total success: 23, total n: 100, percentage: 23%
95% (1.96 SD) CI error interval: 8.25 i.e. 14.75 to 31.25
Provider counts: Counter({'Lambda': 100})
Max token usage on a call was 2,235, Median token usage on a call was 1,949
Experiment took 0:20:50.400756
Full logs in:
experiments/exp_20250919T192012/experiment.log
select code from experiments where all_train_transformed_correctly = True;
shows very similar results
