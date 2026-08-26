from project_manager import ProjectManager
from trainer import Trainer
from evaluator import Evaluator
from prelabeler import Prelabeler
from label_studio_manager import LabelStudioManager

class AutoTrainer:
    """ Manager class where all the magic happens folks

    @author: Sami Ibrahim
    @version: 8/21/2026
    
    """

    def __init__(
            self,
            proj_dir,
            data_dir,
            model,
        ):
        self.project_manager = ProjectManager(proj_dir)
        self.evaluator = Evaluator(self.project_manager)
        self.trainer = Trainer(model)
        self.prelabeler = Prelabeler()
        self.label_studio_manager = LabelStudioManager()

        self.project_manager.create_project(name="auto-train_" + model, data_dir=data_dir)



    def start(self, labels_json):        

        #STEP 1 - initial training try out 3 fixed param configurations to get imgsz, batch size and epoch number
        self.trainer.train(cfg="")
        self.trainer.tune()

        paramsets = self.evaluator.params()
        self.trainer.train(paramsets)
        self.evaluator.generate_report()
        self.prelabeler.seg_predict()
        self.label_studio_manager.launch()
        self.label_studio_manager.import_json()
        # Review on labelstudio
        