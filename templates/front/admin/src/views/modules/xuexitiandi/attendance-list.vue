<template>
  <el-dialog
    :title="dialogTitle"
    :visible.sync="dialogVisible"
    width="80%"
    :before-close="handleClose"
  >
    <el-table
      :data="attendanceList"
      border      style="width: 100%"
      v-loading="loading"
    >
      <el-table-column
        prop="id"
        label="考勤 ID"
      ></el-table-column>
      <el-table-column
        prop="course_name"
        label="课程名"
      ></el-table-column>
      <el-table-column
        prop="user_name"
        label="用户名"
      ></el-table-column>
      <el-table-column
        prop="attendance_time"
        label="考勤时间"
      ></el-table-column>
    </el-table>
  </el-dialog>
</template>

<script>
export default {
  props: {
    visible: {
      type: Boolean,
      default: false
    },
    course_id: {
      type: Number,
      default: 0
    }
  },
  data() {
    return {
      dialogVisible: this.visible,
      dialogTitle: '课程考勤列表',
      attendanceList: [],
      loading: false
    }
  },
  watch: {
    visible(newVal) {
      this.dialogVisible = newVal
    },
    dialogVisible(newVal) {
      this.$emit('update:visible', newVal)
      if (newVal) {
        this.getAttendanceList()
      }
    }
  },
  methods: {
    async getAttendanceList() {
      this.loading = true
      try {
        const response = await this.$http.get(`/api/courses/${this.course_id}/attendance/`)
        if (response.data && response.data.code === 200) {
          this.attendanceList = response.data.data || []
        } else {
          this.attendanceList = []
        }
      } catch (error) {
        console.error('获取考勤列表失败:', error)
        this.$message.error('获取考勤列表失败：' + (error.message || '未知错误'))
        this.attendanceList = []
      } finally {
        this.loading = false
      }
    },
    handleClose() {
      this.dialogVisible = false
    }
  }
}
</script>