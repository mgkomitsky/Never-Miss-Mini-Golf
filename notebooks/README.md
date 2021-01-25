 # instructions to set up notebook in a venv

Do not use if you are not using a python virtual enviroment:

```
. venv/bin/activate
 python3 -m pip install ipykernel
 ipython kernel install --user --name=NMMGkernel
 jupyter notebook
 ```

 Be sure to chose NMMGkernel kernel