# Design Document

## Overview

This design document describes the integration of Baidu Face Recognition API into the Django-based intelligent learning management system. The system will provide three main features: face registration during user signup, face verification before exams, and face-based attendance check-in on the xuexitiandi page.

The design follows a layered architecture with clear separation between the face recognition utility layer, API endpoints, and frontend integration.

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Layer                           │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  Registration │  │  Exam Page   │  │  Xuexitiandi │      │
│  │     Forms     │  │  Verification│  │  Attendance  │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                     Django Backend                           │
│  ┌──────────────────────────────────────────────────────┐   │
│  │              API Endpoints Layer                      │   │
│  │  • /file/upload2 (face search)                       │   │
│  │  • /xuesheng/register (with face)                    │   │
│  │  • /jiaoshi/register (with face)                     │   │
│  │  • /exampaper/verify_face (new)                      │   │
│  │  • /xuexitiandi/attendance (new)                     │   │
│  └──────────────────────────────────────────────────────┘   │
│                            │                                  │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           Face Recognition Utility Layer              │   │
│  │  • FaceUtil class                                     │   │
│  │    - get_access_token()                              │   │
│  │    - register_face(base64_image, user_id)           │   │
│  │    - find_face(base64_image) -> user_id             │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Baidu Face Recognition API                      │
│  • OAuth 2.0 Token Endpoint                                 │
│  • Face Registration Endpoint                                │
│  • Face Search Endpoint                                      │
└─────────────────────────────────────────────────────────────┘
```

### Data Flow

1. **Registration Flow**:
   - User uploads face photo → Frontend sends to backend
   - Backend saves file → Converts to Base64
   - Calls FaceUtil.register_face() → Baidu API
   - On success: Complete user registration
   - On failure: Rollback and return error

2. **Exam Verification Flow**:
   - User clicks start exam → Frontend shows face capture dialog
   - User uploads face → Frontend calls /file/upload2
   - Backend calls FaceUtil.find_face() → Returns user_id
   - Frontend compares user_id with logged-in user
   - Match: Allow exam access | Mismatch: Deny access

3. **Attendance Flow**:
   - User clicks attendance button → Frontend shows face capture
   - User uploads face → Frontend calls /file/upload2
   - Backend returns matched user_id
   - Frontend verifies match → Records attendance (future)


## Components and Interfaces

### 1. FaceUtil Utility Class

**Location**: `util/face_util.py`

**Purpose**: Encapsulates all Baidu Face Recognition API interactions

**Class Definition**:
```python
class FaceUtil:
    API_KEY = "ql21uVftf13jXL0FGEkFCCzH"
    SECRET_KEY = "81L7L2FRTMcEkuMr3opuyx8cccXsEw20"
    GROUP_ID = "aabb"
    TOKEN_URL = "https://aip.baidubce.com/oauth/2.0/token"
    REGISTER_URL = "https://aip.baidubce.com/rest/2.0/face/v3/faceset/user/add"
    SEARCH_URL = "https://aip.baidubce.com/rest/2.0/face/v3/search"
    
    @staticmethod
    def get_access_token() -> str
    
    @staticmethod
    def register_face(base64_image: str, user_id: str) -> dict
    
    @staticmethod
    def find_face(base64_image: str) -> str | None
