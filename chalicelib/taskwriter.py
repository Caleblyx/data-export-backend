from abc import abstractmethod
import pandas as pd

class TaskWriterInterface():
    @abstractmethod
    def addTaskChart(self, institutions, yMin, yMax, position):
        pass


class TaskWriter1(TaskWriterInterface):
    def __init__(self, dataFrame : pd.DataFrame , writer : pd.ExcelWriter):
        self.writer = writer
        self.workbook = writer.book

        
        columns = list(dataFrame.columns)
        self.nameToIdx = {}
        for idx, col in enumerate(columns):
            self.nameToIdx[col] = idx + 1


        dataFrame.to_excel(self.writer, "Graduates")
        self.tnp = self.workbook.add_worksheet('Trends and Projections charts')

        for column in columns:
            column_width = max(dataFrame[column].astype(str).map(len).max(), len(column)) + 10
            col_idx = self.nameToIdx[column]
            writer.sheets['Graduates'].set_column(col_idx, col_idx, column_width)

    def addTaskChart(self, institutions, yMin, yMax, position):
        colors = iter(["black", "red", "green", "blue", "yellow"])
        chart = self.workbook.add_chart({'type' : 'scatter'})
        yearColIdx = self.nameToIdx["year"]
        for institution in institutions:
            color = next(colors)
            colIdx = self.nameToIdx[institution]
            chart.add_series({
                'name' : ["Graduates", 0, colIdx],
                'categories' : ["Graduates", 1, yearColIdx, 5, yearColIdx],
                'values' : ["Graduates", 1, colIdx, 5, colIdx],
                'marker' : {
                            'type' : "diamond",
                            'fill' : {"color": color}
                            },
                'trendline' : { 
                                'type' : 'log',
                                'forward' : 5,
                                'line' : {
                                    'color' : color
                                },
                            }
            })
        chart.set_y_axis({'name' : "Number of Graduates", "min": yMin, "max": yMax})
        chart.set_x_axis({'name': "Years", 'major_unit': 1, "min": 2016, "max": 2025, 'num_font':  {'rotation': 45}})
        self.tnp.insert_chart(position, chart)



class TaskWriter2(TaskWriterInterface):
    def __init__(self, dataFrame1: pd.DataFrame, dataFrame2:pd.DataFrame, writer :pd.DataFrame):
        self.writer = writer
        self.workbook = writer.book

        columns = list(dataFrame2.columns)
        self.nameToIdx = {}
        for idx, col in enumerate(columns):
            self.nameToIdx[col] = idx + 1

        dataFrame1.to_excel(self.writer, "Intakes")

        for column in columns:
            column_width = max(dataFrame1[column].astype(str).map(len).max(), len(column)) + 10
            col_idx = self.nameToIdx[column]
            writer.sheets['Intakes'].set_column(col_idx, col_idx, column_width)

        dataFrame2.to_excel(self.writer, "Percentage of Difference")

        for column in columns:
            column_width = max(dataFrame2[column].astype(str).map(len).max(), len(column)) + 10
            col_idx = self.nameToIdx[column]
            writer.sheets['Percentage of Difference'].set_column(col_idx, col_idx, column_width)

        

        self.pod = self.workbook.add_worksheet('Percentage of Difference charts')
    
    def addTaskChart(self, institutions, yMin, yMax, position):
        chart = self.workbook.add_chart({'type' : 'column'})
        yearColIdx = self.nameToIdx["year"]
        for institution in institutions:
            colIdx = self.nameToIdx[institution]
            chart.add_series({
                'name' : ["Percentage of Difference", 0, colIdx],
                'categories' : ["Percentage of Difference", 1, yearColIdx, 5, yearColIdx],
                'values' : ["Percentage of Difference", 1, colIdx, 5, colIdx],
            })
        chart.set_y_axis({'name' : "Percentage of Difference", "min": yMin, "max": yMax})
        chart.set_x_axis({'name': "Years", 'major_unit': 1, "min": 2016, "max": 2020, 'num_font':  {'rotation': 45}})
        self.pod.insert_chart(position, chart)