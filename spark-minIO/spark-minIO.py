from minio import Minio
from pyspark.sql import SparkSession
from pyspark import SparkContext, SparkConf
import os

conf = SparkConf().setAppName('pyspark_minio').setMaster('local[*]')
sc=SparkContext(conf=conf)
spark=SparkSession(sc)

accessKeyId = os.getenv('ACCESS_KEY')
secretAccessKey = os.getenv('SECRET_KEY')

## Create Connection
client = Minio(
    "ec2-65-0-177-178.ap-south-1.compute.amazonaws.com:9000",
    access_key=accessKeyId,
    secret_key=secretAccessKey,
    secure=False
)

## Get Data
output_file = "store_sales_processed.parquet"

result = client.fget_object(
    "source", "trial/covid.csv.gz", "./data/covid.csv.gz",
)

## Load Data
df=spark.read.option('header', 'true').option("inferSchema", "true").csv('./data/covid.csv.gz')

print(df.printSchema())
df1 = df.groupBy("SEX").avg("AGE")
df.registerTempTable("covid")
spark.sql("show tables").show()
df1 = spark.sql("select * from covid")
df2 = spark.sql("""select AGE, avg(`DIABETES`) as avg_DIABETES, avg(`HIPERTENSION`) as avg_HIPERTENSION from covid group by(`AGE`)""")
df3 = spark.sql("""select SEX, count(distinct `ASTHMA`) as count_ASTHMA, avg(`INTUBED`) as avg_INTUBED, avg(`CLASIFFICATION_FINAL`) as avg_CLASIFFICATION_FINAL from covid group by(`SEX`)""")

df1.repartition(1).write.format("parquet").mode("overwrite").save("./data/output1.parquet")
df2.repartition(1).write.format("parquet").mode("overwrite").save("./data/output2.parquet")
df3.repartition(1).write.format("parquet").mode("overwrite").save("./data/output3.parquet")

output_files = ["output1.parquet","output2.parquet","output3.parquet"]

## Write Back Output
for output_file in output_files:
    for file in os.listdir("./data/"+ output_file):
        if(".parquet" in file and ".crc" not in file):
            result = client.fput_object(
                "processed", output_file, "./data/"+ output_file + "/" + file,
            )