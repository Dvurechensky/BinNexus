> Разделение на модульную архитектуру при прикручивании Ghidra и IDA анализаторов

```

├── core/
│   ├── scanner.py        # file traversal
│   ├── imports.py        # dumpbin
│   ├── exports.py        # pefile
│   ├── filters.py        # noise
│   └── graph.py          # nodes/edges
│
├── output/
│   ├── html.py
│   ├── search.py
│   └── writer.py
│
├── cli.py
└── main.py

```
