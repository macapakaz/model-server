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
