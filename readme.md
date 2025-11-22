# readme.md  

Easy Notebook Tutorials and Utilties, for learning/exploring **Technical Analysis**

<img src="https://encrypted-tbn1.gstatic.com/licensed-image?q=tbn:ANd9GcRwPcYN4eW0ESEmksgxAfc5r2Z_0aLrrhH0oqJSZmR5TbybgycXJru7-YLs465dxwCupVHBMEUW7rmE5QKYWyX5UH8JBiEXS35WuZcRxucX_vlU6rc" alt="Technical Analysis" width="300" height="150"/>

Example Notebook showing SMA Crossover  [A Moving Average Crossover Strategy -- Example for NVDA](https://lgtkgtv.github.io/Technical-Analysis/HTML/)

## Setup  
```
uv venv .venv --python 3.12
source .venv/bin/activate

uv pip install --upgrade google-genai

uv pip install yfinance pandas numpy tabulate
uv pip install jupyterlab 
uv pip install ipykernel  
uv pip install ipywidgets
uv pip install joblib         # ideal library for efficiently caching large Python objects (like pandas DataFrames) to the disk.

python -m ipykernel install --user --name=uv_project --display-name="Python (uv project)"

jupyter notebook
```

