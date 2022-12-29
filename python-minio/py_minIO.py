def run_data_process():
	from minio import Minio
	import pandas as pd
	import os

	accessKeyId = os.getenv('ACCESS_KEY')
	secretAccessKey = os.getenv('SECRET_KEY')
	
	## Create Connection
	client = Minio(
		"ec2-65-0-177-178.ap-south-1.compute.amazonaws.com:9000",
		access_key=accessKeyId,
		secret_key=secretAccessKey,
		secure=False
	)

	# Collect Files
	files = []
	output_file = "store_sales_processed.parquet"

	for i in client.list_objects('source', recursive=True):
		if("tpcds" in i.object_name):
			files.append("./data/"+i.object_name[6:])
			result = client.fget_object(
			    "source", i.object_name, "./data/"+i.object_name[6:],
			)

	## Load Data		
	df = None
	flag = True

	for file in files:
		df1 = pd.read_csv(file)
		if(flag):
			df = df1
			flag = False
		else:
			df = pd.concat([df, df1], ignore_index=True)

	## Processing
	df = df.dropna().reset_index(drop=True)
	print(df.shape)

	df = (df.groupby(['ss_hdemo_sk']).mean().loc[:,["ss_promo_sk","ss_sales_price", "ss_ext_sales_price", "ss_ext_tax","ss_net_paid", "ss_net_paid_inc_tax" ]])

	## Generate Output
	df.to_parquet("./" + output_file)

	## Write Back Output
	result = client.fput_object(
		"processed", output_file, "./"+ output_file,
	)

	os.remove("./" + output_file)
	os.rmdir("./data")
