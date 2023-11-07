# transformer libs
from transformers import AutoModelForSequenceClassification
from transformers import AutoTokenizer
import torch
import numpy as np

class ModelSingleton(object):
    '''Provides a singleton of pretrained transformer model'''

    def __new__(cls):
        if not hasattr(cls, 'instance'):
            cls.instance = super(ModelSingleton, cls).__new__(cls)
        return cls.instance

    def __init__(self):
        self.model = AutoModelForSequenceClassification.from_pretrained("../transormer_multi_model/")
        print('got model, getting tokenizer')
        self.tokenizer = AutoTokenizer.from_pretrained("../transormer_multi_model/")
        print('got tokenizer')

    def eval_message(self, msg):
        ''' Loads transformer based tokenizer and model. Evaluates input on this.
            INPUT:
                msg       - single text message to be evaluated

            
            OUTPUT:
                list of predicted categories
        '''
        id2label = {0: 'related',
                    1: 'request',
                    2: 'offer',
                    3: 'aid_related',
                    4: 'medical_help',
                    5: 'medical_products',
                    6: 'search_and_rescue',
                    7: 'security',
                    8: 'military',
                    9: 'child_alone',
                    10: 'water',
                    11: 'food',
                    12: 'shelter',
                    13: 'clothing',
                    14: 'money',
                    15: 'missing_people',
                    16: 'refugees',
                    17: 'death',
                    18: 'other_aid',
                    19: 'infrastructure_related',
                    20: 'transport',
                    21: 'buildings',
                    22: 'electricity',
                    23: 'tools',
                    24: 'hospitals',
                    25: 'shops',
                    26: 'aid_centers',
                    27: 'other_infrastructure',
                    28: 'weather_related',
                    29: 'floods',
                    30: 'storm',
                    31: 'fire',
                    32: 'earthquake',
                    33: 'cold',
                    34: 'other_weather',
                    35: 'direct_report'}
        text = msg

        encoding = self.tokenizer(text, return_tensors="pt")
        encoding = {k: v.to(self.model.device) for k,v in encoding.items()}

        outputs = self.model(**encoding)
        # logits is a tensor containing the scores for each label
        logits = outputs.logits
        logits.shape
        # apply sigmoid + threshold
        sigmoid = torch.nn.Sigmoid()
        probs = sigmoid(logits.squeeze().cpu())
        predictions = np.zeros(probs.shape)
        predictions[np.where(probs >= 0.5)] = 1
        # turn predicted id's into actual label names
        predicted_labels = [id2label[idx] for idx, label in enumerate(predictions) if label == 1.0]
        return predicted_labels

