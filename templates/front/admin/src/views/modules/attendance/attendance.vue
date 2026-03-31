<template>
  <div class="attendance-container">
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>课程考勤</span>
      </div>

      <el-form :model="form" ref="form" label-width="120px">
        <el-form-item label="选择课程">
          <el-select v-model="form.course_id" placeholder="请选择课程" @change="loadStudents">
            <el-option
              v-for="course in courses"
              :key="course.id"
              :label="course.biaoti"
              :value="course.id"
            ></el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="学生列表">
          <el-checkbox-group v-model="form.student_ids">
            <el-checkbox
              v-for="student in students"
              :key="student.id"
              :label="student.id"
              :disabled="!form.course_id"
            >{{ student.xingming }}</el-checkbox>
          </el-checkbox-group>
        </el-form-item>

        <el-form-item>
          <el-button type="primary" @click="submitAttendance">提交考勤</el-button>
          <el-button @click="resetForm">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>考勤记录</span>
      </div>
      <el-table :data="attendanceRecords" border style="width: 100%">
        <el-table-column prop="id" label="考勤ID" width="80"></el-table-column>
        <el-table-column prop="course_name" label="课程名" width="120"></el-table-column>
        <el-table-column prop="user_name" label="学生姓名" width="120"></el-table-column>
        <el-table-column prop="attendance_time" label="考勤时间" width="180"></el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script>
export default {
  data() {
    return {
      form: {
        course_id: '',
        student_ids: []
      },
      courses: [],
      students: [],
      attendanceRecords: []
    }
  },
  created() {
    this.loadCourses()
  },
  methods: {
    async loadCourses() {
      try {
        const response = await this.$http.get('/api/courses/')
        this.courses = response.data
      } catch (error) {
        this.$message.error('加载课程列表失败: ' + error.message)
      }
    },
    async loadStudents() {
      if (!this.form.course_id) {
        this.students = []
        return
      }

      try {
        const response = await this.$http.get(`/api/courses/${this.form.course_id}/students/`)
        this.students = response.data
      } catch (error) {
        this.$message.error('加载学生列表失败: ' + error.message)
      }
    },
    async submitAttendance() {
      if (!this.form.course_id || this.form.student_ids.length === 0) {
        this.$message.warning('请选择课程和学生')
        return
      }

      try {
        const now = new Date()
        const attendanceTime = now.toISOString()

        // 为每个学生创建考勤记录
        for (const studentId of this.form.student_ids) {
          await this.$http.post('/api/attendance/', {
            course_id: this.form.course_id,
            user_id: studentId,
            attendance_time: attendanceTime
          })
        }

        this.$message.success('考勤提交成功')
        this.resetForm()
        this.loadAttendanceRecords()
      } catch (error) {
        this.$message.error('考勤提交失败: ' + error.message)
      }
    },
    async loadAttendanceRecords() {
      try {
        const response = await this.$http.get('/api/attendance/records/')
        this.attendanceRecords = response.data
      } catch (error) {
        this.$message.error('加载考勤记录失败: ' + error.message)
      }
    },
    resetForm() {
      this.$refs.form.resetFields()
      this.students = []
    }
  }
}
</script>

<style scoped>
.attendance-container {
  padding: 20px;
}
.box-card {
  margin-bottom: 20px;
}
</style>