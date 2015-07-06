README.MD

Profiling test:

```bash
python snmp/table.py
       2050004 function calls in 0.976 seconds

 Ordered by: standard name

 ncalls  tottime  percall  cumtime  percall filename:lineno(function)
      1    0.000    0.000    0.976    0.976 <string>:1(<module>)
  10000    0.006    0.000    0.006    0.000 table.py:14(__init__)
  10000    0.029    0.000    0.927    0.000 table.py:23(request)
  10000    0.445    0.000    0.818    0.000 table.py:35(_process_body)
  10000    0.019    0.000    0.951    0.000 table.py:47(do)
      1    0.025    0.025    0.976    0.976 table.py:57(do_times)
  20000    0.001    0.000    0.001    0.000 {len}
      1    0.000    0.000    0.000    0.000 {method 'disable' of '_lsprof.Profiler' objects}
  90000    0.079    0.000    0.079    0.000 {method 'split' of 'str' objects}
1820000    0.355    0.000    0.355    0.000 {method 'translate' of 'str' objects}
  80001    0.018    0.000    0.018    0.000 {range}
      ```
