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

package com.BUPT.TextSentiment.service;

import com.BUPT.TextSentiment.domain.Tmp;
import com.BUPT.TextSentiment.repository.TmpRepo;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class TmpService {
  private final TmpRepo tmpRepo;

  @Autowired
  public TmpService(TmpRepo tmpRepo) {
    this.tmpRepo = tmpRepo;
  }

  public void saveTmp(Tmp tmp) {
    tmpRepo.save(tmp);
  }

  public Float getResult() {
    return tmpRepo.findAll().get(0).getValue();
  }
}
