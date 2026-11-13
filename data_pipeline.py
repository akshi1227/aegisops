from pyspark.sql import SparkSession
from pyspark.sql.functions import col, when

def run_compliance_pipeline(file_path: str):
    spark = SparkSession.builder.appName("AegisOpsMedicalCompliance").getOrCreate()
    df = spark.read.json(file_path)
    cleaned_df = df.na.drop(subset=["timestamp", "status"])
    flagged_df = cleaned_df.withColumn(
        "compliance_status",
        when((col("status") == "ERROR") | (col("message").contains("PHI_BREACH")), "VIOLATION").otherwise("COMPLIANT")
    )
    flagged_df.write.mode("overwrite").parquet("output/validated_medical_logs.parquet")
    return flagged_df.count()