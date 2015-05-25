# HOW TO USE

```
#!/bin/bash

git clone https://github.com/wtelecom/net-interviewer -b jobQueue

cd net-interviewer
source bin/activate
pip install -r requirements.txt
cd src/jobs/

python simple_test.py
```

# TODO
0. Define how much queues will be used
1. Build jobs producer. It will create (schedule) messages (jobs) each X seconds
* Build jobs consumer. Depending on the topic, a function (handler) will be called
* Build Topic creator. Managed of care if the topics had been created before all.
* Managed lost of data. How can I use the index of each topic?
