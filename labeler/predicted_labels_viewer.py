import yaml

from .labeler_window import LabelerWindow
from .labeler import Labeler
from .labels import Label
from models import ModelType, get_predictions_file_path


class PredictedLabelsWindow(LabelerWindow):
    def set_predicted_labels(self, predicted_labels):
        self.predicted_labels = predicted_labels
    
    def _create_token_widget(self, i):
        if self.predicted_labels is None:
            return None
        
        widget, layout = super()._create_token_widget(i)
        predicted_label_widget = self._create_label_widget(self.predicted_labels[i])
        layout.addWidget(predicted_label_widget)
        return widget, layout


class PredictedLabelsViewer(Labeler):
    def __init__(self):
        super().__init__()
        with open(get_predictions_file_path(ModelType.CLASSICAL), "r") as file:
            self.predictions = yaml.safe_load(file)

    def _create_window(self):
        return PredictedLabelsWindow()

    def set_definition(self):
        current_key = self.keys[self.current]

        if current_key in self.predictions:
            predicted_labels = [Label(label) for label in self.predictions[current_key]]
            self.widget.set_predicted_labels(predicted_labels)
        else:
            self.widget.set_predicted_labels(None)
        
        super().set_definition()
    

def main():
    labeler = PredictedLabelsViewer()
    labeler.start()


if __name__ == "__main__":
    main()
