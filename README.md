![clockit](images/clockit.png)

# clockit

A super lightweight utility to time your Python code — nothing more, nothing less.

## usage

Install with `pip install clockit-code` or with `uv pip install clockit-code`.

Then import with `from clockit import clockit`

### Example 1: Timing Data Loading
```python
from clockit import clockit
import pandas as pd

with clockit(name="load csv") as ct:
    df = pd.read_csv("big_data.csv")
print(ct)  # load csv: X.XXX seconds
```

### Example 2: Timing Model Training
```python
from clockit import clockit
from sklearn.ensemble import RandomForestClassifier

X, y = ...  # your features and labels
model = RandomForestClassifier()

with clockit(printer=print, name="fit model") as ct:
    model.fit(X, y)
# Output: fit model: X.XXX seconds
```

### Example 3: Batch Processing with Nested Timers
```python
from clockit import clockit
import time

data_batches = [range(1000), range(1000), range(1000)]

with clockit(printer=print, name="total batch processing") as ct_total:
    for i, batch in enumerate(data_batches):
        with clockit(printer=print, name=f"process batch {i+1}") as ct:
            time.sleep(0.5)  # simulate processing
print(ct_total)  # total batch processing: X.XXX seconds
```

### Example 4: Accessing Raw Timing Data
```python
with clockit() as ct:
    # expensive operation
    ...
print(ct.elapsed)   # 1.234 (float seconds)
print(ct.readout)   # 'Time: 1.234 seconds'
```

### Example 5: Custom Formatting
```python
# Custom formatting
def my_printer(msg):
    print(f"⏱️  {msg}")

with clockit(printer=my_printer) as ct:
    time.sleep(1)
```

See more examples in `examples.ipynb`

## why clockit?

- 🪶 Lightweight: zero dependencies, minimal footprint
- 🧩 Drop-in: works anywhere
- 🤫 Silent by default, but easy to log or print
- 🏗️ Perfect for steps, scripts, or experiments
- 🕶️ No configuration, no boilerplate, just timing

## Limitations

- **Wall-clock time only:**
  - clockit uses `time.perf_counter()`, which measures elapsed (wall) time, not CPU time. This includes time spent sleeping or waiting on I/O.
- **Single-threaded timing:**
  - clockit does not account for parallel or asynchronous execution. If your code spawns threads, processes, or async tasks, the timer only tracks the main context and won't reflect per-task durations or concurrency effects.
- **No GPU/CUDA synchronization:**
  - For GPU workloads (e.g., PyTorch, TensorFlow), clockit does not synchronize with CUDA or other accelerators. Measured time may not reflect actual device execution time unless you manually synchronize before/after timing.
