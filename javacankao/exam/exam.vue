<template>
  <div class="content content-bgcolor papermain">
      <div class="container exam-container">
          <div class="row">
              <div class="col-xs-12 title-content-style workontop" style="display: flex;flex-direction: row;
                  align-items: center;
                  justify-content: space-between;">
                  <div class="col-xs-10" style="width: 50%;margin-left: 20px;">
                      <div class="worktitle">{{exampaperName}}</div>
                      <p class="score">
                          Total {{dataList.length}} questions, Total Score:
                          <span class="jobscore">{{exampaperMyscore}}</span> points
                      </p>
                  </div>
                  <div class="col-xs-2 stunews-right" style="width: 50%;text-align: right;margin-right: 20px;">
                      Exam Countdown
                      <span>{{SecondToDate}}</span>
                  </div>
              </div>
          </div>

          <div class="exam-layout">
              <div class="col-xs-9 student-config-left padding-right">
                  <div class="left-content padd topicwrap">
                      <div v-for="(item, index) in dataList" :key="item.examquestionId" class="question question-radio" :data-question-id="item.examquestionId">
                          <div class="question-cont">
                              <div class="question-cont-left">
                                  <div class="question-number">{{index+1}}</div>
                                  <div class="question-points">{{item.exampapertopicNumber}} points</div>
                                  <div class="question-type">{{item.examquestionValue}}</div>
                              </div>
                              <div class="question-cont-right">
                                  <div class="question-text">
                                      <table class="blank-title">
                                          <tbody>
                                              <tr>
                                                  <td class="qestitle" style="width:96%">
                                                      {{item.examquestionName}}
                                                  </td>
                                              </tr>
                                          </tbody>
                                      </table>
                                      
                                      <div v-if="item.examquestionTypes === 1" class="question-options">
                                          <el-radio-group v-model="answersMap[item.examquestionId]" @change="selectQuestions(item.examquestionId, $event)">
                                              <el-radio :label="io.code" v-for="(io, optIndex) in item.examquestionOptions" :key="io.code" class="block-option">
                                                  <span class="option-label">{{ String.fromCharCode(65 + optIndex) }}.</span>
                                                  <span class="qesitem">{{ io.text }}</span>
                                              </el-radio>
                                          </el-radio-group>
                                      </div>
                                      
                                      <div v-if="item.examquestionTypes === 2" class="question-options">
                                          <el-checkbox-group v-model="answersArrayMap[item.examquestionId]" @change="selectMultipleQuestions(item.examquestionId, $event)">
                                              <el-checkbox :label="io.code" v-for="(io, optIndex) in item.examquestionOptions" :key="io.code" class="block-option">
                                                  <span class="option-label">{{ String.fromCharCode(65 + optIndex) }}.</span>
                                                  <span class="qesitem">{{ io.text }}</span>
                                              </el-checkbox>
                                          </el-checkbox-group>
                                      </div>
                                      
                                      <div v-if="item.examquestionTypes === 3" class="question-options">
                                          <el-radio-group v-model="answersMap[item.examquestionId]" @change="selectQuestions(item.examquestionId, $event)">
                                              <el-radio label="true" class="block-option">
                                                  <span class="qesitem">True</span>
                                              </el-radio>
                                              <el-radio label="false" class="block-option">
                                                  <span class="qesitem">False</span>
                                              </el-radio>
                                          </el-radio-group>
                                      </div>
                                      
                                      <el-input v-if="item.examquestionTypes === 4" type="textarea" :rows="4" v-model="answersMap[item.examquestionId]" @change="selectQuestions(item.examquestionId, $event)"></el-input>
                                  </div>
                              </div>
                          </div>
                      </div>
                  </div>
              </div>
              <div id="dong" class="col-xs-3 student-config-center content-style">
                  <div class="resultshow">
                      <!-- Camera Display -->
                      <div class="camera-container">
                          <div class="camera-title">Exam Monitoring</div>
                          <div class="camera-wrapper">
                              <video v-if="cameraAvailable" ref="cameraVideo" autoplay muted playsinline class="camera-video"></video>
                              <div v-else class="camera-placeholder">
                                  <i class="el-icon-video-camera"></i>
                                  <span>Monitoring Active</span>
                              </div>
                          </div>
                      </div>
                      <div id="answerguide" class="chioce-btn answerguide">
                          <dl class="question-result-item clearfix">
                              <dt class="question-resul-title">Exam Questions</dt>
                              <dd class="question-resul-tab">
                                  <a @click="goTo(item.examquestionId)" v-for="(item, index) in dataList" :key="index"
                                     :class="{'done': isAnswered(item.examquestionId), 'current': currentQuestionId === item.examquestionId}">
                                      <span>{{index+1}}</span>
                                  </a>
                              </dd>
                          </dl>
                      </div>
                      <ul class="question-result-explain">
                          <li><i class="icon-explain donei"></i>Answered</li>
                          <li><i class="icon-explain undo"></i>Unanswered</li>
                          <li><i class="icon-explain currenti"></i>Current</li>
                      </ul>
                      <div class="right-bottom">
                          <el-button type="primary" class="hm_btn_orange marginr20 submitwrok" @click="submitQuestions">Submit Exam</el-button>
                      </div>
                  </div>
              </div>
          </div>
      </div>
      
      <div class="blank-container"></div>
      
      <!-- Warning Popup -->
      <el-dialog
          title="High Risk Warning"
          :visible.sync="warningVisible"
          width="400px"
          :close-on-click-modal="false"
          :close-on-press-escape="false"
          :show-close="false"
          center>
          <div class="warning-content">
              <i class="el-icon-warning warning-icon"></i>
              <p class="warning-message">{{ warningMessage }}</p>
          </div>
          <span slot="footer" class="dialog-footer">
              <el-button type="primary" @click="closeWarning">I Understand</el-button>
          </span>
      </el-dialog>
  </div>
