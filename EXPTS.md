
TESTING
%run method2_reflexion.py -t reflexion.j2 -p 0d3d703e -i 2
%run method1_text_prompt.py -t baseline_justjson.j2 -p  0d3d703e -i 2
%run method1_text_prompt.py -t baseline_quotedgridcsv.j2 -p  0d3d703e -i 

%run method2_reflexion.py -t reflexion.j2 -p 08ed6ac7 -i 25
same restul



%run method1_text_prompt.py -t baseline_wquotedgridcsv_excel.j2 -p 08ed6ac7 -i 100
(Total success: 23, total n: 100, percentage: 23% without gridcsv excel)
RUNNING

%run run_all_problems.py -t baseline_justjson.j2  -i 100
RUNNING

%run run_all_problems.py -t baseline_wplaingrid.j2  -i 100
RUNNING

TODO maybe?
baseline_wquotedgridcsv_excel.j2

Just json, no grid repr, method1
#%run run_all_problems.py -t baseline_justjson.j2  -i 30
Results Summary:
    problem  all_correct_rate  at_least_one_correct_rate  total_runs  all_correct  at_least_one_correct
0  0d3d703e          0.466667                   0.500000          30           14                    15
1  08ed6ac7          0.400000                   0.400000          30           12                    12
2  9565186b          0.000000                   0.066667          30            0                     2
3  178fcbfb          0.200000                   0.366667          30            6                    11
4  0a938d79          0.000000                   0.000000          30            0                     0
Experiment took circa 40 mins
Provider counts: Counter({'Lambda': 150})
Max token usage on a call was 8096
Median token usage on a call was 1892


Json & plain grid, method1
#%run run_all_problems.py -t baseline.j2  -i 30
Results Summary:
    problem  all_correct_rate  at_least_one_correct_rate  total_runs  all_correct  at_least_one_correct
0  0d3d703e          0.633333                   0.666667          30           19                    20
1  08ed6ac7          0.300000                   0.300000          30            9                     9
2  9565186b          0.000000                   0.100000          30            0                     3
3  178fcbfb          0.233333                   0.233333          30            7                     7
4  0a938d79          0.000000                   0.000000          30            0                     0
Experiment took 0:09:14.121500
Provider counts: Counter({'Lambda': 150})
Max token usage on a call was 7400
Median token usage on a call was 2049




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

(baseline is now baseline_wplaingrid)
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
