from code_names_bot_text_processor.model.baseline_model import BaselineModel
from code_names_bot_text_processor.model.classical_model import ClassicalModel
from enum import Enum
from config import PREDICTIONS_DIR

import os


class ModelType(Enum):
    BASELINE = 0,
    CLASSICAL = 1


def get_model(type):
    if type == ModelType.BASELINE:
        return BaselineModel()
    elif type == ModelType.CLASSICAL:
        return ClassicalModel()


def get_predictions_file_path(type):
    if type == ModelType.BASELINE:
        file_name = "baseline"
    elif type == ModelType.CLASSICAL:
        file_name = "classical"

    return os.path.join(PREDICTIONS_DIR, f"{file_name}.yaml")