</template>

<script>
export default {
  data() {
      return {
          dataList: [],
          inter: null,
          count: 0,
          answerList: [],
          exampaperName: null,
          exampaperMyscore: null,
          student: {},
          currentQuestionId: null,
          answersMap: {},
          answersArrayMap: {},
          // Camera monitoring
          cameraStream: null,
          cameraAvailable: false,
          // Idle detection
          idleCheckInterval: null,
          lastActivityTime: null,
          idleThreshold: 30000,
          // Warning popup
          warningVisible: false,
          warningMessage: '',
          warningPaused: false
      };
  },
  computed: {
      SecondToDate() {
          let time = this.count;
          if (time !== null && time !== "") {
              if (time > 60 && time < 60 * 60) {
                  time =
                      parseInt(time / 60.0) +
                      " minutes " +
                      parseInt((parseFloat(time / 60.0) - parseInt(time / 60.0)) * 60) +
                      " seconds";
              } else if (time >= 60 * 60 && time < 60 * 60 * 24) {
                  time =
                      parseInt(time / 3600.0) +
                      " hours " +
                      parseInt(
                          (parseFloat(time / 3600.0) - parseInt(time / 3600.0)) * 60
                      ) +
                      " minutes " +
                      parseInt(
                          (parseFloat(
                              (parseFloat(time / 3600.0) - parseInt(time / 3600.0)) * 60
                          ) -
                          parseInt(
                              (parseFloat(time / 3600.0) - parseInt(time / 3600.0)) * 60
                          )) *
                          60
                      ) +
                      " seconds";
              } else if (time >= 60 * 60 * 24) {
                  time =
                      parseInt(time / 3600.0 / 24) +
                      " days " +
                      parseInt(
                          (parseFloat(time / 3600.0 / 24) - parseInt(time / 3600.0 / 24)) *
                          24
                      ) +
                      " hours " +
                      parseInt(
                          (parseFloat(time / 3600.0) - parseInt(time / 3600.0)) * 60
                      ) +
                      " minutes " +
                      parseInt(
                          (parseFloat(
                              (parseFloat(time / 3600.0) - parseInt(time / 3600.0)) * 60
                          ) -
                          parseInt(
                              (parseFloat(time / 3600.0) - parseInt(time / 3600.0)) * 60
                          )) *
                          60
                      ) +
                      " seconds";
              } else {
                  time = parseInt(time) + " seconds";
              }
          }
          return time;
      }
  },
  created() {
      this.init();
      this.initCamera();
      this.initIdleDetection();
      this.initFocusDetection();
  },
  beforeDestroy() {
      if (this.inter) {
          clearInterval(this.inter);
      }
      this.stopCamera();
      this.cleanupIdleDetection();
      this.cleanupFocusDetection();
  },
  methods: {
      // Camera methods
      async initCamera() {
          try {
              if (navigator.mediaDevices && navigator.mediaDevices.getUserMedia) {
                  this.cameraStream = await navigator.mediaDevices.getUserMedia({ 
                      video: { width: 320, height: 240 }, 
                      audio: false 
                  });
                  this.cameraAvailable = true;
                  this.$nextTick(() => {
                      if (this.$refs.cameraVideo) {
                          this.$refs.cameraVideo.srcObject = this.cameraStream;
                      }
                  });
              } else {
                  console.warn('getUserMedia not supported');
                  this.cameraAvailable = false;
              }
          } catch (error) {
              console.warn('Camera access denied or unavailable:', error);
              this.cameraAvailable = false;
          }
      },
      stopCamera() {
          if (this.cameraStream) {
              this.cameraStream.getTracks().forEach(track => track.stop());
              this.cameraStream = null;
          }
      },
      // Idle detection methods
      initIdleDetection() {
          this.lastActivityTime = Date.now();
          // Add event listeners for user activity
          document.addEventListener('mousemove', this.resetIdleTimer);
          document.addEventListener('mousedown', this.resetIdleTimer);
          document.addEventListener('keydown', this.resetIdleTimer);
          document.addEventListener('scroll', this.resetIdleTimer);
          // Start checking idle status every second
          this.idleCheckInterval = setInterval(() => {
              this.checkIdleStatus();
          }, 1000);
      },
      resetIdleTimer() {
          this.lastActivityTime = Date.now();
      },
      checkIdleStatus() {
          // Only check if exam is in progress and warning is not shown
          if (this.count <= 0 || this.warningPaused || this.warningVisible) {
              return;
          }
          const idleTime = Date.now() - this.lastActivityTime;
          if (idleTime >= this.idleThreshold) {
              this.showWarning('You have been inactive for more than 30 seconds. Please continue your exam.');
          }
      },
      cleanupIdleDetection() {
          document.removeEventListener('mousemove', this.resetIdleTimer);
          document.removeEventListener('mousedown', this.resetIdleTimer);
          document.removeEventListener('keydown', this.resetIdleTimer);
          document.removeEventListener('scroll', this.resetIdleTimer);
          if (this.idleCheckInterval) {
              clearInterval(this.idleCheckInterval);
              this.idleCheckInterval = null;
          }
      },
      // Focus detection methods
      initFocusDetection() {
          window.addEventListener('blur', this.handleWindowBlur);
          document.addEventListener('visibilitychange', this.handleVisibilityChange);
      },
      handleWindowBlur() {
          if (this.count > 0 && !this.warningPaused && !this.warningVisible) {
              this.showWarning('You have switched away from the exam window. Please stay focused on your exam.');
          }
      },
      handleVisibilityChange() {
          if (document.hidden && this.count > 0 && !this.warningPaused && !this.warningVisible) {
              this.showWarning('You have switched away from the exam window. Please stay focused on your exam.');
          }
      },
      cleanupFocusDetection() {
          window.removeEventListener('blur', this.handleWindowBlur);
          document.removeEventListener('visibilitychange', this.handleVisibilityChange);
      },
      // Warning popup methods
      showWarning(message) {
          this.warningMessage = message;
          this.warningVisible = true;
          this.warningPaused = true;
      },
      closeWarning() {
          this.warningVisible = false;
          this.warningPaused = false;
          this.resetIdleTimer();
      },
      goTo(id) {
          this.currentQuestionId = id;
          const element = document.querySelector(`[data-question-id="${id}"]`);
          if (element) {
              element.scrollIntoView({ behavior: 'smooth' });
          }
      },
      isAnswered(examquestionId) {
          const answerItem = this.answerList.find(item => item.examquestionId === examquestionId);
          if (!answerItem) return false;
          
          if (answerItem.examquestionTypes === 2) {
              return this.answersArrayMap[examquestionId] && this.answersArrayMap[examquestionId].length > 0;
          } else if (answerItem.examquestionTypes === 3) {
              return this.answersMap[examquestionId] === 'true' || this.answersMap[examquestionId] === 'false';
          } else if (answerItem.examquestionTypes === 4) {
              return this.answersMap[examquestionId] !== null && this.answersMap[examquestionId] !== '';
          } else {
              return this.answersMap[examquestionId] !== null && this.answersMap[examquestionId] !== '';
          }
      },
      selectQuestions(examquestionId, code) {
          this.$set(this.answersMap, examquestionId, code);
          const answerItem = this.answerList.find(item => item.examquestionId === examquestionId);
          if (answerItem) {
              answerItem.answer = code;
              this.currentQuestionId = examquestionId;
          }
      },
      selectMultipleQuestions(examquestionId, codes) {
          this.$set(this.answersArrayMap, examquestionId, codes);
          const answerItem = this.answerList.find(item => item.examquestionId === examquestionId);
          if (answerItem) {
              answerItem.answer = codes.join(',');
              this.currentQuestionId = examquestionId;
          }
      },
      init() {
          const exampaperId = this.$route.query.exampaperId;
          if (!exampaperId) {
              this.$message.error('Missing Exam Paper ID parameter');
              return;
          }

          // Get user information
          this.$http.get(`${localStorage.getItem("UserTableName")}/session`)
              .then(response => {
                  this.student = response.data.data;
                  console.log("User Info："+this.student);
              })
              .catch(error => {
                  console.error('Failed to get user information', error);
                  this.$message.error('Failed to get user information, please login again');
              });

          // Get exam paper questions
          this.$http.get(`exampapertopic/questionAcquisition?exampaperId=${exampaperId}`)
              .then(response => {
                  this.dataList = response.data.data;
                  if (this.dataList && this.dataList.length > 0) {
                      this.exampaperName = this.dataList[0].exampaperName;
                      this.exampaperMyscore = this.dataList[0].exampaperMyscore;
                      
                      if (this.dataList[0].exampaperDate) {
                          this.count = this.dataList[0].exampaperDate * 60;
                          if (this.count > 0) {
                              this.inter = setInterval(() => {
                                  this.count--;
                                  if (this.count <= 0) {
                                      clearInterval(this.inter);
                                      this.submitQuestions();
                                  }
                              }, 1000);
                          }
                      }
                      
                      // Initialize answer list and answer mapping
                      this.answerList = [];
                      this.answersMap = {};
                      this.answersArrayMap = {};
                      
                      this.dataList.forEach(item => {
                          if (item.examquestionTypes !== 4) {
                              item.examquestionOptions = JSON.parse(item.examquestionOptions);
                          }
                          
                          // Initialize answer mapping
                          if (item.examquestionTypes === 2) {
                              this.$set(this.answersArrayMap, item.examquestionId, []);
                          } else {
                              this.$set(this.answersMap, item.examquestionId, '');
                          }
                          
                          this.answerList.push({
                              examquestionId: item.examquestionId,
                              examquestionTypes: item.examquestionTypes,
                              answer: item.examquestionTypes === 2 ? [] : ''
                          });
                      });
                      
                      if (this.dataList.length > 0) {
                          this.currentQuestionId = this.dataList[0].examquestionId;
                      }
                  }
              })
              .catch(error => {
                  console.error('Failed to get exam paper questions', error);
                  this.$message.error('Failed to get exam paper questions');
              });
      },
      submitQuestions() {
          // Check if user ID exists
          if (!this.student || !this.student.id) {
              this.$message.error('User information is missing, please login again');
              return;
          };
          // Check if exam paper ID is valid
          const exampaperId = parseInt(this.$route.query.exampaperId);
          if (isNaN(exampaperId)) {
                this.$message.error('Invalid Exam Paper ID, please refresh the page');
                return;
          };

          // Verify all examquestionId in answerList are valid numbers
          const invalidQuestion = this.answerList.find(item => {
                const id = parseInt(item.examquestionId);
                return isNaN(id) || id <= 0;
            });
            
            if (invalidQuestion) {
                this.$message.error(`Invalid question ID found: ${invalidQuestion.examquestionId}`);
                return;
            };

          const notDone = [];
          this.dataList.forEach((item, index) => {
              if (!this.isAnswered(item.examquestionId)) {
                  notDone.push(index + 1);
              }
          });

          const confirmSubmit = () => {
              // Create FormData object
                const formData = new FormData();
                
                // Add basic parameters
                formData.append('yonghuId', this.student.id);
                formData.append('exampaperId', this.$route.query.exampaperId);
                
                // Serialize answerList to JSON string
                const answerListJson = JSON.stringify(this.answerList);
                formData.append('answerList', answerListJson);
                
                // Print complete submission data
                // console.log('Complete submission parameters:');
                // console.log('yonghuId:', this.student.id);
                // console.log('exampaperId:', this.$route.query.exampaperId);
                // console.log('answerList:', answerListJson);

                this.$http.post(`exampapertopic/submitQuestions`, formData, {
                    headers: {
                        'Content-Type': 'multipart/form-data'  // Let browser automatically set correct Content-Type
                    }
                })
                  .then(response => {
                      this.$message.success('Submitted successfully');
                      this.$router.back();
                  })
                  .catch(error => {
                      console.error('Failed to submit exam paper', error);
                      this.$message.error('Failed to submit exam paper');
                  });
          };

          if (this.count > 0) {
              this.$confirm(`You have '${notDone.length}' unanswered questions: ${notDone}, are you sure to submit?`, 'Prompt', {
                  confirmButtonText: 'Confirm',
                  cancelButtonText: 'Cancel',
                  type: 'warning'
              }).then(() => {
                  confirmSubmit();
              }).catch(() => {
                  // User cancelled submission
              });
          } else {
              if (notDone.length > 0) {
                  this.$alert(`You have '${notDone.length}' unanswered questions: ${notDone}; Unanswered questions will be scored 0 points!`, 'Prompt', {
                      confirmButtonText: 'Confirm',
                      callback: () => {
                          confirmSubmit();
                      }
                  });
              } else {
                  this.$alert('Time is up, the exam paper will be submitted!!!', 'Prompt', {
                      confirmButtonText: 'Confirm',
                      callback: () => {
                          confirmSubmit();
                      }
                  });
              }
          }
      }
  }
}
</script>

