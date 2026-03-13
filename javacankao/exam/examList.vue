<template>
	<div :style='{"border":"1px solid #e5e9ef","padding":"20px","margin":"10px auto","borderRadius":"8px","background":"#fff","width":"1200px","position":"relative","box-shadow":"0 1px 2px rgba(0,0,0,0.05)"}'>
		<el-button :style='{"cursor":"pointer","padding":"0 12px","margin":"5px 10px","outline":"none","color":"#fff","borderRadius":"4px","background":"#3498db","width":"auto","lineHeight":"36px","fontSize":"14px","height":"36px","transition":"all 0.2s ease"}' type="warning" size="mini" @click="backClick" class="el-icon-back">Back</el-button>
		<div class="section-title" :style='{"padding":"15px 0","margin":"0px 0 20px","color":"#333","borderRadius":"6px","textAlign":"center","background":"#f5f7fa","fontSize":"18px","lineHeight":"24px","fontWeight":"600","borderBottom":"2px solid #3498db"}'>Exam Record</div>
		<el-table
		  :data="tableData"
		  :row-class-name="tableRowClassName"
		  style="width: 100%">
		  <el-table-column
			label="Paper Name"
			prop="papername">
			<template slot-scope="scope">
			  <div :style='{"fontWeight":"500","color":"#3498db","transition":"color 0.2s ease","cursor":"pointer"}'>
				{{ scope.row.papername }}
			  </div>
			</template>
		  </el-table-column>
		  <el-table-column
			label="Exam Score">
			<template slot-scope="scope">
				<div :style='{"fontWeight":"500","color":"#e74c3c"}'>{{ scope.row.myscore || 0 }} points</div>
			</template>
		  </el-table-column>
		  <el-table-column label="Operation" width="100">
			<template slot-scope="scope">
			  <el-button
				type="danger"
				size="mini"
				:style='{"borderRadius":"4px","transition":"all 0.2s ease","width":"70px"}'
				@click="handleView(scope.$index, scope.row)">View</el-button>
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
		  :style='{"width":"1200px","padding":"0","margin":"20px auto","whiteSpace":"nowrap","color":"#333","fontWeight":"500"}'
		  @current-change="curChange"
		  @size-change="sizeChange"
		></el-pagination>
		
	</div>
	</template>
	
	<script>
	  export default {
		data() {
		  return {
			tableData: [],
			total: 0,
			pageSize: 10,
			pageSizes: [10, 20, 30, 50],
			currentPage: 1,
			loading: false,
			errorMsg: ''
		  }
		},
		created() {
		  this.getExamList(1);
		},
		methods: {
		  tableRowClassName({row, rowIndex}) {
            return 'forum-row';
          },
		  backClick() {
			  this.$router.push('/index/center')
		  },
		  getExamList(page) {
			this.loading = true;
			this.errorMsg = '';
			
			this.currentPage = page;
			
			const userTable = localStorage.getItem("UserTableName");
			if (!userTable) {
			  this.errorMsg = "UserTableName not found";
			  this.$message.error(this.errorMsg);
			  this.loading = false;
			  return;
			}
			
			this.$http.get(`${userTable}/session`)
			  .then(sessionResponse => {
				const userInfo = sessionResponse.data.data;
				if (!userInfo || !userInfo.id) {
				  this.errorMsg = "User information does not exist or is incomplete";
				  this.$message.error(this.errorMsg);
				  this.loading = false;
				  return;
				}
				
				const userid = userInfo.id;
				
				this.$http.get(`examrecord/my/${userid}`, {
				  params: {
					page: page,
					limit: this.pageSize
				  }
				})
				.then(res => {
				  if (res.data.code === 0) {
					this.tableData = (res.data.data || []).map(item => ({
					papername: item.exampaper_name,
					myscore: item.total_score,
					paperid: item.exampaper_id,
					...item
					}));
					this.total = res.data.total || this.tableData.length;
					this.pageSize = res.data.pageSize || this.pageSize;
					
					if (this.tableData.length === 0) {
					  this.errorMsg = "No Exam Records Available";
					}
				  } else {
					this.errorMsg = res.data.msg || "Failed to get Exam Records";
					this.$message.error(this.errorMsg);
				  }
				})
				.catch(examError => {
				  console.error("Failed to get Exam Records", examError);
				  this.errorMsg = "Failed to get Exam Records, please try again later";
				  this.$message.error(this.errorMsg);
				})
				.finally(() => {
				  this.loading = false;
				});
			  })
			  .catch(sessionError => {
				console.error("Failed to get user session", sessionError);
				this.errorMsg = "Failed to get user session, please login first";
				this.$message.error(this.errorMsg);
				this.loading = false;
			  });
		  },
		  curChange(page) {
			this.getExamList(page);
		  },
		  sizeChange(newSize) {
			this.pageSize = newSize;
			this.getExamList(1);
		  },
		  handleView(index, row) {
			this.$router.push({
				path: '/index/examResult', 
				query: {
				id: row.id,
				examrecordUuidNumber: row.examrecord_uuid_number,
				yonghuId: row.yonghuId
				}
			});
		  }
		}
	  }
	</script>

