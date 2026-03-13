<template>
    <div class="content content-bgcolor papermain">
      <!-- Loading State -->
      <div v-if="loading" class="loading-state">
        <el-loading-spinner></el-loading-spinner>
        <p>Loading...</p>
      </div>
      
      <!-- Error State -->
      <div v-if="errorMsg && !loading" class="error-state">
        <i class="el-icon-error"></i>
        <p>{{ errorMsg }}</p>
        <el-button type="primary" @click="handleBack">Back</el-button>
      </div>
      
      <!-- Content Area - Display only when loaded and no errors -->
      <div v-if="!loading && !errorMsg" class="container exam-container">
        <!-- Title Area -->
        <div class="row">
          <div class="col-xs-12 title-content-style workontop" style="display: flex;flex-direction: row;
              align-items: center;
              justify-content: space-between;">
            <div class="col-xs-10" style="width: 50%;margin-left: 20px;">
              <div class="worktitle">{{headData.exampaperName}}</div>
              <p class="score">
                Total {{dataList.length}} questions, Total Score:
                <span class="jobscore">{{headData.exampaperMyscore}}</span> points
              </p>
            </div>
            <div class="col-xs-2 stunews-right" style="width: 50%;text-align: right;margin-right: 20px;">
              <span> Score：{{headData.totalScore}} points</span>
            </div>
          </div>
        </div>
  
        <!-- Content Area -->
        <div class="exam-layout">
          <!-- Left Question Area -->
          <div class="col-xs-9 student-config-left padding-right">
            <div class="left-content padd topicwrap">
              <!-- Loop to display questions -->
              <div v-for="(item, index) in dataList" :key="item.id" class="question question-radio" :data-question-id="item.id">
                <div class="question-cont">
                  <div class="question-cont-left">
                    <span :id="'id'+item.id" class="question-num">{{index+1}}</span>
                    <span class="question-score">{{item.examquestionValue}}</span>
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
                      
                      <!-- Multiple Choice Options -->
                      <ul class="question-options" v-if="item.examquestionTypes != 4">
                        <li :class="getOptionClass(item, io)"
                            v-for="(io) in item.examquestionOptions" :key="io.code">
                          <i class="options">{{ io.code }}</i>
                          <span class="qesitem">{{ io.text }}</span>
                        </li>
                      </ul>
                      
                      <!-- Fill-in-the-blank -->
                      <ul v-else class="question-options">
                        <li>
                          <textarea readonly v-model="item.examredetailsMyanswer"
                                    style="width: 720px;height: 150px;resize:none"></textarea>
                        </li>
                      </ul>
                    </div>
  
                    <!-- Answer Area -->
                    <div class="Answer-Box">
                      <div class="My-Answer" v-if="item.examredetailsMyanswer">
                        <h3 style="margin: 7px 0;font-size: 15px;">My Answer:
                          <span :class="verificationAnswer(item.examquestionAnswer, item.examredetailsMyanswer, item.examquestionTypes) ? 'answer-correct' : 'answer-wrong'">
                            {{ formatAnswer(item) }}
                          </span>
                        </h3>
                      </div>
                      <div class="Teacher-Answer">
                        <h3 style="margin: 7px 0;font-size: 15px;">Correct Answer:
                          <span class="answer-right-special">{{ formatAnswer(item, true) }}</span>
                        </h3>
                      </div>
                    </div>
  
                    <!-- Analysis Area -->
                    <div class="Analysis-Box" v-if="item.examquestionAnalysis">
                      <button class="release">Analysis:</button>
                      <div class="Analysis-Content">{{ item.examquestionAnalysis }}</div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          
          <!-- Right Navigation Area -->
          <div id="dong" class="col-xs-3 student-config-center content-style">
            <div class="resultshow">
              <div id="answerguide" class="chioce-btn answerguide">
                <dl class="question-result-item clearfix">
                  <dt class="question-resul-title">Paper Questions</dt>
                  <dd class="question-resul-tab">
                    <a @click="goTo(item.id)" v-for="(item, index) in dataList" :key="index"
                       :class="{'done': verificationAnswer(item.examquestionAnswer, item.examredetailsMyanswer, item.examquestionTypes), 
                               'mark': !verificationAnswer(item.examquestionAnswer, item.examredetailsMyanswer, item.examquestionTypes)}">
                      <span>{{index+1}}</span>
                    </a>
                  </dd>
                </dl>
              </div>
              
              <!-- Legend Explanation -->
              <ul class="question-result-explain">
                <li><i class="icon-explain donei"></i>Correct</li>
                <li><i class="icon-explain marki"></i>Incorrect</li>
              </ul>
              
              <!-- Back Button -->
              <div class="right-bottom">
                <el-button type="primary" class="hm_btn_orange marginr20 submitwrok"
                           @click="handleBack">Back</el-button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ExamResult', // Ensure component has a name for route recognition
    data() {
      return {
        dataList: [],
        headData: {},
        loading: false,
        errorMsg: ''
      };
    },
    created() {
      // Check route parameters when component is created
      this.checkRouteParams();
    },
    methods: {
      // Check if route parameters are complete
      checkRouteParams() {
        // Get required data from route parameters
        const routeParams = this.$route.query;
        
        // Verify required parameters
        const requiredParams = ['id', 'examrecordUuidNumber', 'yonghuId'];
        const missingParams = requiredParams.filter(param => !routeParams[param]);
        
        if (missingParams.length > 0) {
          this.errorMsg = `Missing required parameters: ${missingParams.join(', ')}`;
          return false;
        }
        
        // Parameters are complete, load exam results
        this.loadExamResult(routeParams);
        return true;
      },
      
      // Jump to specified question
      goTo(id) {
        document.querySelector('#id' + id).scrollIntoView({ behavior: 'smooth' });
      },
      
      // Verify if answer is correct
      verificationAnswer(examquestionAnswer, examredetailsMyanswer, type) {
        // Handle empty values
        if (!examquestionAnswer || !examredetailsMyanswer) return false;
        
        if (type == 2) { // Multiple-choice
          return examquestionAnswer.split(",").sort().toString() === 
                 examredetailsMyanswer.split(",").sort().toString();
        } else { // Single Choice、True or False
          return examquestionAnswer === examredetailsMyanswer;
        }
      },
      
      // Format answer display
      formatAnswer(item, isCorrectAnswer = false) {
        const answer = isCorrectAnswer ? item.examquestionAnswer : item.examredetailsMyanswer;
        
        // For multiple-choice questions, convert answer codes to letters
        if (item.examquestionTypes == 2 && item.examquestionOptions && answer) {
          return answer.split(',').map(code => {
            const option = item.examquestionOptions.find(opt => opt.code === code);
            return option ? option.code : code;
          }).join(',');
        }
        
        // For True or False questions
        if (item.examquestionTypes == 3) {
          return answer === 'true' ? 'Correct' : 'Incorrect';
        }
        
        return answer || 'Not Answered';
      },
      
      // Get option style class
      getOptionClass(item, option) {
        const isCorrect = this.verificationAnswer(item.examquestionAnswer, item.examredetailsMyanswer, item.examquestionTypes);
        const userSelected = item.examredetailsMyanswer && item.examredetailsMyanswer.indexOf(option.code) !== -1;
        const isCorrectAnswer = item.examquestionAnswer.indexOf(option.code) !== -1;
        
        // Correct answer
        if (isCorrectAnswer) {
          return isCorrect ? 'blue correct' : 'blue correct not-selected';
        }
        
        // Wrong answer
        return userSelected ? 'wrong' : '';
      },
      
      // Return to previous page or specified page
      handleBack() {
        // Can be edited to specific route as needed
        this.$router.push('/index/examList').catch(err => {
          // Ignore redundant navigation errors
          if (!err.message.includes('Avoided redundant navigation')) {
            console.error('Back failed', err);
          }
        });
      },
      
      // Load exam result data
      loadExamResult(params) {
        this.loading = true;
        this.errorMsg = '';
        
        // Get exam paper information
        this.$http.get(`examrecord/info/${params.id}`)
          .then(response => {
            this.headData = response.data.data || {};
            
            // Get exam question data
            return this.$http.get(`examredetails/page`, {
              params: {
                page: 1,
                limit: 100, // Get all questions
                examredetailsUuidNumber: params.examrecordUuidNumber,
                yonghuId: params.yonghuId
              }
            });
          })
          .then(response => {
            this.dataList = response.data.data.list || [];
            
            // Process option data
            this.dataList.forEach((item, index) => {
              if (item.examquestionTypes != 4) {
                try {
                  this.dataList[index].examquestionOptions = JSON.parse(item.examquestionOptions || '[]');
                } catch (e) {
                  console.error("Failed to parse option data", e);
                  this.dataList[index].examquestionOptions = [];
                }
              }
            });
          })
          .catch(error => {
            console.error("Failed to load exam results", error);
            this.errorMsg = "Failed to load exam results, please try again later";
          })
          .finally(() => {
            this.loading = false;
          });
      }
    }
  }
  </script>
  
  <style scoped>
  /* Base Styles */
  .content-bgcolor {
    background-color: #f5f5f5;
  }
  
  .papermain {
    padding: 20px 0;
    min-height: 100vh;
  }
  
  .exam-container {
    max-width: 1440px;
    margin: 0 auto;
    padding: 0 40px;
  }
  
  /* Loading and Error States */
  .loading-state, .error-state {
    text-align: center;
    padding: 50px 0;
    color: #666;
  }
  
  .loading-state p, .error-state p {
    margin-top: 15px;
    font-size: 16px;
  }
  
  .error-state i {
    font-size: 36px;
    color: #F56C6C;
  }
  
  /* Title Area Styles */
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
  
  /* Content Layout */
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
  
  /* Question Styles */
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
  
  .question-num {
    display: inline-block;
    width: 24px;
    height: 24px;
    line-height: 24px;
    text-align: center;
    background-color: #f5f5f5;
    border-radius: 50%;
    margin-bottom: 8px;
  }
  
  .question-score {
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
  
  /* Option Styles */
  .question-options {
    margin-top: 10px;
    list-style: none;
    padding-left: 0;
  }
  
  .question-options li {
    padding: 8px 10px;
    margin-bottom: 8px;
    border-radius: 4px;
    border: 1px solid #eee;
  }
  
  .question-options li.blue {
    background-color: #e6f7ff;
    border-color: #91d5ff;
  }
  
  .question-options li.blue.correct {
    background-color: #f6ffed;
    border-color: #b7eb8f;
  }
  
  .question-options li.blue.correct.not-selected {
    opacity: 0.6;
  }
  
  .question-options li.wrong {
    background-color: #fff2f0;
    border-color: #ffccc7;
  }
  
  .options {
    display: inline-block;
    width: 24px;
    text-align: center;
    margin-right: 8px;
    font-weight: bold;
  }
  
  /* Answer and Analysis Areas */
  .Answer-Box, .Analysis-Box {
    margin-top: 15px;
    padding-top: 10px;
    border-top: 1px dashed #eee;
  }
  
  .My-Answer h3 {
    color: #666;
  }
  
  .Teacher-Answer h3 {
    color: #333;
  }
  
  .answer-correct {
    color: #52c41a;
    font-weight: bold;
  }
  
  .answer-wrong {
    color: #f5222d;
    font-weight: bold;
  }
  
  .answer-right-special {
    color: #1890ff;
    font-weight: bold;
  }
  
  .release {
    background: none;
    border: none;
    color: #333;
    font-weight: bold;
    cursor: pointer;
    padding: 0;
    margin: 0;
  }
  
  .Analysis-Content {
    margin-top: 5px;
    padding: 10px;
    background-color: #f9f9f9;
    border-radius: 3px;
    line-height: 1.5;
  }
  
  /* Right Navigation */
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
  
  .question-resul-tab a.mark {
    background-color: #d9534f;
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
  
  .marki {
    background-color: #d9534f;
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
    width: 100%;
  }
  
  .hm_btn_orange:hover {
    background-color: #e65c00;
  }
  
  #dong {
    position: sticky;
    top: 20px;
    height: fit-content;
  }
  
  /* Responsive Adjustments */
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
  </style>