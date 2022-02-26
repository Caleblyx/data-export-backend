from chalice import Chalice
import boto3
import botocore
import io
import os
from chalicelib.excelcreator import ExcelCreator

app = Chalice(app_name='data-export-backend')
BUCKET = "data-export-project"

@app.route('/download', cors = True)
def getDownloadLink():
    try:
        saveExcelToS3()
    except botocore.exceptions.ClientError as e:
        return {"status-code" : e.response['Error']['Code']}
    s3_client = boto3.client('s3')
    response = s3_client.generate_presigned_url('get_object',
                                                    Params={'Bucket': BUCKET,
                                                            'Key': "analysis.xlsx"},
                                                    ExpiresIn=3600)
    return {"status-code": "200 OK", "download-link":response}

def saveExcelToS3():
    storage = boto3.resource('s3')
    try:
        storage.Object(BUCKET,'analysis.xlsx').load()
    except botocore.exceptions.ClientError as e:
        if e.response['Error']['Code'] == "404":
        # The object does not exist.
            with io.BytesIO() as output:
                creator = ExcelCreator(output)
                creator.generateExcel()
                storage.Object(BUCKET, "analysis.xlsx").put(Body = output.getvalue())
        else:
        # Something else has gone wrong.

            raise