<style rel="stylesheet/scss" lang="scss" scoped>
  .section-title {
    font-family: "Helvetica Neue", Arial, sans-serif;
  }
  
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
  
  .el-pagination ::v-deep .el-pagination__total {
  	margin: 0 10px 0 0;
  	color: #666;
  	font-weight: 400;
  	display: inline-block;
  	vertical-align: top;
  	font-size: 13px;
  	line-height: 28px;
  	height: 28px;
  }
  
  .el-pagination ::v-deep .btn-prev,
  .el-pagination ::v-deep .btn-next {
  	border: 1px solid #e5e9ef;
  	border-radius: 4px;
  	padding: 0;
  	margin: 0 5px;
  	color: #666;
  	background: #fff;
  	display: inline-block;
  	vertical-align: top;
  	font-size: 13px;
  	line-height: 28px;
  	min-width: 35px;
  	height: 28px;
  	transition: all 0.2s ease;
  }
  
  .el-pagination ::v-deep .btn-prev:hover,
  .el-pagination ::v-deep .btn-next:hover {
    border-color: #3498db;
    color: #3498db;
  }
  
  .el-pagination ::v-deep .btn-prev:disabled,
  .el-pagination ::v-deep .btn-next:disabled {
  	border: 1px solid #e5e9ef;
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
  	margin: 0 2px;
  	color: #666;
  	display: inline-block;
  	vertical-align: top;
  	font-size: 13px;
  	line-height: 28px;
  	border-radius: 4px;
  	background: #fff;
  	text-align: center;
  	min-width: 30px;
  	height: 28px;
  	transition: all 0.2s ease;
  }
  
  .el-pagination ::v-deep .el-pager .number:hover {
  	color: #3498db;
  	background: #f0f7ff;
  }
  
  .el-pagination ::v-deep .el-pager .number.active {
  	color: #FFF;
  	background: #3498db;
  	font-weight: 500;
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
  
  .el-pagination ::v-deep .el-pagination__sizes .el-input .el-input__inner:focus {
    border-color: #3498db;
  }
  
  .el-pagination ::v-deep .el-pagination__jump {
  	margin: 0 0 0 15px;
  	color: #606266;
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
  
  .el-pagination ::v-deep .el-pagination__jump .el-input .el-input__inner:focus {
    border-color: #3498db;
  }
  
  ::v-deep .el-button--mini {
    padding: 0 10px;
    height: 28px;
    line-height: 28px;
  }
  
  ::v-deep .el-button:hover {
    transform: translateY(-1px);
  }
  
  ::v-deep .el-button:active {
    transform: translateY(0);
  }
</style>