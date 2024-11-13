from pyspark.sql.functions import *
from pyspark.sql import *

def load_data():
    # Loads the data
    # ---------------------change the s3 bucket here----------------
    input_bucket = "s3://ece4150-group-project"
    
    # Load Trip Data
    # ---------------------change the csv file here----------------
    trip_path = '/yellow_tripdata*'
    trips = spark.read.csv(input_bucket + trip_path, header=True, inferSchema=True)
    print("Trip Count: ",trips.count()) # Prints # of trips (# of records, as each record is one trip)
    
    # Load Lookup Data
    # ---------------------change the csv file here----------------
    lookup_path = '/taxi*'
    lookup = spark.read.csv(input_bucket + lookup_path, header=True, inferSchema=True)
    
    return trips, lookup

def main(bucket1, bucket2):
    trips, lookup = load_data()
    trips = long_trips(trips)
    top_drop = topDrop_trips(trips, lookup)
    top_drop.write.csv(bucket1, mode="overwrite")
    top_drop.show()

    # just select "manhattan"
    mtrips = manhattan_trips(trips, lookup)
    wp = weighted_profit(trips, mtrips)
    final = final_output(wp, lookup)
    
    # Outputs the results
    final.show()
    
    # Writes out as a CSV
    final.write.csv(bucket2, mode="overwrite")

def long_trips(trips):
    # Returns a Dataframe (trips) with Schema the same as :trips:
    df = trips.filter(col("trip_distance")>=2)
    return df

def topDrop_trips(trips, lookup):
    # for all drop location, try to find top100 locations, and find the Borough where is most dropLocations
    # Returns a Dataframe (mtrips) with Schema: DOLocationID, pcount
    df_mtrip_join = trips.join(lookup, col("DOLocationID")==col("LocationID"))
    df_mtrip_join = df_mtrip_join.withColumn("Borough_trips", col("Borough"))
    df_mtrip_group = df_mtrip_join.groupBy("DOLocationID").agg(sum("passenger_count").alias("pcount"), first("Borough_trips").alias("Borough"))
    df_mtrip = df_mtrip_group.orderBy(desc("pcount")).limit(100)
    return df_mtrip

def manhattan_trips(trips, lookup):
    # from topDrop_trips, we will find that Manhattan is the most popular drop Borough
    # Here, we try to find the top30 drop locations in Manhattan
    # Returns a Dataframe (mtrips) with Schema: DOLocationID, pcount
    df_mtrip_join = trips.join(lookup, col("DOLocationID")==col("LocationID")).where(col("borough")=="Manhattan")
    df_mtrip_group = df_mtrip_join.groupBy("DOLocationID").agg(sum("passenger_count").alias("pcount"))
    df_mtrip = df_mtrip_group.orderBy(desc("pcount")).limit(30)
    return df_mtrip

def weighted_profit(trips, mtrips): 
    # Returns a Dataframe (wp) with Schema: PULocationID, weighted_profit
    
    # get the avg_total_amount,and pickup_loction_count
    df_total_amount = trips.groupBy("PULocationID").agg(avg("total_amount").alias("avg_total_amount"),count("*").alias("PLoction_count"))
    
    # get the count of trips whose droplocations are 30 popular loction
    mtrips = mtrips.withColumnRenamed("DOLocationID", "DOLocationID_mtrips")
    df_top_drop_join = trips.join(mtrips, trips.DOLocationID == mtrips.DOLocationID_mtrips)
    df_top_drop = df_top_drop_join.groupBy("PULocationID", "DOLocationID").agg(count("*").alias("topDrop_count"))
    df_top_drop = df_top_drop.withColumnRenamed("PULocationID", "PULocationID_mtrips")
    
    # join
    df_top_counts = df_total_amount.join(df_top_drop, df_total_amount["PULocationID"] == df_top_drop["PULocationID_mtrips"])
    
    # get the weighted profits
    df_weighted = df_top_counts.withColumn("weighted_profit_one", (col("topDrop_count")/col("PLoction_count"))*col("avg_total_amount"))
    df_weighted = df_weighted.groupBy("PULocationID").agg(sum("weighted_profit_one").alias("weighted_profit"))
    df_weighted = df_weighted.select("PULocationID", "weighted_profit")

    return df_weighted

def final_output(wp, lookup): 
    # Returns a Dataframe (final) with Schema: Zone, Borough, weighted_profit
    df_join = wp.join(lookup, wp["PULocationID"]==lookup["LocationID"])
    df_final = df_join.select("LocationID","Zone","Borough","weighted_profit").orderBy(desc("weighted_profit"))
    return df_final

# -----------------------change the output s3 bucket path --------------------------
path1 = "s3://cse6242-zzhang3180/output-top100"
path2 = "s3://cse6242-zzhang3180/output-large"
main(path1, path2)
