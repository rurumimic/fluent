# fluent

- [fluentd](https://www.fluentd.org/)
- docs
  - [fluentd](https://docs.fluentd.org/)
  - [fluentbit](https://docs.fluentbit.io/)
- k8s
  - [logging](https://kubernetes.io/docs/concepts/cluster-administration/logging/)
- repo
  - [fluent-logger-python](https://github.com/fluent/fluent-logger-python)

## examples

### sidecar container with a logging agent

```bash
kubectl apply -f tcp.yaml
```

#### tail logs

```bash
kubectl logs -l app=app -c app -f
```

```json
{"level":"INFO", "message":"Log number 0", "timestamp":"Sat Oct 12 14:52:27 UTC 2024"}
{"level":"INFO", "message":"Log number 1", "timestamp":"Sat Oct 12 14:52:32 UTC 2024"}
{"level":"INFO", "message":"Log number 2", "timestamp":"Sat Oct 12 14:52:37 UTC 2024"}
{"level":"INFO", "message":"Log number 3", "timestamp":"Sat Oct 12 14:52:42 UTC 2024"}
{"level":"INFO", "message":"Log number 4", "timestamp":"Sat Oct 12 14:52:47 UTC 2024"}
```

```bash
kubectl logs -l app=app -c fluent-bit -f
```

```
Fluent Bit v3.1.9
* Copyright (C) 2015-2024 The Fluent Bit Authors
* Fluent Bit is a CNCF sub-project under the umbrella of Fluentd
* https://fluentbit.io

______ _                  _    ______ _ _           _____  __
|  ___| |                | |   | ___ (_) |         |____ |/  |
| |_  | |_   _  ___ _ __ | |_  | |_/ /_| |_  __   __   / /`| |
|  _| | | | | |/ _ \ '_ \| __| | ___ \ | __| \ \ / /   \ \ | |
| |   | | |_| |  __/ | | | |_  | |_/ / | |_   \ V /.___/ /_| |_
\_|   |_|\__,_|\___|_| |_|\__| \____/|_|\__|   \_/ \____(_)___/

[2024/10/12 14:52:28] [ info] [fluent bit] version=3.1.9, commit=431fa79ae2, pid=1
[2024/10/12 14:52:28] [ info] [storage] ver=1.5.2, type=memory, sync=normal, checksum=off, max_chunks_up=128
[2024/10/12 14:52:28] [ info] [cmetrics] version=0.9.6
[2024/10/12 14:52:28] [ info] [ctraces ] version=0.5.6
[2024/10/12 14:52:28] [ info] [input:tcp:tcp.0] initializing
[2024/10/12 14:52:28] [ info] [input:tcp:tcp.0] storage_strategy='memory' (memory only)
[2024/10/12 14:52:28] [ info] [sp] stream processor started
[2024/10/12 14:52:28] [ info] [output:stdout:stdout.0] worker #0 started
[0] app.tcp.*: [[1728744752.911389389, {}], {"level"=>"INFO", "message"=>"Log number 1", "timestamp"=>"Sat Oct 12 14:52:32 UTC 2024"}]
[0] app.tcp.*: [[1728744757.916534687, {}], {"level"=>"INFO", "message"=>"Log number 2", "timestamp"=>"Sat Oct 12 14:52:37 UTC 2024"}]
[0] app.tcp.*: [[1728744762.923420675, {}], {"level"=>"INFO", "message"=>"Log number 3", "timestamp"=>"Sat Oct 12 14:52:42 UTC 2024"}]
[0] app.tcp.*: [[1728744767.929010853, {}], {"level"=>"INFO", "message"=>"Log number 4", "timestamp"=>"Sat Oct 12 14:52:47 UTC 2024"}]
```

### fluent logger python

```bash
cd app
docker build -t fluent-logger:0.1.0 .
```

```bash
kubectl apply -f python.yaml
```

#### http request

```bash
curl "localhost:30080"

[0] app.tcp.log: [[1728810012.000000000, {}], {
  "host"=>"app-deploy-844f6fdb68-nvmbn",
  "where"=>"routes.home",
  "type"=>"INFO",
  "stack_trace"=>"None",
  "message"=>"Hello, World!"
}]
```

```bash
curl "localhost:30080/items/12?q=123"

[0] app.tcp.log: [[1728810033.000000000, {}], {
  "host"=>"app-deploy-844f6fdb68-nvmbn",
  "where"=>"routes.read_item",
  "type"=>"INFO",
  "stack_trace"=>"None",
  "message"=>"{'item_id': 12, 'q': '123'}",
  "item_id"=>12,
  "q"=>"123"
}]
```