```

**Method Specifications**:

- `get_access_token()`:
  - Returns: Access token string
  - Raises: Exception if API call fails
  - Caches token for reuse (optional optimization)

- `register_face(base64_image, user_id)`:
  - Parameters:
    - base64_image: Base64-encoded image string
    - user_id: Unique user identifier (string)
  - Returns: Response dict from Baidu API
  - Raises: Exception if registration fails

- `find_face(base64_image)`:
  - Parameters:
    - base64_image: Base64-encoded image string
  - Returns: Matched user_id string or None
  - Extracts user_id from API response

### 2. Modified Registration Endpoints

**Student Registration**: `main/Xuesheng_v.py::xuesheng_register()`

**Teacher Registration**: `main/Jiaoshi_v.py::jiaoshi_register()`

**Modifications**:
```python
def xuesheng_register(request):
    # Existing validation...
    
    # Create user record
    error = xuesheng.createbyreq(xuesheng, xuesheng, req_dict)
    if error != None:
        return JsonResponse({'code': crud_error_code, 'msg': error})
    
    # NEW: Face registration
    try:
        face_photo = req_dict.get('touxiang')  # or appropriate field
        if face_photo:
            file_path = os.path.join(settings.MEDIA_ROOT, face_photo)
            with open(file_path, 'rb') as f:
                image_data = f.read()
                base64_image = base64.b64encode(image_data).decode('utf-8')
            
            user_id = str(req_dict.get('id'))
            FaceUtil.register_face(base64_image, user_id)
    except Exception as e:
        # Rollback user creation
        xuesheng.delete(xuesheng, xuesheng, req_dict.get('id'))
        return JsonResponse({
            'code': crud_error_code,
            'msg': '人脸注册失败，请重试'
        })
    
    return JsonResponse({'code': normal_code, 'msg': mes.normal_code})
```

### 3. Face Search Endpoint

**Location**: `main/schema_v.py::schemaName_face_search()`

**URL**: `/file/upload2`

**Implementation**:
```python
def schemaName_face_search(request):
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "成功", "result": None}
        
        file = request.FILES.get("file")
        if not file:
            msg['code'] = crud_error_code
            msg['msg'] = "未上传文件"
            return JsonResponse(msg)
        
        try:
            # Read file and convert to base64
            file_bytes = file.read()
            base64_image = base64.b64encode(file_bytes).decode('utf-8')
            
            # Search for face
            user_id = FaceUtil.find_face(base64_image)
            msg['result'] = user_id
            
        except Exception as e:
            msg['code'] = crud_error_code
            msg['msg'] = f"人脸识别失败: {str(e)}"
        
        return JsonResponse(msg)
```


### 4. Exam Verification Endpoint

**Location**: `main/Exampaper_v.py::exampaper_verify_face()`

**URL**: `/exampaper/verify_face`

**Implementation**:
```python
def exampaper_verify_face(request):
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "验证成功", "verified": False}
        
        req_dict = request.session.get("req_dict")
        logged_in_user_id = str(request.session.get("params", {}).get("id"))
        
        file = request.FILES.get("file")
        if not file:
            msg['code'] = crud_error_code
            msg['msg'] = "未上传人脸照片"
            return JsonResponse(msg)
        
        try:
            # Convert to base64
            file_bytes = file.read()
            base64_image = base64.b64encode(file_bytes).decode('utf-8')
            
            # Find face
            recognized_user_id = FaceUtil.find_face(base64_image)
            
            if recognized_user_id is None:
                msg['code'] = crud_error_code
                msg['msg'] = "未识别到人脸，请确保面部清晰可见"
                return JsonResponse(msg)
            
            if recognized_user_id == logged_in_user_id:
                msg['verified'] = True
                msg['msg'] = "身份验证成功"
            else:
                msg['code'] = crud_error_code
                msg['msg'] = "人脸与当前登录用户不匹配"
                
        except Exception as e:
            msg['code'] = crud_error_code
            msg['msg'] = f"验证失败: {str(e)}"
        
        return JsonResponse(msg)
