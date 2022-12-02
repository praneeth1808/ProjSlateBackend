import boto3
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np
from JsonModel.utility import getDataFilePath
import uuid


def generate_graphs(df):
    if df is None:
        return {"Graph1": "", "Graph2": ""}

    if not df.empty:
        print("Perform operations")
    graph_one_id = str(uuid.uuid4())+".png"
    plt.plot([0, 1, 2, 3, 4], [0, 3, 5, 9, 11])
    plt.xlabel('Months')
    plt.ylabel('Books Read')
    plt.savefig(graph_one_id)
    data = 'https://vincentarelbundock.github.io/Rdatasets/csv/datasets/mtcars.csv'

    df_test = pd.read_csv(data, index_col=0)
    df_test.head(6)
    sns.distplot(df_test['mpg'])

    # Saving the Seaborn Figure:
    plt.savefig('save_as_a_png.png')
    # # Try Self
    # df_new = pd.read_csv(getDataFilePath("iris.csv"))
    # df_new['SepalWidth'].value_counts().plot(kind='bar')
    # plt.savefig('visualization1.png')
    # # End try

    # plt.boxplot(df['SepalLength'].value_counts(), notch=None,
    #             vert=None, patch_artist=None, widths=None)
    # plt.savefig('visualization2.png')

    # Here are my AWS keys
    access_key = "AKIAVHIF3775VD7BVKJV"
    secret = "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"

    # Connecting to s3 instance using keys
    s3 = boto3.resource("s3", aws_access_key_id=access_key,
                        aws_secret_access_key=secret)
    s3_client = boto3.client(
        's3', aws_access_key_id=access_key, aws_secret_access_key=secret)

    # Specifying bucket
    bucket = s3.Bucket('project-slate-bucket')

    # Deleting all contents of bucket first
    bucket.objects.all().delete()

    # Then uploading the two visualizations
    s3_client.upload_file(
        Filename=graph_one_id,
        Bucket="project-slate-bucket",
        Key=graph_one_id,
    )

    # s3_client.upload_file(
    #     Filename="visualization2.png",
    #     Bucket="project-slate-bucket",
    #     Key="visualization2.png",
    # )

    # # Specifying object urls (objects have same name as details used when uploading to bucket)
    url1 = 'https://project-slate-bucket.s3.amazonaws.com/'+graph_one_id
    url2 = 'https://project-slate-bucket.s3.amazonaws.com/visualization2.png'

    # Removing the local png files from system
    os.remove(graph_one_id)
    # os.remove('visualization2.png')

    # return (url1, url2)
    return {"Graph1": url1, "Graph2": url2}
