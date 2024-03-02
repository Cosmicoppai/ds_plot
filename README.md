# Installation

```bash
pip install -r requirements.txt

# To create a graph
cd plotter && python main.py --filename={file_name}.log

# To run server
# cd to root directory

python main.py
```

# Usage

```bash
# Arguments accepted by plotter/main.py
--filename: Name of the log file
--time_window: Time window for the graph
--output: Name of the output file
--current_time: Current time to be used for the graph
--time_res: Time resolution for the graph
```