```

### 5. Attendance Check-in Endpoint

**Location**: `main/Xuexitiandi_v.py::xuexitiandi_attendance()`

**URL**: `/xuexitiandi/attendance`

**Implementation**:
```python
def xuexitiandi_attendance(request):
    if request.method == "OPTIONS":
        return JsonResponse({})
    if request.method in ["POST", "GET"]:
        msg = {"code": normal_code, "msg": "签到成功", "checked_in": False}
        
        logged_in_user_id = str(request.session.get("params", {}).get("id"))
        
        file = request.FILES.get("file")
        if not file:
            msg['code'] = crud_error_code
            msg['msg'] = "未上传人脸照片"
            return JsonResponse(msg)
        
        try:
            # Convert to base64
            file_bytes = file.read()
            base64_image = base64.b64encode(file_bytes).decode('utf-8')
            
            # Find face
            recognized_user_id = FaceUtil.find_face(base64_image)
            
            if recognized_user_id is None:
                msg['code'] = crud_error_code
                msg['msg'] = "未识别到人脸，请重试"
                return JsonResponse(msg)
            
            if recognized_user_id == logged_in_user_id:
                msg['checked_in'] = True
                msg['msg'] = "考勤签到成功"
                
                # TODO: Record attendance in database
                # attendance_record = {
                #     'user_id': logged_in_user_id,
                #     'check_in_time': datetime.now(),
                #     'location': 'xuexitiandi'
                # }
                # Save to attendance table
                
            else:
                msg['code'] = crud_error_code
                msg['msg'] = "人脸与当前登录用户不匹配"
                
        except Exception as e:
            msg['code'] = crud_error_code
            msg['msg'] = f"签到失败: {str(e)}"
        
        return JsonResponse(msg)
```

## Data Models

### Existing Models (No Changes Required)

**Student Model** (`xuesheng`):
- Already has `touxiang` (profile photo) field
- Will store face photo path

**Teacher Model** (`jiaoshi`):
- Already has `touxiang` (profile photo) field
- Will store face photo path

### Future Attendance Model (Reserved)

```python
class Attendance(models.Model):
    __tablename__ = 'attendance'
    
    id = models.BigAutoField(primary_key=True)
    user_id = models.BigIntegerField()  # Student/Teacher ID
    user_type = models.CharField(max_length=20)  # 'xuesheng' or 'jiaoshi'
    check_in_time = models.DateTimeField(auto_now_add=True)
    location = models.CharField(max_length=50)  # 'xuexitiandi'
    face_verified = models.BooleanField(default=True)
```


## Correctness Properties

A property is a characteristic or behavior that should hold true across all valid executions of a system—essentially, a formal statement about what the system should do. Properties serve as the bridge between human-readable specifications and machine-verifiable correctness guarantees.

### Property 1: Access Token Generation

*For any* API call requiring authentication, calling `get_access_token()` should return a non-empty string that can be used for subsequent API requests.

**Validates: Requirements 1.2**

### Property 2: Group ID Consistency

*For any* face registration or search operation, the request payload should contain the group_id "aabb".

**Validates: Requirements 1.3**

### Property 3: Error Message Descriptiveness

*For any* failed API call, the system should return an error response containing a descriptive message string (non-empty and meaningful).

**Validates: Requirements 1.4**

### Property 4: Base64 Image Encoding

*For any* image file uploaded for face operations, the system should successfully convert it to a valid Base64-encoded string.

**Validates: Requirements 1.5, 2.2, 4.1**

### Property 5: Face Photo Storage

*For any* successfully registered user (student or teacher) with face registration, the user record should contain a non-empty file path to the face photo.

**Validates: Requirements 2.6, 3.6**

### Property 6: Face Search Returns User ID

*For any* face image that matches a registered user, calling `find_face()` should return a user_id string that exists in the database.

**Validates: Requirements 4.3, 8.4**

### Property 7: Empty File Rejection

*For any* file upload request with an empty file, the system should reject the upload and return an error.

**Validates: Requirements 7.2**

### Property 8: Valid File Storage

*For any* valid image file uploaded, the system should save it to the upload directory and the file should exist on disk after the operation.

**Validates: Requirements 7.3**

### Property 9: Filename Return

*For any* successful file upload, the API response should contain the saved filename in the response data.

**Validates: Requirements 7.4**

### Property 10: Exam Authentication Logging

*For any* exam face verification attempt (success or failure), the system should create a log entry with timestamp, user_id, and result.

**Validates: Requirements 5.6**

## Error Handling

### Error Categories

1. **API Communication Errors**:
   - Network timeout
   - Invalid credentials
   - Rate limiting
   - Response: "服务暂时不可用，请稍后重试"

2. **Face Recognition Errors**:
   - No face detected
   - Multiple faces detected
   - Low confidence score
   - Response: "未识别到人脸，请确保面部清晰可见"

3. **User Mismatch Errors**:
   - Recognized user_id ≠ logged-in user_id
   - Response: "人脸与当前登录用户不匹配"

4. **File Upload Errors**:
   - Empty file
   - Invalid format
   - File too large
   - Response: "文件上传失败，请检查文件格式和大小"

5. **Registration Errors**:
   - Face registration fails after user creation
   - Action: Rollback user record
   - Response: "人脸注册失败，请重试"

### Error Handling Strategy

```python
try:
    # Face operation
    result = FaceUtil.some_operation()
