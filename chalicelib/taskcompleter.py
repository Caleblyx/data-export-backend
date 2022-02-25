from abc import abstractmethod
from chalicelib.taskwriter import TaskWriterInterface

class TaskCompleterInterface():
    @abstractmethod
    def completeTask(self):
        pass

class TaskCompleter(TaskCompleterInterface):
    def __init__(self, taskwriter : TaskWriterInterface, chartParams):
        self.taskwriter = taskwriter
        self.chartParams = chartParams

    
    def completeTask(self):
        for param in self.chartParams:
            self.taskwriter.addTaskChart(param["institutes"], param["yMin"], param["yMax"], param["position"])


