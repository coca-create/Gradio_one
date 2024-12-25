import os
import sys
import gradio as gr
import json
from gradio_components import gr_components as gc
import warnings
from datetime import datetime


warnings.filterwarnings("ignore", category=FutureWarning)
#print("Current working directory:", os.getcwd())
# 必要なら作業ディレクトリをスクリプトのディレクトリに変更

css="""

    .my-table-container {
        font-family:inherit !important;
        max-height: 400px;
        overflow-y: auto;
        border: 0.5px solid gray !important;
        padding: 10px;
        width:100%;
        margin:auto;
    }
    .my-table-wrapper {
        display: flex;
        justify-content: center;
    }
    .table {
        width: 100%;
        font-family:inherit;
        border:0.5px solid gray;
    }
    .dataframe{
        width:100%;
    }

    table { width: 100%; }
    
    
    """


if __name__=="__main__":
    with gr.Blocks(css=css) as UI:
        gc.gr_components()
    UI.launch(debug=True, share=True)