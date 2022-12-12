package com.BUPT.TextSentiment;

import com.BUPT.TextSentiment.algorithm.TextMood;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

import java.io.IOException;

@SpringBootTest
class TextSentimentApplicationTests {

	@Test
	void contextLoads() throws IOException {
		TextMood.train();
	}

}
