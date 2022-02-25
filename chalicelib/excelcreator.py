import pandas as pd
from chalicelib.importer import DataFrameImporter
from chalicelib.taskcompleter import TaskCompleter
from chalicelib.taskwriter import TaskWriter1, TaskWriter2
from chalicelib.dataurls import GRADUATES, INTAKES
from chalicelib.chartparams import TASK1, TASK2
from chalicelib.transformer import DataFrameTransformer
import os
class ExcelCreator():
    def __init__(self, file):
        self.writer = pd.ExcelWriter(file, engine = 'xlsxwriter')

    def generateExcel(self):
        #Create sheets for Task 1
        gradDf = DataFrameImporter(GRADUATES).getFilteredDataFrame("sex", "MF")
        taskWriter = TaskWriter1(gradDf, self.writer)
        taskCompleter = TaskCompleter(taskWriter, TASK1)
        taskCompleter.completeTask()
        #Create sheets for Task 2
        intakeDf = DataFrameImporter(INTAKES).getFilteredDataFrame("sex", "MF")
        transformer = DataFrameTransformer()
        percOfDiffDf = transformer.getPercOfDiffDf(gradDf, intakeDf, ["_id", "year", "sex"])
        taskWriter = TaskWriter2(intakeDf, percOfDiffDf, self.writer)
        taskCompleter = TaskCompleter(taskWriter, TASK2)
        taskCompleter.completeTask()
        self.writer.save()
