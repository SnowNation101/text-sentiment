
import org.apache.spark.api.java.function.MapFunction;
import org.apache.spark.internal.config.R;
import org.apache.spark.ml.Pipeline;
import org.apache.spark.ml.PipelineModel;
import org.apache.spark.ml.PipelineStage;
import org.apache.spark.ml.classification.NaiveBayes;
import org.apache.spark.ml.classification.NaiveBayesModel;
import org.apache.spark.ml.evaluation.MulticlassClassificationEvaluator;
import org.apache.spark.ml.feature.HashingTF;
import org.apache.spark.ml.feature.IDF;
import org.apache.spark.ml.feature.IDFModel;
import org.apache.spark.sql.*;
import org.apache.spark.sql.catalyst.encoders.RowEncoder;
import org.apache.spark.sql.types.*;

import java.io.IOException;
import java.util.ArrayList;
import java.util.List;

public class TextMood {
    public static void main(String[] args) throws IOException {
        SparkSession spark = SparkSession.builder()
                .appName("Iris Species")
                .master("local[4]")
                .getOrCreate();

        Dataset<Row> origin = spark.read()
            .option("inferSchema", "true")
            .option("header","true")
            .csv("./src/main/resources/data.csv")
            .toDF("label", "features");

        StructType customStructType = new StructType();
        customStructType = customStructType.add("label", DataTypes.IntegerType, false);
        customStructType = customStructType.add("words", ArrayType.apply(DataTypes.StringType), false);

        Dataset<Row> data = origin.map((MapFunction<Row, Row>) row -> {
            int i = row.getInt(0);
            String[] list = AnalyzerTools.analyze(row.getString(1));
            return RowFactory.create(i, list);
        }, RowEncoder.apply(customStructType));

        HashingTF hashingTF = new HashingTF()
            .setNumFeatures(500000)
            .setInputCol("words")
            .setOutputCol("rawFeatures");

        IDF idf = new IDF()
            .setInputCol("rawFeatures")
            .setOutputCol("features");

        // Split the data into training and test sets (30% held out for testing).
        Dataset<Row>[] splits = data.randomSplit(new double[]{0.7, 0.3});
        Dataset<Row> training = splits[0];
        Dataset<Row> test = splits[1];

        // create the trainer and set its parameters
        NaiveBayes nb = new NaiveBayes()
            .setLabelCol("label")
            .setFeaturesCol("features");

        Pipeline pipeline = new Pipeline()
            .setStages(new PipelineStage[] {hashingTF, idf, nb});

        // Fit the pipeline to training documents
        PipelineModel model = pipeline.fit(training);

        // Make predictions on test documents
        Dataset<Row> predictions = model.transform(test);
        predictions.show();

//        predictions.write().csv("./test");

        model.write().overwrite().save("./model");

//        StructType structType = new StructType();
//        structType = structType.add("words", ArrayType.apply(DataTypes.StringType), false);
//
//        List<Row> nums = new ArrayList<>();
//        nums.add(RowFactory.create(AnalyzerTools.analyze("我觉得这个太糟糕了！")));
//        Dataset<Row> pre = model.transform(spark.createDataFrame(nums, structType));
//        pre.show();


        MulticlassClassificationEvaluator evaluator = new MulticlassClassificationEvaluator()
            .setLabelCol("label")
            .setPredictionCol("prediction")
            .setMetricName("accuracy");
        double accuracy = evaluator.evaluate(predictions);
        System.out.println("Test set accuracy = " + accuracy);

        spark.close();
    }
}