<style scoped>
.content-bgcolor {
  background-color: #f5f5f5;
}

.papermain {
  padding: 20px 0;
}

.exam-container {
  max-width: 1440px;
  margin: 0 auto;
  padding: 0 40px;
}

.blank-container {
  max-width: 1440px;
  margin: 0 auto;
  padding: 0 40px;
  height: 300px;
}

.workontop {
  background-color: #fff;
  padding: 15px;
  border-radius: 5px;
  margin-bottom: 20px;
}

.worktitle {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 10px;
}

.score {
  color: #666;
}

.jobscore {
  color: #ff6600;
  font-weight: bold;
}

.stunews-right {
  color: #333;
}

.exam-layout {
  display: flex;
  flex-direction: row;
}

.student-config-left {
  flex: 0 0 74%;
  max-width: 74%;
  padding-right: 15px;
}

.student-config-center {
  flex: 0 0 26%;
  max-width: 26%;
  background-color: #fff;
  padding: 15px;
  border-radius: 5px;
}

.topicwrap {
  background-color: #fff;
  padding: 15px;
  border-radius: 5px;
}

.question {
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
  position: relative;
}

.question[data-question-id] {
  scroll-margin-top: 20px;
}

.question-cont {
  display: flex;
}

.question-cont-left {
  display: flex;
  flex-direction: column;
  width: 60px;
  margin-right: 15px;
}

