
# No reflexion, simple prompt

## json, then with plain grid, then better grid & excel

%run run_all_problems.py -t baseline_justjson.j2  -i 100
    problem  all_correct_rate  at_least_one_correct_rate  total_runs  all_correct  at_least_one_correct
0  0d3d703e              0.46                       0.55         100           46                    55
1  08ed6ac7              0.41                       0.41         100           41                    41
2  178fcbfb              0.17                       0.21         100           17                    21
3  9565186b              0.00                       0.11         100            0                    11
4  0a938d79              0.00                       0.00         100            0                     0
Experiment took 1:52:37.985472

%run run_all_problems.py -t baseline_wplaingrid.j2  -i 100
Results Summary:
    problem  all_correct_rate  at_least_one_correct_rate  total_runs  all_correct  at_least_one_correct
0  0d3d703e              0.67                       0.75         100           67                    75
1  08ed6ac7              0.20                       0.20         100           20                    20
2  178fcbfb              0.14                       0.15         100           14                    15
3  9565186b              0.00                       0.07         100            0                     7
4  0a938d79              0.00                       0.00         100            0                     0
Experiment took 1:59:15.627492

%run run_all_problems.py -t baseline_wquotedgridcsv_excel.j2  -i 100
    problem  all_correct_rate  at_least_one_correct_rate  total_runs  all_correct  at_least_one_correct
0  0d3d703e              0.63                       0.67         100           63                    67
1  08ed6ac7              0.38                       0.38         100           38                    38
2  178fcbfb              0.27                       0.35         100           27                    35
3  9565186b              0.00                       0.22         100            0                    22
4  0a938d79              0.00                       0.02         100            0                     2
Experiment took 1:59:00.945262


# Use of Reflexion
 
## first with an easy problem, reflexion 3 and 5 iterations vs 1 (above), plain grid


%run method2_reflexion.py -t reflexion.j2 -p 08ed6ac7 -i 100
REFLEXION=3
Total success: 54, total n: 100, percentage: 54%
95% (1.96 SD) CI error interval: 9.77 i.e. 44.23 to 63.77
Provider counts: Counter({'Lambda': 466})
Max token usage on a call was 3,853, Median token usage on a call was 2,305
Experiment took 1:38:15.071390

%run method2_reflexion.py -t reflexion.j2 -p 08ed6ac7 -i 100
REFLEXION=5
Total success: 70, total n: 100, percentage: 70%
95% (1.96 SD) CI error interval: 8.98 i.e. 61.02 to 78.98
Provider counts: Counter({'Lambda': 616})
Max token usage on a call was 4,242, Median token usage on a call was 2,357
Experiment took 2:12:19.665814

%run method2_reflexion.py -t reflexion.j2 -p 08ed6ac7 -i 10
REFLEXION=7
Total success: 8, total n: 10, percentage: 80%
95% (1.96 SD) CI error interval: 2.48 i.e. 5.52 to 10.48
Provider counts: Counter({'Lambda': 64})
Max token usage on a call was 4,582, Median token usage on a call was 2,482
Experiment took 0:12:24.830306
Full logs in:
experiments/exp_20250925T184719/experiment.log

%run method2_reflexion.py -t reflexion.j2 -p 08ed6ac7 -i 10
REFLEXION=9
Total success: 10, total n: 10, percentage: 100%
95% (1.96 SD) CI error interval: 0.00 i.e. 10.00 to 10.00
Provider counts: Counter({'Lambda': 60})
Max token usage on a call was 4,660, Median token usage on a call was 2,441
Experiment took 0:11:14.453969
Full logs in:
experiments/exp_20250925T184757/experiment.log

## then on a harder problem which scores 0 in the non-reflexion scenario, strong representation

reflexion 3
%run method2_reflexion.py -t reflexion_wquotedgridcsv_excel.j2 -p 9565186b -i 20
Total success: 0, total n: 20, percentage: 0%
95% (1.96 SD) CI error interval: 0.00 i.e. 0.00 to 0.00
Provider counts: Counter({'Lambda': 120})
Max token usage on a call was 2,767, Median token usage on a call was 2,204
Experiment took 0:21:48.178928

reflexion 5
%run method2_reflexion.py -t reflexion_wquotedgridcsv_excel.j2 -p 9565186b -i 20
Total success: 1, total n: 20, percentage: 5%
95% (1.96 SD) CI error interval: 1.91 i.e. -0.91 to 2.91
Provider counts: Counter({'Lambda': 198})
Max token usage on a call was 3,962, Median token usage on a call was 2,300
Experiment took 0:38:34.153013
experiments/exp_20250925T152952/experiment.log
sqlite3 experiments/exp_20250925T152952/experiments.db
python run_code.py -c example_solutions/ex_poor_soln_9565186b_didnotgeneralise.py
the solution didn't really generalise

reflexion 7
Total success: 0, total n: 20, percentage: 0%
95% (1.96 SD) CI error interval: 0.00 i.e. 0.00 to 0.00
Provider counts: Counter({'Lambda': 280})
Max token usage on a call was 5,899, Median token usage on a call was 2,414
Experiment took 0:59:18.755429
Full logs in:
experiments/exp_20250925T153019/experiment.log

reflexion 9
Total success: 0, total n: 20, percentage: 0%
95% (1.96 SD) CI error interval: 0.00 i.e. 0.00 to 0.00
Provider counts: Counter({'Lambda': 360})
Max token usage on a call was 5,962, Median token usage on a call was 2,514
Experiment took 1:18:20.896764
Full logs in:
experiments/exp_20250925T162142/experiment.log

reflexion 11
Total success: 2, total n: 20, percentage: 10%
95% (1.96 SD) CI error interval: 2.63 i.e. -0.63 to 4.63
Provider counts: Counter({'Lambda': 404})
Max token usage on a call was 7,404, Median token usage on a call was 2,524
Experiment took 1:23:51.251955
Full logs in:
experiments/exp_20250925T164344/experiment.log
sqlite3 experiments/exp_20250925T164344/experiments.db
Total success: 0, total n: 20, percentage: 0%
Total success: 1, total n: 20, percentage: 5%
experiments/exp_20250925T183323/experiment.log
but all these successes are overfitted and have the wrong rule (but they do pass)

---------------------------

%run method1_text_prompt.py -t baseline_wquotedgridcsv_excel.j2 -p 08ed6ac7 -i 100
(Total success: 23, total n: 100, percentage: 23% without gridcsv excel)
Total success: 39, total n: 100, percentage: 39%
95% (1.96 SD) CI error interval: 9.56 i.e. 29.44 to 48.56
Experiment took 0:15:53.046025

is a 2-part prompt any different? no obvious difference within CI
%run method1_text_prompt_in2part2.py -t baseline_wquotedgridcsv_excel_for2parts.j2 -p 08ed6ac7 -i 100
Total success: 16, total n: 100, percentage: 16%
95% (1.96 SD) CI error interval: 7.19 i.e. 8.81 to 23.19
Provider counts: Counter({'Lambda': 200})
Max token usage on a call was 5,591, Median token usage on a call was 4,329
Experiment took 0:24:56.579797



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





Old TESTING
%run method2_reflexion.py -t reflexion.j2 -p 0d3d703e -i 2
%run method2_reflexion.py -t reflexion_wquotedgridcsv_excel.j2 -p 0d3d703e -i 2


%run method1_text_prompt.py -t baseline_justjson.j2 -p  0d3d703e -i 2
%run method1_text_prompt.py -t baseline_quotedgridcsv.j2 -p  0d3d703e -i 

%run method2_reflexion.py -t reflexion.j2 -p 08ed6ac7 -i 25
same restul