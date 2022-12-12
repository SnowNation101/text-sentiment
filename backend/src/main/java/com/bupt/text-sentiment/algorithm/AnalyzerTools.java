import java.io.IOException;
import java.io.StringReader;
import java.util.ArrayList;

import org.lionsoul.jcseg.ISegment;
import org.lionsoul.jcseg.IWord;
import org.lionsoul.jcseg.dic.ADictionary;
import org.lionsoul.jcseg.dic.DictionaryFactory;
import org.lionsoul.jcseg.segmenter.SegmenterConfig;


public class AnalyzerTools {
  public static String[] analyze(String str) throws IOException {
    //创建SegmenterConfig分词配置实例，自动查找加载jcseg.properties配置项来初始化
    SegmenterConfig config = new SegmenterConfig(true);

    //创建默认单例词库实现，并且按照config配置加载词库
    ADictionary dic = DictionaryFactory.createSingletonDictionary(config);

    //依据给定的ADictionary和SegmenterConfig来创建ISegment
    //为了Api往后兼容，建议使用SegmentFactory来创建ISegment对象
    ISegment seg = ISegment.NLP.factory.create(config, dic);

    if(str != null) {
      str = str.replaceAll("\\pP", "");

      //设置要被分词的文本
      seg.reset(new StringReader(str));

      //获取分词结果
      IWord word = null;
      ArrayList<String> list = new ArrayList<>();
      while ((word = seg.next()) != null) {
        list.add(word.getValue());
      }
      String[] ret = new String[list.size()];
      ret = list.toArray(ret);
      return ret;
    }
    return new String[]{""};
  }
}