# How to run the models locally

To run the model locally, there are 3 steps:
1. Download the repo
2. Install the libraries
3. Run the code

If you have any issues with the instructions below I'd (Joseph) be happy to help out over slack/Jitsi.

## Downloading the repo

To download the repo, go to the [main repo page](https://github.com/AIforGoodSimulator/model-server), and click the greed button at the top right of the list of files that says "code" and then click "download zip". It should then download into your downloads folder where you can unzip it.

## Installing libraries

The most common way to install a python library is by using pip. You can pip install a libarary by opening command prompt and typing `pip install {library name}`. If you do not have the libarary installed already, you will get a response that looks similar to (its different for different libraries) this:
```
C:\Users\josep>pip install {libarary}
Collecting {libarary}
  Downloading https://files.pythonhosted.org/packages/00/00/aaaa/{libarary}-0.0.0-cp00-cp00m-win_amd64.whl (1.0MB)
     |################################| 1.0MB 100kB/s
     ...
```
if you already have the library installed, the below will be printed:
```
C:\Users\josep>pip install {libarary}
Requirement already satisfied: {libarary} in c:\program files\python35\lib\site-packages
```
It might also attempt to install other libararies that it requires, so you may get a few lines that begin with "Requirement already satisfied", like with Pandas:
```
C:\Users\josep>pip install pandas
Requirement already satisfied: pandas in c:\users\josep\appdata\roaming\python\python35\site-packages (0.24.2)
Requirement already satisfied: pytz>=2011k in c:\users\josep\appdata\roaming\python\python35\site-packages (from pandas) (2020.1)
Requirement already satisfied: python-dateutil>=2.5.0 in c:\program files\python35\lib\site-packages (from pandas) (2.8.1)
Requirement already satisfied: numpy>=1.12.0 in c:\program files\python35\lib\site-packages (from pandas) (1.18.1)
Requirement already satisfied: six>=1.5 in c:\program files\python35\lib\site-packages (from python-dateutil>=2.5.0->pandas) (1.15.0)
```

### If pip doesn't work

It is pretty common to get the error `'pip' is not recognized as an internal or external command,
operable program or batch file.` This will happen if you do not have python added to your environment variable, which allows the console to know where the code that needs to be run when certain commands are entered.

To add pip to your environment variables:
1. search start for "environemnt variables" and open it
2. Click the button at the bottom right that says "environment variables"
3. In system variables (bottom winddow) double click "path", and then "new"
4. Add the directory that python is in on your pc (probably looks like: C:\Users\user\AppData\Local\Programs\Python\Python37-32\Scripts
5. Restart CMD

### requirements.txt

Instead of manually installing all of the libraries incividually, there is a file within the repo called "reqirements.txt". This allows us to install all the libraries at once with:
```
pip install -r requirements.txt
```
A lot of the libraries will not work with older versions of python (I originally tried with python 3.5 and many of them didn't work). I was able to install all the libararies with Python 3.8.5.

When we were installing the libararies we were getting errors with immutables, but the installations continued anyway and the code seems to be working fine, so I guess if you get that you could just ignore it.

After I installed requirements, I got a few errors when running the code with libraries not being installed (see example error below). If you get this, you can simply install the library manually and run again.

Error:
```
>>> import {library}
Traceback (most recent call last):
  File "<stdin>", line 1, in <module>
ModuleNotFoundError: No module named '{library}'
```
Fix:
```
pip install {library}
```

Because I have two versions of python on my computer, CMD often defaults to using the older version. If this is happening to you, it is sometimes the case that `python` refers to one version and `py` refers to another. If `py` refers to the later version of python for example, you can install and run files with the code below:
```
py -m pip install {library}
py file.py
```

## Running the code

To get into the correct folder (you want to be in the folder called `model-server-master`) to run the code, use the cd command. To open a folder within the directory you are currently in, you can write `cd {directory}`. If you want to go to a parent directory, you can use `cd ..`.

Before running the code, you need to tell python what the path we are working in is. If you don't do this, python will not know where to look for files you want to import from and you will get an error like:
```
Traceback (most recent call last):
  File "ai4good/runner/console_runner.py", line 6, in <module>
    from ai4good.models.model import Model, ModelResult
ModuleNotFoundError: No module named 'ai4good'
```
To do this, you need to write into CMD:
```
set PYTHONPATH=%PYTHONPATH%;
```
It shouldn't output anything after you run the above command.

Once this is all done, the files should be ready to run. You can run the following command to get help with commands for the conosle runner for the compartmental model:
```
C:\Users\...\model-server-master>py ai4good/runner/console_runner.py -h
usage: console_runner.py [-h] [--model {compartmental-model}] [--profile PROFILE | --run_all_profiles]
                         [--camp CAMP | --run_all_camps] [--do_not_load_from_model_result_cache]
                         [--do_not_save_to_model_result_cache] [--save_plots] [--show_plots] [--save_report]
                         [--profile_overrides PROFILE_OVERRIDES]

AI4Good model runner

optional arguments:
  -h, --help            show this help message and exit
  --model {compartmental-model}
                        Model to run
  --profile PROFILE     Model profile to run, by default first one will be run
  --run_all_profiles    Run all profiles in the model
  --camp CAMP           Camp to run model for
  --run_all_camps       Run all camps
  --do_not_load_from_model_result_cache
                        Do not load from cache, re-compute everything
  --do_not_save_to_model_result_cache
                        Do save results to cache
  --save_plots          Save plots
  --show_plots          Show plots
  --save_report         Save model report
  --profile_overrides PROFILE_OVERRIDES
                        Model specific profile overrides as JSON
```
To get a report, you can run:
```
python ai4good/runner/console_runner.py --save_report
```
The report will be saved in `\model-server-master\fs\reports`

This is what it outputs when I run all of this last section:
```
C:\Users\josep>cd C:\Users\...\model-server-master

C:\Users\...\model-server-master>set PYTHONPATH=%PYTHONPATH%;

C:\Users\...\model-server-master>py ai4good/runner/console_runner.py -h
usage: console_runner.py [-h] [--model {compartmental-model}] [--profile PROFILE | --run_all_profiles]
                         [--camp CAMP | --run_all_camps] [--do_not_load_from_model_result_cache]
                         [--do_not_save_to_model_result_cache] [--save_plots] [--show_plots] [--save_report]
                         [--profile_overrides PROFILE_OVERRIDES]

AI4Good model runner

optional arguments:
  -h, --help            show this help message and exit
  --model {compartmental-model}
                        Model to run
  --profile PROFILE     Model profile to run, by default first one will be run
  --run_all_profiles    Run all profiles in the model
  --camp CAMP           Camp to run model for
  --run_all_camps       Run all camps
  --do_not_load_from_model_result_cache
                        Do not load from cache, re-compute everything
  --do_not_save_to_model_result_cache
                        Do save results to cache
  --save_plots          Save plots
  --show_plots          Show plots
  --save_report         Save model report
  --profile_overrides PROFILE_OVERRIDES
                        Model specific profile overrides as JSON

C:\Users\...\model-server-master>py ai4good/runner/console_runner.py --save_report
INFO:root:Running compartmental-model model with baseline profile
INFO:root:Loading from model result cache
INFO:root:Saving report
...
```

# Temporary Model Server Code Explanation

When the user travels to the route "/", the below code is run from the [server.py](https://github.com/AIforGoodSimulator/model-server/blob/master/ai4good/webapp/server.py) file:
```python
@flask_app.route("/")  # Decorator specifies route this function is called on
def index():
    return redirect('/sim/run_model')
```
This redirects the user to the `run_model` route. The `display_page` function is then run in the same file. The pathname is now `/sim/run_model/`, so we return `run_model_page.layout` from the `display_page()` function (and display it).

## Run model page

We can see that `run_model_page` comes from the [run_model_page](https://github.com/AIforGoodSimulator/model-server/blob/master/ai4good/webapp/run_model_page.py) file from the imports at the top of the file.
```python
import ai4good.webapp.run_model_page as run_model_page
```
Within the `run_model_page` we can find the layout object.
```python
layout = html.Div(
    [
        html.H3('Run Model'),
        camp_selector(),
        model_selector(),
        profile_selector(),
        model_run_buttons(),
        history_table(),
        dcc.Interval(
            id='interval-component',
            interval=5 * 1000  # in milliseconds
        )
    ], style={'margin': 10}
)
```
The first line just adds the title `Run Model`, and then the `camp_selector()` function is called.

### Camp selector

```python
def camp_selector():
    return dbc.Row([
        dbc.Col(
            html.Div([
                html.Label('Camp', style={'font-weight': 'bold'}),
                dcc.Dropdown(
                    id='camp-dropdown',
                    options=[{'label': c, 'value': c} for c in facade.ps.get_camps()]
                ),
            ]),
            width=3,
        ),
        dbc.Col(html.Div([dbc.Card('', id='camp-info', body=True)], style={'height': '100%'}),
            width=6,
        ),
    ], style={'margin': 10})
```

The [camp_selector()](https://github.com/AIforGoodSimulator/model-server/blob/355af127713bf64115960503e1406d8a99873fe7/ai4good/webapp/run_model_page.py#L13) function returns an html table with two columns and one row. The left column contains a label with text `camp`
```python
html.Label('Camp', style={'font-weight': 'bold'}
```
and a dropdown menu
```python
dcc.Dropdown(
  id='camp-dropdown',
  options=[{'label': c, 'value': c} for c in facade.ps.get_camps()]
)
```
The labels are taken from facade, which can be found in the `apps.py` file in the same directory.
```python
from ai4good.runner.facade import Facade
facade = Facade.simple()
```
This `facade` object is created from a function that is imported within the `Facade` (capital `F`) class from the [facade.py](https://github.com/AIforGoodSimulator/model-server/blob/master/ai4good/runner/facade.py) file.

```python
from ai4good.params.param_store import ParamStore, SimpleParamStore
from ai4good.models.model_result_store import ModelResultStore, SimpleModelResultStore


class Facade:

    def __init__(self, ps: ParamStore, rs: ModelResultStore):
        self.ps = ps
        self.rs = rs

    @staticmethod
    def simple():
        return Facade(SimpleParamStore(), SimpleModelResultStore())
```

The `facade.py file is only 13 lines long (above), using classes from [model_result_store.py](https://github.com/AIforGoodSimulator/model-server/blob/master/ai4good/models/model_result_store.py), which get the values from pickled files in the same directory (which I think have been left out of the github repo).
```python
def load(self, model_id: str, result_id: str) -> Any:
        p = self._path(f"{model_id}_{result_id}.pkl")
        with open(p, 'rb') as handle:
            return pickle.load(handle)
```

These values are then displayed on the webapp in the dropdown menu.

On the right column of the table is a label that shows info about the camp selected.
```python
dbc.Col(html.Div([dbc.Card('', id='camp-info', body=True)],
  style={'height': '100%'}),
  width=6,
)
```
The card is initially left blank, and then updated with info when a camp is selected.

I'm not entirely sure how this is updated with the camp info. I think this may be due to some missing flask/dash knowledge, as I am not sure how dash is handling the `display_page()` function. Hopefully someone can explain this? For reference, the following decorator is used on the `display_page()` function:
```python
@dash_app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname'), Input('url', 'search')])
```
And the dropdown and card are given ids of `camp-dropdown` and `camp-info` respectively

### Model selector

The model selector is made in almost exactly the same way as the camp selector, but with different values and id. Function is below.

```python
def model_selector():
    return dbc.Row([
        dbc.Col(
            html.Div([
                html.Label('Model', style={'font-weight': 'bold'}),
                dcc.Dropdown(
                    id='model-dropdown',
                    options=[{'label': m, 'value': m} for m in facade.ps.get_models()]
                ),
            ]),
            width=3,
        ),
        dbc.Col(html.Div([dbc.Card('', id='model-info', body=True)], style={'height': '100%'}),
            width=6,
        ),
    ], style={'margin': 10})
```
### Profile selector
## Compartmental Model Results Page
## Compartmental Model Report Page
## Compartmental Model Admin Page

# Model Outputs

The model output seems to be held in a variable `mr` in the [cm_model_results_page file](https://github.com/AIforGoodSimulator/model-server/blob/master/ai4good/webapp/cm_model_results_page.py). 

mr comes from calling the `get_result` function on the model_runner object in ai4good/webapp/apps.
```python
mr = model_runner.get_result(CompartmentalModel.ID, profile, camp)
```
This object is an instance of the `ModelRunner` (not the same as `model_runner`) class that is from ai4good/webapp/model_runner.
```python
model_runner = ModelRunner(facade, _redis, dask_client)
```
The `ModelRunner` class is created with the above parameters. facade is used to store parameters and results:
```python
class Facade:

    def __init__(self, ps: ParamStore, rs: ModelResultStore):
        self.ps = ps
        self.rs = rs

    @staticmethod
    def simple():
        return Facade(SimpleParamStore(), SimpleModelResultStore())
```
When we get mr from calling the `get_result` function on the `model_runner` object in ai4good/webapp/apps, we run the below code:
```python
def get_result(self, _model: str, _profile: str, camp: str) -> ModelResult:
        _mdl: Model = get_models()[_model](self.facade.ps)
        params = create_params(self.facade.ps, _model, _profile, camp)
        res_id = _mdl.result_id(params)
        return self.facade.rs.load(_mdl.id(), res_id)
```
the `Model` object, `_mdl` is created by first getting a list of models, and then indexing the model we want to use using the `_model` parameter. `_model` is set to `CompartmentalModel.ID`, so this is the model we use. We then run the compartmental model on parameters from `self.facade.ps`, which is the param store that was entered with facade as a parameter when the `model_runner` object was created.

To find what info the model returns, we therefore need to look at the `get_models` function from ai4good/models/model_registry. There seems to only be one model returned by this function at the moment, which is imported from ai4good/models/cm/cm_model.
```python
def get_models() -> Dict[str, Any]:
    return {
        CompartmentalModel.ID: lambda ps: CompartmentalModel(ps)
    }
```
Within the `run` function of this model, the following is returned.
```python
return ModelResult(self.result_id(p), {
            #'sols_raw': sols_raw,
            'standard_sol': standard_sol,
            'percentiles': percentiles,
            'config_dict': config_dict,
            'params': p,
            'report': report_raw,
            'prevalence_age': prevalence_age,
            'prevalence_all': prevalence_all,
            'cumulative_all': cumulative_all,
            'cumulative_age': cumulative_age
        })
```

# model_results_store.py

This file is available here: https://github.com/AIforGoodSimulator/model-server/blob/master/ai4good/models/model_result_store.py

This page defines some methods to pickle and unpickle the model results, as well a method to check if the pickle file exists (although I am not too sure why this is, maybe someone else can explain?). 

```python
class SimpleModelResultStore(ModelResultStore):

    def store(self, model_id: str, result_id: str, obj: Any):
        p = self._path(f"{model_id}_{result_id}.pkl")
        with open(p, 'wb') as handle:
            pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)

    def load(self, model_id: str, result_id: str) -> Any:
        p = self._path(f"{model_id}_{result_id}.pkl")
        with open(p, 'rb') as handle:
            return pickle.load(handle)

    def exists(self, model_id: str, result_id: str) -> bool:
        p = self._path(f"{model_id}_{result_id}.pkl")
        return os.path.exists(p)
```

I haven't finished this section- didn't understand what the methods at the bottom were doing- so if anyone wants to finish off feel free, it's a very short page.




List of model outputs:
 - standard sol
 - percentiles
 - report
 - prevalence_age
 - prevalence_all
 - cumulative_all
 - cumulative_age

`run` function can be found here: https://github.com/AIforGoodSimulator/model-server/blob/355af127713bf64115960503e1406d8a99873fe7/ai4good/models/cm/cm_model.py#L12