except requests.Timeout:
    return error_response("网络超时，请重试")
except requests.RequestException:
    return error_response("服务暂时不可用，请稍后重试")
except ValueError as e:
    return error_response(f"参数错误: {str(e)}")
except Exception as e:
    logging.error(f"Face operation failed: {str(e)}")
    return error_response("操作失败，请联系管理员")
```

### Logging Strategy

All face recognition operations should be logged with:
- Timestamp
- User ID (if available)
- Operation type (register/search/verify)
- Result (success/failure)
- Error details (if failure)

```python
logging.info(f"Face operation: {operation_type}, User: {user_id}, Result: {result}")
```


## Testing Strategy

### Dual Testing Approach

This feature will use both unit tests and property-based tests to ensure comprehensive coverage:

- **Unit tests**: Verify specific examples, edge cases, and error conditions
- **Property tests**: Verify universal properties across all inputs

Both types of tests are complementary and necessary for comprehensive coverage. Unit tests catch concrete bugs in specific scenarios, while property tests verify general correctness across many inputs.

### Unit Testing

Unit tests will focus on:

1. **Specific API Integration Examples**:
   - Test successful face registration with a known image
   - Test successful face search with a registered user
   - Test face verification with matching user_id
   - Test face verification with mismatched user_id

2. **Edge Cases**:
   - Empty file upload
   - Invalid image format
   - Multiple faces in image
   - No face in image
   - API timeout scenarios

3. **Error Conditions**:
   - Network failures
   - Invalid API credentials
   - Malformed API responses
   - Database rollback on face registration failure

4. **Integration Points**:
   - Registration flow with face binding
   - Exam verification flow
   - Attendance check-in flow

### Property-Based Testing

Property tests will be implemented using Python's `hypothesis` library. Each test will run a minimum of 100 iterations to ensure comprehensive input coverage.

**Property Test Configuration**:
```python
from hypothesis import given, settings
import hypothesis.strategies as st

@settings(max_examples=100)
@given(image_data=st.binary(min_size=100, max_size=10000))
def test_property_name(image_data):
    # Test implementation
    pass
```

**Property Tests to Implement**:

1. **Base64 Encoding Property** (Property 4):
   - Generate random binary image data
   - Verify conversion to Base64 always produces valid string
   - Verify decoding Base64 returns original data

2. **File Storage Property** (Property 8):
   - Generate random valid image files
   - Upload each file
   - Verify file exists on disk after upload

3. **Filename Return Property** (Property 9):
   - Generate random valid image files
   - Upload each file
   - Verify response contains a filename
   - Verify filename matches saved file

4. **Empty File Rejection Property** (Property 7):
   - Generate various empty or near-empty files
   - Verify all are rejected with error

5. **Error Message Property** (Property 3):
   - Generate various failure scenarios
   - Verify all return non-empty error messages

### Test Organization

```
tests/
├── unit/
│   ├── test_face_util.py
│   ├── test_registration.py
│   ├── test_exam_verification.py
│   └── test_attendance.py
├── property/
│   ├── test_base64_properties.py
│   ├── test_file_upload_properties.py
│   └── test_error_handling_properties.py
└── integration/
    ├── test_registration_flow.py
    ├── test_exam_flow.py
    └── test_attendance_flow.py
