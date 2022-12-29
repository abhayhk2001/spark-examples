import findspark
findspark.init()
import pyspark
from pyspark.sql import SparkSession, SQLContext
from pyspark import SparkContext, SparkConf
import os

conf = SparkConf().set('spark.executor.extraJavaOptions','-Dcom.amazonaws.services.s3.enableV4=true').set('spark.driver.extraJavaOptions','-Dcom.amazonaws.services.s3.enableV4=true').set('spark.jars.packages', 'com.amazonaws:aws-java-sdk:1.7.4,org.apache.hadoop:hadoop-aws:2.7.3').setAppName('pyspark_aws').setMaster('local[*]')
sc=SparkContext(conf=conf)
sc.setSystemProperty('com.amazonaws.services.s3.enableV4', 'true')

accessKeyId = os.getenv('ACCESS_KEY')
secretAccessKey = os.getenv('SECRET_KEY')

hadoopConf = sc._jsc.hadoopConfiguration()
hadoopConf.set('fs.s3a.access.key', accessKeyId)
hadoopConf.set('fs.s3a.secret.key', secretAccessKey)
hadoopConf.set('fs.s3a.endpoint', 's3-ap-south-1.amazonaws.com')
hadoopConf.set('fs.s3a.impl', 'org.apache.hadoop.fs.s3a.S3AFileSystem')

spark=SparkSession(sc)
sqlContext = SQLContext(sc)
df=spark.read.option('header', 'true').option("inferSchema","true").csv('s3a://bpcl-spark/ss1.csv.gz')
print(df.show())
df.groupBy("ss_ext_discount_amt").count().show(10)
df.write.format("parquet").mode("overwrite").save("temp.parquet")

df.registerTempTable("covid")
tables = spark.sql("show tables").show()

sqlContext.sql("""select distinct(`ss_ext_discount_amt`), sum(`ss_quantity`) as cnt from covid group by `ss_ext_discount_amt` order by cnt desc""").show()
sqlContext.sql("select * from covid").show()