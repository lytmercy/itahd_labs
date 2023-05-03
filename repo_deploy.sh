#!/bin/bash

echo
echo "Downloading git repo - start"
echo

git clone https://github.com/lytmercy/itahd_labs.git
echo
echo ">>Repo download successfully"
python -m venv itahd_labs/itenv
echo
echo ">>Venv create successfully"
source ./itahd_labs/itenv/Scripts/activate
echo
echo ">>Venv" $VIRTUAL_ENV "Activated"
python -m pip install --upgrade pip
echo
echo ">>Pip upgrade successfully"
pip install -r itahd_labs/requirements.txt
echo
echo ">>Dependencies downloaded successfully"

echo
echo ">> DownLoad done <<"