```

### Mocking Strategy

For unit tests, mock external dependencies:
- Mock Baidu API responses using `unittest.mock`
- Mock file system operations for faster tests
- Mock database operations for isolated testing

For integration tests:
- Use test database
- Use test file storage directory
- Consider using Baidu API test credentials if available

### Test Data

Create test fixtures:
- Sample face images (valid formats)
- Sample non-face images
- Sample corrupted images
- Sample user records
- Sample API responses (success and error)


## Frontend Integration Details

### 1. Registration Page Modifications

**Files to Modify**:
- `templates/front/pages/xuesheng/register.html` (or .vue)
- `templates/front/pages/jiaoshi/register.html` (or .vue)

**Changes Required**:

```html
<!-- Add face photo upload field -->
<div class="form-group">
    <label>人脸照片 *</label>
    <input type="file" 
           id="facePhoto" 
           accept="image/jpeg,image/jpg,image/png"
           @change="handleFaceUpload"
           required>
    <img id="facePreview" style="max-width: 200px; display: none;">
</div>
```

```javascript
// JavaScript for face upload
methods: {
    handleFaceUpload(event) {
        const file = event.target.files[0];
        if (file) {
            // Preview image
            const reader = new FileReader();
            reader.onload = (e) => {
                document.getElementById('facePreview').src = e.target.result;
                document.getElementById('facePreview').style.display = 'block';
            };
            reader.readAsDataURL(file);
            
            // Store for submission
            this.facePhotoFile = file;
        }
    },
    
    async submitRegistration() {
        // First upload face photo
        const formData = new FormData();
        formData.append('file', this.facePhotoFile);
        
        const uploadRes = await this.$http.post('/file/upload', formData);
        if (uploadRes.data.code === 0) {
            // Add filename to registration data
            this.registrationData.touxiang = uploadRes.data.file;
            
            // Submit registration
            const regRes = await this.$http.post('/xuesheng/register', this.registrationData);
            if (regRes.data.code === 0) {
                this.$message.success('注册成功');
                this.$router.push('/login');
            } else {
                this.$message.error(regRes.data.msg || '注册失败');
            }
        }
    }
}
```

### 2. Exam Page Modifications

**Files to Modify**:
- `templates/front/pages/exampaper/list.html` (or .vue)
- `templates/front/pages/exampaper/detail.html` (or .vue)

**Changes Required**:

```html
<!-- Face verification dialog -->
<el-dialog title="人脸验证" :visible.sync="showFaceVerification">
    <div class="face-verification">
        <p>开始考试前需要进行人脸验证</p>
        <input type="file" 
               accept="image/*" 
               @change="handleFaceCapture"
               ref="faceInput">
        <el-button @click="$refs.faceInput.click()">
            选择照片
        </el-button>
        <el-button type="primary" 
                   @click="verifyFace"
                   :loading="verifying">
            开始验证
        </el-button>
    </div>
</el-dialog>
```

```javascript
methods: {
    startExam(examId) {
        // Show face verification dialog
        this.currentExamId = examId;
        this.showFaceVerification = true;
    },
    
    handleFaceCapture(event) {
        this.capturedFace = event.target.files[0];
    },
    
    async verifyFace() {
        if (!this.capturedFace) {
            this.$message.warning('请先选择照片');
            return;
        }
        
        this.verifying = true;
        const formData = new FormData();
        formData.append('file', this.capturedFace);
        
        try {
            const res = await this.$http.post('/file/upload2', formData);
            if (res.data.code === 0 && res.data.result) {
                // Check if recognized user matches logged-in user
                const userId = sessionStorage.getItem('userId');
                if (res.data.result === userId) {
                    this.$message.success('验证成功');
                    this.showFaceVerification = false;
                    // Navigate to exam
                    this.$router.push(`/exam/${this.currentExamId}`);
                } else {
                    this.$message.error('人脸与当前登录用户不匹配');
                }
            } else {
                this.$message.error('人脸识别失败，请重试');
            }
        } catch (error) {
            this.$message.error('验证失败，请重试');
        } finally {
            this.verifying = false;
        }
    }
}
```

### 3. Xuexitiandi Page Modifications

**Files to Modify**:
- `templates/front/pages/xuexitiandi/list.html` (or .vue)

**Changes Required**:

```html
<!-- Add attendance button -->
<div class="attendance-section">
    <el-button type="success" 
               icon="el-icon-camera"
               @click="showAttendanceDialog = true">
        人脸识别考勤
    </el-button>
