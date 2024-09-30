# sample1

Init.

```
$ rye sync
```

For debug.

```
$ debug-server
INFO:     Started server process [22922]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
...
```

For production.

```
$ uvicorn sample1.cmd.main:app --host 0.0.0.0 --port 8000 --workers 4
```