.question-number {
  display: inline-block;
  width: 24px;
  height: 24px;
  line-height: 24px;
  text-align: center;
  background-color: #f5f5f5;
  border-radius: 50%;
  margin-bottom: 8px;
}

.question-points, .question-type {
  color: #999;
  font-size: 12px;
  margin-bottom: 4px;
}

.question-text {
  margin-top: 0;
}

.blank-title {
  width: 100%;
}

.qestitle {
  font-size: 14px;
  line-height: 1.5;
}

.question-options {
  margin-top: 10px;
}

.block-option {
  display: block;
  margin-bottom: 10px;
}

.option-label {
  display: inline-block;
  width: 24px;
  text-align: center;
  margin-right: 5px;
}

/* True or False不显示选项编号 (Keep Chinese comment as it's style-related) */
.question-options[class*="examquestionTypes-3"] .option-label {
  display: none;
}

.chioce-btn {
  margin-bottom: 20px;
}

.question-result-item {
  margin: 0;
  padding: 0;
}

.question-resul-title {
  font-weight: bold;
  margin-bottom: 10px;
}

.question-resul-tab {
  display: flex;
  flex-wrap: wrap;
}

.question-resul-tab a {
  display: block;
  width: 24px;
  height: 24px;
  line-height: 24px;
  text-align: center;
  margin: 0 5px 5px 0;
  background-color: #f5f5f5;
  border-radius: 3px;
  color: #333;
  text-decoration: none;
}

