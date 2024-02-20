import inquirer
import pandas as pd
from pathlib import Path
import requests
import typing
from tqdm import tqdm
from typing import List

HEADERS = {
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; rv:91.0) Gecko/20100101 Firefox/91.0'
}
ROOT_DIR = str(Path(__file__).absolute().parent.parent.parent)
