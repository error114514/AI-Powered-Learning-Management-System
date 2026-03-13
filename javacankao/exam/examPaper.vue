<template>
    <div :style='{"border":"1px solid #e0e6ed","padding":"25px","margin":"15px auto","borderRadius":"10px","background":"#ffffff","width":"1200px","position":"relative","box-shadow":"0 2px 12px rgba(0,0,0,0.05)"}'>
        <div class="section-title" :style='{"padding":"18px 0","margin":"0 0 20px","color":"#333333","borderRadius":"8px","textAlign":"center","background":"#f5f7fa","fontSize":"22px","lineHeight":"28px","fontWeight":"600","borderBottom":"2px solid #3498db"}'>Paper List</div>
        <el-table
            :data="tableData"
            style="width: 100%"
            :row-style="{transition: 'all 0.3s ease'}"
            :cell-style="{padding: '15px 0'}">
            <el-table-column
                label="Paper Name"
                prop="exampaperName"
                :label-style="{color: '#666666', fontWeight: '500', padding: '12px 15px'}">
            </el-table-column>
            <el-table-column
                label="Exam Duration (minutes)"
                :label-style="{color: '#666666', fontWeight: '500', padding: '12px 15px'}">
                <template slot-scope="scope">
                    {{ scope.row.exampaperDate }} minutes
                </template>
            </el-table-column>
            <el-table-column
                label="Total Score"
                :label-style="{color: '#666666', fontWeight: '500', padding: '12px 15px'}">
                <template slot-scope="scope">
                    {{ scope.row.exampaperMyscore }} points
                </template>
            </el-table-column>
            <el-table-column
                label="Exam Time"
                width="250"
                :label-style="{color: '#666666', fontWeight: '500', padding: '12px 15px'}">
                <template slot-scope="scope">
                    {{ formatDate(scope.row.startTime) }} - {{ formatDate(scope.row.endTime) }}
                </template>
            </el-table-column>
            <el-table-column label="Operation" width="200" :label-style="{color: '#666666', fontWeight: '500', padding: '12px 15px'}">
                <template slot-scope="scope">
                    <el-button
                        v-if="scope.row.canExam"
                        type="success"
                        size="mini"
                        :style="{transition: 'all 0.3s ease'}"
                        @click="handleExam(scope.row.id)">Start Exam</el-button>
                    <span v-else-if="scope.row.examined" style="color: #67c23a;">Exam Attended</span>
                    <span v-else-if="scope.row.exampaperTypes==2" style="color: #909399;">Exam Not Enabled</span>
                    <span v-else style="color: #f56c6c;">Exam Not Started Yet</span>
                </template>
            </el-table-column>
        </el-table>
        
        <el-pagination
            background
            class="pagination"
            :pager-count="7"
            :page-size="pageSize"
            :page-sizes="pageSizes"
            prev-text="<"
            next-text=">"
            :hide-on-single-page="true"
            :layout='["total","prev","pager","next","sizes","jumper"].join()'
            :total="total"
            :style='{"width":"1200px","padding":"20px 0 0","margin":"20px auto 0","whiteSpace":"nowrap","color":"#333333","fontWeight":"500","textAlign":"center"}'
            @current-change="curChange"
            @prev-click="prevClick"
            @next-click="nextClick"
            @size-change="sizeChange"
        ></el-pagination>

        <!-- 人脸识别验证弹窗 -->
        <el-dialog
            title="Identity Verification - Face Recognition"
            :visible.sync="faceRecognitionDialogVisible"
            width="500px"
            :close-on-click-modal="false"
            :close-on-press-escape="false"
            :show-close="false">
            <div class="face-recognition-content">
                <div style="margin: 10px 0; text-align: center; font-size: 16px; color: #333;">
                    Please upload your face photo for identity verification
                </div>
                
                <!-- 图片上传组件 -->
                <el-upload 
                    class="upload-demo"
                    :action="$config.baseUrl + 'file/upload2'"
                    :on-success="handleFaceRecognitionSuccess"
                    :on-error="handleFaceRecognitionError"
                    :before-upload="beforeFaceUpload"
                    :show-file-list="false"
                    :disabled="verifyingFace">
                    <el-button 
                        size="medium" 
                        type="primary"
                        :loading="verifyingFace"
                        style="margin: 0 auto; display: block;">
                        {{ verifyingFace ? 'Verifying...' : 'Upload Face Photo' }}
                    </el-button>
                </el-upload>
                
                <!-- 上传状态提示 -->
                <p v-if="uploadStatus" :style="{color: uploadStatus.includes('成功') ? '#67c23a' : '#f56c6c', textAlign: 'center', marginTop: '10px'}">
                    {{ uploadStatus }}
                </p>
                
                <!-- 预览上传的图片 -->
                <img 
                    v-if="previewUrl"
                    :src="previewUrl"
                    alt="Face Photo"
                    style="max-width: 100%; margin: 15px auto; display: block; max-height: 200px; border-radius: 8px;">
                
                <!-- 验证结果 -->
                <div v-if="recognitionResult" class="result-container" style="text-align: center; margin: 10px 0;">
                    <p><strong>Verification Result:</strong> {{ recognitionResult }}</p>
                </div>
            </div>
            
            <div slot="footer" class="dialog-footer">
                <el-button 
                    @click="cancelFaceRecognition"
                    :disabled="verifyingFace">
                    Cancel
                </el-button>
                <el-button 
                    type="primary" 
                    @click="confirmExamAfterVerification"
                    :disabled="!faceRecognitionPassed || verifyingFace">
                    Confirm and Start Exam
                </el-button>
            </div>
        </el-dialog>
    </div>
