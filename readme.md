# readme.md  

This repo is work in progress but the 
Easy to follow Jupyter Notebook tutorials and Utilties for the retail investors community interested in learning about **Technical Analysis**

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
