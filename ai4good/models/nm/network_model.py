from typeguard import typechecked
from ai4good.models.model import Model, ModelResult
from ai4good.params.param_store import ParamStore
import pandas as pd
import json
import hashlib
import logging


class NetworkModelParameters:

    def __init__(self, ps: ParamStore, camp: str, profile: pd.DataFrame, profile_override_dict={}):
        #TODO: read various params from param store
        pass

    def sha1_hash(self):
        hash_params = [
            #TODO:
        ]
        serialized_params = json.dumps(hash_params, sort_keys=True)
        hash_object = hashlib.sha1(serialized_params.encode('UTF-8'))
        _hash = hash_object.hexdigest()
        return _hash
        pass

@typechecked
class NetworkModel(Model):

    ID = 'r-network-model'

    def __init__(self, ps: ParamStore):
        Model.__init__(self, ps)

    def id(self) -> str:
        return self.ID

    def result_id(self, p: NetworkModelParameters) -> str:
        return p.sha1_hash()

    def run(self, p: NetworkModelParameters) -> ModelResult:
        #run R code here
        return ModelResult(self.result_id(p), {
            'params': p,

            #'report': report_raw,
            #any more results here
        })