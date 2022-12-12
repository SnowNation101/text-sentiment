/*
 * Copyright (c) 2022. David "SnowNation" Zhang
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 * http://www.apache.org/licenses/LICENSE-2.0
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing permissions and limitations under
 * the License.
 */

package com.BUPT.TextSentiment.controller;

import com.BUPT.TextSentiment.domain.AlgorithmTwo;
import com.BUPT.TextSentiment.domain.Tmp;
import com.BUPT.TextSentiment.repository.TmpRepo;
import com.BUPT.TextSentiment.service.AlgorithmTwoService;
import com.BUPT.TextSentiment.service.TmpService;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.exec.CommandLine;
import org.apache.commons.exec.DefaultExecutor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.io.IOException;
import java.util.List;

@Slf4j
@RestController
@CrossOrigin("*")
@RequestMapping("/api/algo-2")
public class AlgorithmTwoController {

  private final AlgorithmTwoService algorithmTwoService;
  private final TmpService tmpService;
  @Autowired
  public AlgorithmTwoController(AlgorithmTwoService algorithmTwoService, TmpRepo tmpRepo, TmpService tmpService) {
    this.algorithmTwoService = algorithmTwoService;
    this.tmpService = tmpService;
  }

  @GetMapping("/get-all")
  public List<AlgorithmTwo> getComments() {
    return algorithmTwoService.getAllComments();
  }

  @PostMapping("/run")
  public Void runAlgorithm(@RequestParam String str, @RequestParam Integer language) throws IOException {
    Tmp tmp = new Tmp();
    tmp.setId(1);
    tmp.setText(str);
    tmp.setLanguage(0);
    tmpService.saveTmp(tmp);
    runPythonScript();
    return null;
  }

  @GetMapping("/get")
  public Float get() {
    return tmpService.getResult();
  }

  Void runPythonScript() throws IOException {
    String line = "D:/ProgramData/Anaconda3/envs/lightning/python.exe  ./PyScript/two/main_withsql.py";
    CommandLine cmdLine = CommandLine.parse(line);
    DefaultExecutor executor = new DefaultExecutor();
    executor.execute(cmdLine);
    return null;
  }
}