</div>

<!-- Attendance dialog -->
<el-dialog title="考勤打卡" :visible.sync="showAttendanceDialog">
    <div class="attendance-check">
        <p>请上传人脸照片进行考勤打卡</p>
        <input type="file" 
               accept="image/*" 
               @change="handleAttendanceCapture"
               ref="attendanceInput">
        <el-button @click="$refs.attendanceInput.click()">
            选择照片
        </el-button>
        <el-button type="primary" 
                   @click="checkInAttendance"
                   :loading="checkingIn">
            打卡签到
        </el-button>
    </div>
</el-dialog>
```

```javascript
data() {
    return {
        showAttendanceDialog: false,
        attendanceFace: null,
        checkingIn: false
    };
},

methods: {
    handleAttendanceCapture(event) {
        this.attendanceFace = event.target.files[0];
    },
    
    async checkInAttendance() {
        if (!this.attendanceFace) {
            this.$message.warning('请先选择照片');
            return;
        }
        
        this.checkingIn = true;
        const formData = new FormData();
        formData.append('file', this.attendanceFace);
        
        try {
            const res = await this.$http.post('/file/upload2', formData);
            if (res.data.code === 0 && res.data.result) {
                // Check if recognized user matches logged-in user
                const userId = sessionStorage.getItem('userId');
                if (res.data.result === userId) {
                    this.$message.success('考勤打卡成功');
                    this.showAttendanceDialog = false;
                    
                    // TODO: Call attendance recording API when implemented
                    // await this.$http.post('/xuexitiandi/attendance', {
                    //     user_id: userId,
                    //     check_in_time: new Date()
                    // });
                } else {
                    this.$message.error('人脸与当前登录用户不匹配');
                }
            } else {
                this.$message.error('人脸识别失败，请重试');
            }
        } catch (error) {
            this.$message.error('打卡失败，请重试');
        } finally {
            this.checkingIn = false;
        }
    }
}
```

## Security Considerations

1. **API Credentials**:
   - Store in environment variables or config file (not hardcoded in production)
   - Rotate credentials periodically
   - Monitor API usage for anomalies

2. **Image Upload**:
   - Validate file size (max 5MB)
   - Validate file type (only jpg, jpeg, png)
   - Sanitize filenames
   - Store in secure directory with limited access

3. **User Verification**:
   - Always verify session user_id matches recognized user_id
   - Log all verification attempts
   - Implement rate limiting to prevent abuse

4. **Data Privacy**:
   - Face images are sensitive personal data
   - Comply with data protection regulations
   - Provide user consent mechanism
   - Allow users to delete their face data

## Performance Considerations

1. **API Response Time**:
   - Baidu Face API typically responds in 1-3 seconds
   - Implement timeout (10 seconds)
   - Show loading indicators to users

2. **Image Size Optimization**:
   - Compress images before upload (client-side)
   - Recommended size: 640x480 or smaller
   - Reduces upload time and API processing time

3. **Caching**:
   - Cache access tokens (valid for 30 days)
   - Reduce token API calls

4. **Concurrent Requests**:
   - Baidu API has rate limits
   - Implement request queuing if needed
   - Monitor API quota usage

## Deployment Notes

1. **Dependencies**:
   - Add `requests` library to requirements.txt (already present)
   - No additional Python packages required

2. **Configuration**:
   - Update API credentials in production
   - Configure file upload directory permissions
   - Set up logging directory

3. **Database**:
   - No schema changes required for initial implementation
   - Future: Create attendance table when needed

4. **Testing**:
   - Test with real Baidu API in staging environment
   - Verify file upload permissions
   - Test error handling scenarios

5. **Monitoring**:
   - Monitor API success/failure rates
   - Track response times
   - Alert on high error rates