.question-resul-tab a.done {
  background-color: #5cb85c;
  color: #fff;
}

.question-resul-tab a.current {
  background-color: #1890ff;
  color: #fff;
}

.question-result-explain {
  list-style: none;
  padding: 0;
  margin: 20px 0;
  display: flex;
}

.question-result-explain li {
  margin-right: 20px;
  font-size: 12px;
  color: #666;
}

.icon-explain {
  display: inline-block;
  width: 12px;
  height: 12px;
  margin-right: 5px;
  border-radius: 3px;
}

.donei {
  background-color: #5cb85c;
}

.undo {
  background-color: #f5f5f5;
  border: 1px solid #ddd;
}

.currenti {
  background-color: #1890ff;
}

.right-bottom {
  margin-top: 20px;
  text-align: center;
}

.hm_btn_orange {
  background-color: #ff6600;
  color: #fff;
  border: none;
  padding: 8px 20px;
  border-radius: 3px;
  cursor: pointer;
}

.hm_btn_orange:hover {
  background-color: #e65c00;
}

.marginr20 {
  margin-right: 20px;
}

.submitwrok {
  width: 100%;
}

.blue {
  color: #1890ff;
}

#dong {
  position: sticky;
  top: 20px;
  height: fit-content;
}

@media (max-width: 1024px) {
  .exam-container {
      padding: 0 20px;
  }
  
  .student-config-left {
      flex: 0 0 70%;
      max-width: 70%;
  }
  
  .student-config-center {
      flex: 0 0 30%;
      max-width: 30%;
  }
}

@media (max-width: 768px) {
  .exam-layout {
      flex-direction: column;
  }
  
  .student-config-left, .student-config-center {
      flex: 0 0 100%;
      max-width: 100%;
  }
  
  .student-config-left {
      padding-right: 0;
      margin-bottom: 20px;
  }
  
  #dong {
      position: static;
  }
}

/* Camera Display Styles */
.camera-container {
  margin-bottom: 15px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.camera-title {
  font-weight: bold;
  margin-bottom: 10px;
  font-size: 14px;
}

.camera-wrapper {
  width: 100%;
  height: 150px;
  background-color: #1a1a1a;
  border-radius: 5px;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
}

.camera-video {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.camera-placeholder {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #5cb85c;
  font-size: 12px;
}

.camera-placeholder i {
  font-size: 32px;
  margin-bottom: 8px;
}

/* Warning Popup Styles */
.warning-content {
  text-align: center;
  padding: 20px 0;
}

.warning-icon {
  font-size: 48px;
  color: #E6A23C;
  margin-bottom: 15px;
}

.warning-message {
  font-size: 14px;
  color: #606266;
  line-height: 1.6;
}
</style>