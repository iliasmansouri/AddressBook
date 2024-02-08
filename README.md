# AddressBook

Either build and run a docker container with
```cli
bash build_and_run.sh
```

once done go to: http://localhost:8501/

or create first a python environment a la:
```cli
conda create --name addressbook python=3.9 -y
conda activate addressbook
pip install -r requirements.txt
```

and run with:
```cli
streamlit run app.py
```

or feel free to run each of the following python-script separately:
- data_handler.py
- browser.py
- tests.py