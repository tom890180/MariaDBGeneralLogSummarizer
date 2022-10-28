# MariaDBGeneralLogSummarizer

Summarize an MariaDB/MySQL General log, e.g:
```
    18403 Query	SELECT * FROM Bar WHERE ID = 1    
    18403 Query	SELECT * FROM Foo WHERE ID = 1
    18403 Query	SELECT * FROM Foo WHERE ID = 1
    18403 Query	SELECT * FROM Foo WHERE ID = 2
    18405 Query	SELECT * FROM Foo WHERE ID = 3
    18402 Query	SET GLOBAL general_log = 'OFF'
```

ex:

```
$ python3.9 Summarize.py my.log
Total queries: 5


[4 - 80.00%]: SELECT * FROM Foo WHERE ID  = '*'
[1 - 20.00%]: SELECT * FROM Bar WHERE ID  = '*'   
```

```
$ python3.9 Summarize.py my.log --explicit
Total queries: 5


[2 - 40.00%]: SELECT * FROM Foo WHERE ID = 1
[1 - 20.00%]: SELECT * FROM Bar WHERE ID = 1    
[1 - 20.00%]: SELECT * FROM Foo WHERE ID = 2
[1 - 20.00%]: SELECT * FROM Foo WHERE ID = 3
```
