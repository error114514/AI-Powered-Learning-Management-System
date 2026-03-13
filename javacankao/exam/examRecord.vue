<template>
	<div :style='{"border":"1px solid #e5e9ef","padding":"20px","margin":"10px auto","borderRadius":"8px","background":"#fff","width":"1200px","position":"relative","box-shadow":"0 1px 2px rgba(0,0,0,0.05)"}'>
	  <!-- Back按钮 -->
	  <el-button 
		:style='{"cursor":"pointer","padding":"0 12px","margin":"5px 10px","outline":"none","color":"#fff","borderRadius":"4px","background":"#3498db","width":"auto","lineHeight":"36px","fontSize":"14px","height":"36px","transition":"all 0.2s ease"}' 
		type="warning" 
		size="mini" 
		@click="backClick" 
		class="el-icon-back">
		Back
	  </el-button>
	  
	  <!-- 标题区域 -->
	  <div class="section-title" :style='{"padding":"15px 0","margin":"0px 0 20px","color":"#333","borderRadius":"6px","textAlign":"center","background":"#f5f7fa","fontSize":"18px","lineHeight":"24px","fontWeight":"600","borderBottom":"2px solid #3498db"}'>
		Mistake Record
	  </div>
	  
	  <!-- 加载状态 -->
	  <div v-if="loading" class="loading-state">
		<el-loading-spinner></el-loading-spinner>
		<p>Loading...</p>
	  </div>
	  
	  <!-- 错误状态 -->
	  <div v-if="errorMsg && !loading" class="error-state">
		<i class="el-icon-error"></i>
		<p>{{ errorMsg }}</p>
		<el-button type="primary" @click="loadData()">Reload</el-button>
	  </div>
	  
	  <!-- 表格区域 -->
	  <el-table
		v-if="!loading && !errorMsg"
		:data="tableData"
		:row-class-name="tableRowClassName"
		style="width: 100%"
		border>
		<el-table-column
		  label="Paper"
		  prop="exampaperName"
		  width="200">
		  <template slot-scope="scope">
			{{ scope.row.exampaperName || 'After-class Assignment' }}
		  </template>
		</el-table-column>
		<el-table-column
		  label="Questions"
		  prop="examquestionName">
		  <template slot-scope="scope">
			<div class="question-text">
			  {{ scope.row.examquestionName | truncate(30) }}
			</div>
		  </template>
		</el-table-column>
		<el-table-column
		  label="My Answer"
		  prop="examredetailsMyanswer">
		  <template slot-scope="scope">
			<div :style="scope.row.examredetailsMyanswer ? '' : 'color: #999'">
			  {{ scope.row.examredetailsMyanswer || 'Not Answered' }}
			</div>
		  </template>
		</el-table-column>
		<el-table-column
		  label="Record Time"
		  prop="insertTime"
		  width="160">
		</el-table-column>
	  </el-table>
	  
	  <!-- 分页组件 -->
	  <el-pagination
		v-if="!loading && !errorMsg && total > 0"
		background
		class="pagination"
		:pager-count="7"
		:page-size="pageSize"
		:page-sizes="[10, 20, 30, 50]"
		prev-text="<"
		next-text=">"
		:hide-on-single-page="true"
		:layout='["total","prev","pager","next","sizes","jumper"].join()'
		:total="total"
		:current-page="currentPage"
		:style='{"width":"100%","padding":"0","margin":"20px auto 0","whiteSpace":"nowrap","color":"#333","fontWeight":"500","display":"flex","justify-content":"center","align-items":"center","gap":"10px"}'
		@current-change="handleCurrentChange"
		@size-change="handleSizeChange"
	  ></el-pagination>
	  
	  <!-- 空状态 -->
	  <div v-if="!loading && !errorMsg && total === 0" class="empty-state">
		<!-- <img src="https://picsum.photos/200/150" alt="No wrong questions" /> -->
		<p>No Mistake Records</p>
	  </div>
	</div>
  </template>
  
  <script>
  export default {
	name: 'WrongQuestionBook',
	data() {
	  return {
		tableData: [],
		total: 0,
		pageSize: 10,
		currentPage: 1,
		loading: false,
		errorMsg: '',
		userId: '' // Store current user ID
	  };
	},
	created() {
	  // Get user ID
	  this.getUserId();
	},
	filters: {
	  // Truncate long text and add ellipsis
	  truncate(value, length = 20) {
		if (!value) return '';
		// Remove HTML tags
		const text = value.replace(/<[^<>]+>/g, '').replace(/undefined/g, '');
		if (text.length <= length) return text;
		return text.substring(0, length) + '...';
	  }
	},
	methods: {
	  // Add row style class method
	  tableRowClassName({row, rowIndex}) {
        return 'forum-row';
      },
	  
	  // Back to previous page
	  backClick() {
		this.$router.push('/index/center').catch(err => {
		  if (!err.message.includes('Avoided redundant navigation')) {
			console.error('Back failed', err);
		  }
		});
	  },
	  
	  // Get user ID
	  getUserId() {
		// Get from URL parameter or local storage
		const urlUserId = this.$route.query.userid;
		const storedUser = localStorage.getItem('UserTableName');
		
		if (urlUserId) {
		  this.userId = urlUserId;
		  this.loadData();
		} else if (storedUser) {
		  // If user info exists in local storage, try to get ID from it
		  this.$http.get(`${storedUser}/session`)
			.then(response => {
			  const userInfo = response.data.data;
			  if (userInfo && userInfo.id) {
				this.userId = userInfo.id;
				this.loadData();
			  } else {
				this.errorMsg = 'Failed to get user information, please login again';
			  }
			})
			.catch(error => {
			  console.error('Failed to get user information', error);
			  this.errorMsg = 'Failed to get user information';
			});
		} else {
		  this.errorMsg = 'Missing user information, please login again';
		}
	  },
	  
	  // Load wrong question data
	  loadData() {
		if (!this.userId) {
		  this.errorMsg = 'Missing user ID, unable to load wrong question data';
		  return;
		}
		
		this.loading = true;
		this.errorMsg = '';
		
		this.$http.get('examrewrongquestion/page', {
		  params: {
			page: this.currentPage,
			limit: this.pageSize,
			sort: "id",
			myscore: 0, // Only load wrong questions with score 0
			yonghuId: this.userId
		  }
		})
		.then(response => {
		  if (response.data.code === 0) {
			this.tableData = response.data.data.list || [];
			this.total = response.data.data.total || 0;
		  // Ensure page number is within valid range
		  if (this.total > 0 && this.currentPage > Math.ceil(this.total / this.pageSize)) {
			  this.currentPage = 1;
			}
		  } else {
			this.errorMsg = response.data.msg || 'Failed to get wrong question data';
		  }
		})
		.catch(error => {
		  console.error('Failed to get wrong question data', error);
		  this.errorMsg = 'Failed to get wrong question data, please try again later';
		})
		.finally(() => {
		  this.loading = false;
		});
	  },
	  
	  // Handle page number change
	  handleCurrentChange(page) {
		// Prevent reloading the same page number
		if (page !== this.currentPage) {
			this.currentPage = page;
			this.loadData();
		}
	  },
	  
	  // Handle page size change
	  handleSizeChange(size) {
		this.pageSize = size;
		this.currentPage = 1; // Reset to first page
		this.loadData();
	  },
	  
	}
  };
  </script>
  
  <style scoped>
  .section-title {
    font-family: "Helvetica Neue", Arial, sans-serif;
  }
  
  /* Loading state style */
  .loading-state {
	text-align: center;
	padding: 50px 0;
	color: #666;
  }
  
  .loading-state p {
	margin-top: 15px;
	font-size: 16px;
  }
  
  /* Error state style */
  .error-state {
	text-align: center;
	padding: 50px 0;
	color: #F56C6C;
  }
  
  .error-state i {
	font-size: 36px;
	margin-bottom: 15px;
  }
  
  .error-state p {
	margin-bottom: 20px;
	font-size: 16px;
  }
  
  /* Empty state style */
  .empty-state {
	text-align: center;
	padding: 50px 0;
	color: #999;
  }
  
  .empty-state img {
	width: 200px;
	height: 150px;
	object-fit: contain;
	margin-bottom: 15px;
	opacity: 0.5;
  }
  
  /* Questions text style */
  .question-text {
	cursor: pointer;
	color: #3498db;
	transition: color 0.2s ease;
  }
  
  .question-text:hover {
	color: #2980b9;
	text-decoration: underline;
  }
  
  /* Table style */
  ::v-deep .forum-row {
    transition: background-color 0.2s ease;
  }
  
  ::v-deep .forum-row:hover {
    background-color: #f9fafc;
  }
  
  ::v-deep .el-table {
    border: 1px solid #e5e9ef;
    border-radius: 6px;
    overflow: hidden;
  }
  
  ::v-deep .el-table th {
    background-color: #f5f7fa;
    color: #666;
    font-weight: 500;
    border-bottom: 1px solid #e5e9ef;
    padding: 12px 0;
  }
  
  ::v-deep .el-table td {
    border-bottom: 1px solid #f0f2f5;
    padding: 15px 0;
  }
  
  ::v-deep .el-table tr:last-child td {
    border-bottom: none;
  }
  
  /* Pagination style override */
  ::v-deep .el-pagination {
	margin-top: 20px;
  }
  
  ::v-deep .el-pagination__total {
	color: #666;
	font-weight: 400;
  }
  
  ::v-deep .btn-prev,
  ::v-deep .btn-next {
  	border: 1px solid #e5e9ef;
  	border-radius: 4px;
  	padding: 0;
  	margin: 0 5px;
  	color: #666;
  	background: #fff;
  	font-size: 13px;
  	line-height: 28px;
  	min-width: 35px;
  	height: 28px;
  	transition: all 0.2s ease;
  }
  
  ::v-deep .btn-prev:hover,
  ::v-deep .btn-next:hover {
    border-color: #3498db;
    color: #3498db;
  }
  
  ::v-deep .btn-prev:disabled,
  ::v-deep .btn-next:disabled {
  	border: 1px solid #e5e9ef;
  	cursor: not-allowed;
  	color: #C0C4CC;
  	background: #f5f7fa;
  }
  
  ::v-deep .el-pager {
  	padding: 0;
  	margin: 0;
  }
  
  ::v-deep .el-pager .number {
  	cursor: pointer;
  	padding: 0 8px;
  	margin: 0 2px;
  	color: #666;
  	font-size: 13px;
  	line-height: 28px;
  	border-radius: 4px;
  	background: #fff;
  	text-align: center;
  	min-width: 30px;
  	height: 28px;
  	transition: all 0.2s ease;
  }
  
  ::v-deep .el-pager .number:hover {
  	color: #3498db;
  	background: #f0f7ff;
  }
  
  ::v-deep .el-pager .number.active {
  	color: #FFF;
  	background: #3498db;
  	font-weight: 500;
  }
  
  ::v-deep .el-pagination__sizes {
  	font-size: 13px;
  	line-height: 28px;
  	height: 28px;
  }
  
  ::v-deep .el-pagination__sizes .el-input {
  	margin: 0 5px;
  	width: 100px;
  	position: relative;
  }
  
  ::v-deep .el-pagination__sizes .el-input .el-input__inner {
  	border: 1px solid #e5e9ef;
  	cursor: pointer;
  	padding: 0 25px 0 8px;
  	color: #606266;
  	font-size: 13px;
  	line-height: 28px;
  	border-radius: 4px;
  	outline: 0;
  	background: #FFF;
  	width: 100%;
  	text-align: center;
  	height: 28px;
  	transition: border-color 0.2s ease;
  }
  
  ::v-deep .el-pagination__sizes .el-input .el-input__inner:focus {
    border-color: #3498db;
  }
  
  ::v-deep .el-pagination__jump {
  	color: #606266;
  	font-size: 13px;
  	line-height: 28px;
  	height: 28px;
  }
  
  ::v-deep .el-pagination__jump .el-input {
  	border-radius: 4px;
  	padding: 0 2px;
  	margin: 0 2px;
  	width: 50px;
  	font-size: 14px;
  	line-height: 18px;
  	text-align: center;
  	height: 28px;
  }
  
  ::v-deep .el-pagination__jump .el-input .el-input__inner {
  	border: 1px solid #e5e9ef;
  	cursor: pointer;
  	padding: 0 3px;
  	color: #606266;
  	font-size: 14px;
  	line-height: 28px;
  	border-radius: 4px;
  	outline: 0;
  	background: #FFF;
  	width: 100%;
  	text-align: center;
  	height: 28px;
  	transition: border-color 0.2s ease;
  }
  
  ::v-deep .el-pagination__jump .el-input .el-input__inner:focus {
    border-color: #3498db;
  }
  
  ::v-deep .el-button {
    transition: all 0.2s ease;
  }
  
  ::v-deep .el-button:hover {
    transform: translateY(-1px);
  }
  
  ::v-deep .el-button:active {
    transform: translateY(0);
  }
  </style>