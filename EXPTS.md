
%run method2_reflexion.py -t reflexion.j2 -p 0d3d703e -i 2

%run method2_reflexion.py -t reflexion.j2 -p 08ed6ac7 -i 100
REFLEXION=5
Total success: 70, total n: 100, percentage: 70%
95% (1.96 SD) CI error interval: 8.98 i.e. 61.02 to 78.98
Provider counts: Counter({'Lambda': 616})
Max token usage on a call was 4,242, Median token usage on a call was 2,357
Experiment took 2:12:19.665814


%run method2_reflexion.py -t reflexion.j2 -p 08ed6ac7 -i 100
REFLEXION=3
Total success: 54, total n: 100, percentage: 54%
95% (1.96 SD) CI error interval: 9.77 i.e. 44.23 to 63.77
Provider counts: Counter({'Lambda': 466})
Max token usage on a call was 3,853, Median token usage on a call was 2,305
Experiment took 1:38:15.071390

(25 its as a smaller trial)
%run method2_reflexion.py -t reflexion.j2 -p 08ed6ac7 -i 25
REFLEXION=3
Total success: 13, total n: 25, percentage: 52%
95% (1.96 SD) CI error interval: 4.90 i.e. 8.10 to 17.90
Provider counts: Counter({'Lambda': 116})
Max token usage on a call was 3,162, Median token usage on a call was 2,308
Experiment took 0:23:43.389980


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


%run method1_text_prompt.py -t baseline_justjson.j2 -p 08ed6ac7 -i 100
sqlite3 experiments/exp_20250922T183920/experiments.db
Total success: 34, total n: 100, percentage: 34%
95% (1.96 SD) CI error interval: 9.28 i.e. 24.72 to 43.28
Provider counts: Counter({'Lambda': 100})
Max token usage on a call was 2,017, Median token usage on a call was 1,715
Experiment took 0:19:40.088346
Full logs in:
experiments/exp_20250922T183920/experiment.log

%run method1_text_prompt.py -t baseline_justjson.j2 -p 08ed6ac7 -i 100
Total success: 41, total n: 100, percentage: 41%
95% (1.96 SD) CI error interval: 9.64 i.e. 31.36 to 50.64
Provider counts: Counter({'Lambda': 100})
Max token usage on a call was 2,028, Median token usage on a call was 1,758
Experiment took 0:20:30.754208
Full logs in:
experiments/exp_20250922T200146/experiment.log

Total success: 390, total n: 1000, percentage: 39%
95% (1.96 SD) CI error interval: 30.23 i.e. 359.77 to 420.23
Provider counts: Counter({'Lambda': 1000})
Max token usage on a call was 2,318, Median token usage on a call was 1,746
Experiment took 3:09:38.266363
Full logs in:
experiments/exp_20250922T210837/experiment.log