</template>

<script>
export default {
    data() {
        return {
            tableData: [],
            pageSize: 5,
            pageSizes: [5, 10, 20, 30],
            currentPage: 1,
            total: 0,
            currentTime: new Date(), // Current System Time
            userTableName: localStorage.getItem('UserTableName'), // 当前用户表名（student/teacher）
            
            // 人脸识别相关变量
            faceRecognitionDialogVisible: false, // 人脸识别弹窗显示状态
            currentExamPaperId: null, // 当前要考试的试卷ID
            previewUrl: '', // 人脸照片预览URL
            uploadStatus: '', // 上传状态提示
            recognitionResult: '', // 识别结果
            verifyingFace: false, // 是否正在验证中
            faceRecognitionPassed: false, // 人脸识别是否通过
            selectedFile: null // 选中的文件
        }
    },
    created() {
        // Store current URL for Back function
        localStorage.setItem("goUtl", "./pages/exampaper/list.html");
        // Load Paper data
        this.loadData();
    },
    methods: {
        // Format date
        formatDate(date) {
            if (!date) return '';
            const d = new Date(date);
            return `${d.getFullYear()}-${this.padZero(d.getMonth() + 1)}-${this.padZero(d.getDate())} ${this.padZero(d.getHours())}:${this.padZero(d.getMinutes())}`;
        },
        
        // Add zero padding
        padZero(num) {
            return num < 10 ? '0' + num : num;
        },
        
        // Load Paper data
        loadData() {
            // 获取当前用户ID（从localStorage中获取）
            const userId = localStorage.getItem('userid');
            
            this.$http({
                url: `exampaper/page`,
                method: "get",
                params: {
                    page: this.currentPage,
                    limit: this.pageSize,
                    userId: userId // 传递当前用户ID
                }
            }).then(({ data }) => {
                if (data && data.code === 0) {
                    // Process paper data and add exam eligibility status
                    this.tableData = data.data.list.map(item => {
                        // Parse exam time
                       // Handle possible date format issues
						const startTime = item.startTime ? new Date(item.startTime) : null;
                   		const endTime = item.endTime ? new Date(item.endTime) : null;
                		const now = new Date();
                        
                        // Check if within exam time range
						const inTimeRange = startTime && endTime && now >= startTime && now <= endTime;
                        
                        // Comprehensive check for exam eligibility
						item.canExam = inTimeRange && item.exampaperTypes === 1 && !item.examined;
                        
                        return item;
                    });
                    this.total = data.data.total;
                }
            });
        },
        
        // 点击开始考试 - 先弹出人脸识别验证
        handleExam(id) {
            // 重置人脸识别状态
            this.resetFaceRecognitionState();
            // 保存当前试卷ID
            this.currentExamPaperId = id;
            // 显示人脸识别弹窗
            this.faceRecognitionDialogVisible = true;
        },
        
        // 重置人脸识别状态
        resetFaceRecognitionState() {
            this.previewUrl = '';
            this.uploadStatus = '';
            this.recognitionResult = '';
            this.verifyingFace = false;
            this.faceRecognitionPassed = false;
            this.selectedFile = null;
        },
        
        // 人脸识别图片上传前处理
        beforeFaceUpload(file) {
            this.selectedFile = file;
            this.verifyingFace = true;
            this.uploadStatus = '';
            this.recognitionResult = '';
            
            // 创建图片预览URL
            const reader = new FileReader();
            reader.onload = (e) => {
                this.previewUrl = e.target.result;
            };
            reader.readAsDataURL(file);
            
            // 限制文件类型和大小
            const isImage = file.type.startsWith('image/');
            const isLt2M = file.size / 1024 / 1024 < 2;
            
            if (!isImage) {
                this.$message.error('Only image files are allowed!');
                this.verifyingFace = false;
                return false;
            }
            if (!isLt2M) {
                this.$message.error('Image size cannot exceed 2MB!');
                this.verifyingFace = false;
                return false;
            }
            
            return true;
        },
        
        // 人脸识别上传成功处理
        handleFaceRecognitionSuccess(response, file, fileList) {
            this.uploadStatus = 'Upload successful';
            this.verifyingFace = false;
            
            try {
                // 解析返回结果
                const result = JSON.parse(response.result);
                // 从localStorage获取当前用户ID（与个人中心页面保持一致）
                const userId = localStorage.getItem('userid');
                
                console.log('Received result:', result);
                console.log('userId:', userId);
                
                // 验证是否为本人
                if (userId == result) {
                    this.faceRecognitionPassed = true;
                    this.recognitionResult = 'Identity verification successful - you are the valid candidate';
                    this.$message({
                        type: 'success',
                        message: 'Face recognition verification passed!'
                    });
                } else {
                    this.faceRecognitionPassed = false;
                    this.recognitionResult = 'Identity verification failed - not the valid candidate';
                    this.$message({
                        type: 'error',
                        message: 'Face recognition verification failed! You are not the valid candidate.'
                    });
                }
            } catch (error) {
                console.error('Face recognition result parsing error:', error);
                this.faceRecognitionPassed = false;
                this.recognitionResult = 'Verification failed - system error';
                this.$message.error('Face recognition verification failed! System error.');
                this.verifyingFace = false;
            }
        },
        
        // 人脸识别上传失败处理
        handleFaceRecognitionError(error, file, fileList) {
            this.uploadStatus = 'Upload failed';
            this.recognitionResult = 'Upload failed - please try again';
            this.faceRecognitionPassed = false;
            this.verifyingFace = false;
            this.$message.error('Face photo upload failed! Please try again.');
            console.error('Face recognition upload error:', error);
        },
        
        // 取消人脸识别
        cancelFaceRecognition() {
            this.faceRecognitionDialogVisible = false;
            this.resetFaceRecognitionState();
            this.$message.info('Face recognition verification cancelled');
        },
        
        // 验证通过后确认开始考试
        confirmExamAfterVerification() {
            if (!this.faceRecognitionPassed) {
                this.$message.error('Please complete face recognition verification first!');
                return;
            }
            
            // 关闭人脸识别弹窗
            this.faceRecognitionDialogVisible = false;
            
            // 显示考试确认弹窗
            this.$confirm(
                'Are you sure to start the exam? The timer will start once the exam begins, and you can only take it once.', 
                'Start Exam', 
                {
                    confirmButtonText: 'Confirm',
                    cancelButtonText: 'Cancel',
                    type: 'warning'
                }
            ).then(() => {
                // 跳转到考试页面
                this.$router.push({ path: `/exam?exampaperId=${this.currentExamPaperId}` });
            }).catch(() => {
                this.$message.info('Exam cancelled');
                this.resetFaceRecognitionState();
            });
        },
        
        // Pagination related methods
        curChange(page) {
            this.currentPage = page;
            this.loadData();
        },
        prevClick(page) {
            this.currentPage = page;
            this.loadData();
        },
        nextClick(page) {
            this.currentPage = page;
            this.loadData();
        },
        sizeChange(size) {
            this.pageSize = size;
            this.currentPage = 1; // Reset to first page
            this.loadData();
        }
    }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .section {
    width: 900px;
    margin: 0 auto;
  }
  
  ::v-deep .el-table {
    border: 1px solid #e0e6ed;
    border-radius: 8px;
    overflow: hidden;
  }
  
  ::v-deep .el-table th {
    background-color: #f5f7fa;
    border-bottom: 1px solid #e0e6ed;
    font-weight: 500;
  }
  
  ::v-deep .el-table tr {
    background-color: #ffffff;
  }
  
  ::v-deep .el-table tr:hover > td {
    background-color: #f0f7ff !important;
  }
  
  ::v-deep .el-table td {
    border-bottom: 1px solid #f0f2f5;
    color: #666666;
  }
  
  ::v-deep .el-table__header-wrapper {
    border-bottom: 1px solid #e0e6ed;
  }
  
  ::v-deep .el-table__body tr.current-row > td {
    background-color: #e6f7ff !important;
  }
  
  ::v-deep .el-button--success {
    background-color: #52c41a;
    border-color: #52c41a;
  }
  
  ::v-deep .el-button--success:hover {
    background-color: #4cae4c;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px rgba(82, 196, 26, 0.3);
  }
  
  .el-pagination ::v-deep .el-pagination__total {
  	margin: 0 10px 0 0;
  	color: #666666;
  	font-weight: 400;
  	display: inline-block;
  	vertical-align: top;
  	font-size: 13px;
  	line-height: 28px;
  	height: 28px;
  }
  
  .el-pagination ::v-deep .btn-prev,
  .el-pagination ::v-deep .btn-next {
  	border: 1px solid #e0e6ed;
  	border-radius: 4px;
  	padding: 0;
  	margin: 0 5px;
  	color: #666666;
  	background: #fff;
  	display: inline-block;
  	vertical-align: top;
  	font-size: 13px;
  	line-height: 28px;
  	min-width: 35px;
  	height: 28px;
  	transition: all 0.3s ease;
  }
  
  .el-pagination ::v-deep .btn-prev:hover,
  .el-pagination ::v-deep .btn-next:hover {
  	border-color: #3498db;
  	color: #3498db;
  	transform: translateY(-2px);
  }
  
  .el-pagination ::v-deep .btn-prev:disabled,
  .el-pagination ::v-deep .btn-next:disabled {
  	border: 1px solid #e0e6ed;
  	cursor: not-allowed;
  	color: #C0C4CC;
  	background: #f5f7fa;
  }
  
  .el-pagination ::v-deep .el-pager {
  	padding: 0;
  	margin: 0;
  	display: inline-block;
  	vertical-align: top;
  }
  
  .el-pagination ::v-deep .el-pager .number {
  	cursor: pointer;
  	padding: 0 8px;
  	margin: 0 4px;
  	color: #666666;
  	display: inline-block;
  	vertical-align: top;
  	font-size: 13px;
  	line-height: 28px;
  	border-radius: 4px;
  	background: #fff;
  	text-align: center;
  	min-width: 30px;
  	height: 28px;
  	transition: all 0.3s ease;
  }
  
  .el-pagination ::v-deep .el-pager .number:hover {
  	color: #3498db;
  	background: rgba(52, 152, 219, 0.1);
  	transform: translateY(-2px);
  }
  
  .el-pagination ::v-deep .el-pager .number.active {
  	cursor: default;
  	color: #FFF;
  	background: #3498db;
  }
  
  .el-pagination ::v-deep .el-pagination__sizes {
  	display: inline-block;
  	vertical-align: top;
  	font-size: 13px;
  	line-height: 28px;
  	height: 28px;
  }
  
  .el-pagination ::v-deep .el-pagination__sizes .el-input {
  	margin: 0 5px;
  	width: 100px;
  	position: relative;
  }
  
  .el-pagination ::v-deep .el-pagination__sizes .el-input .el-input__inner {
  	border: 1px solid #e0e6ed;
  	cursor: pointer;
  	padding: 0 25px 0 8px;
  	color: #666666;
  	font-size: 13px;
  	line-height: 28px;
  	border-radius: 4px;
  	background: #FFF;
  	width: 100%;
  	text-align: center;
  	height: 28px;
  	transition: border-color 0.3s ease;
  }
  
  .el-pagination ::v-deep .el-pagination__sizes .el-input .el-input__inner:focus {
  	border-color: #3498db;
  }
  
  .el-pagination ::v-deep .el-pagination__jump {
  	margin: 0 0 0 24px;
  	color: #666666;
  	display: inline-block;
  	vertical-align: top;
  	font-size: 13px;
  	line-height: 28px;
  	height: 28px;
  }
  
  .el-pagination ::v-deep .el-pagination__jump .el-input {
  	border-radius: 4px;
  	padding: 0 2px;
  	margin: 0 2px;
  	display: inline-block;
  	width: 50px;
  	font-size: 14px;
  	line-height: 18px;
  	position: relative;
  	text-align: center;
  	height: 28px;
  }
  
  .el-pagination ::v-deep .el-pagination__jump .el-input .el-input__inner {
  	border: 1px solid #e0e6ed;
  	cursor: pointer;
  	padding: 0 3px;
  	color: #666666;
  	font-size: 14px;
  	line-height: 28px;
  	border-radius: 4px;
  	background: #FFF;
  	width: 100%;
  	text-align: center;
  	height: 28px;
  	transition: border-color 0.3s ease;
  }
  
  .el-pagination ::v-deep .el-pagination__jump .el-input .el-input__inner:focus {
  	border-color: #3498db;
  }
  
  /* 人脸识别弹窗样式 */
  ::v-deep .face-recognition-content {
    padding: 10px 0;
  }
  
  ::v-deep .el-dialog__header {
    border-bottom: 1px solid #e0e6ed;
    padding-bottom: 10px;
  }
  
  ::v-deep .el-dialog__title {
    font-size: 18px;
    font-weight: 600;
    color: #3498db;
  }
  
  ::v-deep .el-dialog__body {
    padding: 20px;
  }
  
  ::v-deep .el-dialog__footer {
    border-top: 1px solid #e0e6ed;
    padding-top: 15px;
  }
</style>