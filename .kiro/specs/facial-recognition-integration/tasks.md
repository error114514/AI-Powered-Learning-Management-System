# Implementation Plan: Facial Recognition Integration

## Overview

This implementation plan breaks down the facial recognition integration into discrete, manageable tasks. Each task builds on previous work and includes specific requirements references.

## Tasks

- [x] 1. Create Face Recognition Utility Module
  - Create `util/face_util.py` with FaceUtil class
  - Implement `get_access_token()` method to obtain Baidu API token
  - Implement `register_face(base64_image, user_id)` method
  - Implement `find_face(base64_image)` method
  - Add proper error handling and logging
  - _Requirements: 1.1, 1.2, 1.3, 1.4, 1.5_

- [x] 1.1 Write unit tests for FaceUtil class
  - Test successful token retrieval
  - Test face registration with valid image
  - Test face search with registered user
  - Test error handling for API failures
  - _Requirements: 1.2, 1.3, 1.4_

- [x] 1.2 Write property test for Base64 encoding
  - **Property 4: Base64 Image Encoding**
  - **Validates: Requirements 1.5, 2.2, 4.1**

- [x] 2. Modify Student Registration with Face Binding
  - Update `main/Xuesheng_v.py::xuesheng_register()` function
  - Add face photo upload handling
  - Convert uploaded image to Base64
  - Call `FaceUtil.register_face()` after user creation
  - Implement rollback on face registration failure
  - Add error messages for face registration failures
  - _Requirements: 2.1, 2.2, 2.3, 2.4, 2.5, 2.6_

- [x] 2.1 Write unit tests for student registration with face
  - Test successful registration with face photo
  - Test registration failure when face photo missing
  - Test rollback when face API fails
  - Test file path storage in student record
  - _Requirements: 2.1, 2.3, 2.4, 2.6_

- [x] 2.2 Write property test for face photo storage
  - **Property 5: Face Photo Storage**
  - **Validates: Requirements 2.6, 3.6**

- [x] 3. Modify Teacher Registration with Face Binding
  - Update `main/Jiaoshi_v.py::jiaoshi_register()` function
  - Add face photo upload handling (same as student)
  - Convert uploaded image to Base64
  - Call `FaceUtil.register_face()` after user creation
  - Implement rollback on face registration failure
  - Add error messages for face registration failures
  - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.5, 3.6_

- [x] 3.1 Write unit tests for teacher registration with face
  - Test successful registration with face photo
  - Test registration failure when face photo missing
  - Test rollback when face API fails
  - Test file path storage in teacher record
  - _Requirements: 3.1, 3.3, 3.4, 3.6_

- [x] 4. Checkpoint - Ensure registration tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 5. Implement Face Search Endpoint
  - Add `schemaName_face_search()` function to `main/schema_v.py`
  - Handle file upload from request
  - Convert uploaded image to Base64
  - Call `FaceUtil.find_face()` to search for face
  - Return matched user_id in response
  - Handle errors (no face found, API failures)
  - _Requirements: 4.1, 4.2, 4.3, 4.4, 8.1, 8.2, 8.3, 8.4, 8.5_

- [x] 5.1 Write unit tests for face search endpoint
  - Test successful face search with registered user
  - Test face search with unregistered face
  - Test empty file upload rejection
  - Test invalid image format handling
  - _Requirements: 4.2, 4.3, 4.4, 7.2_

- [x] 5.2 Write property test for face search returns user ID
  - **Property 6: Face Search Returns User ID**
  - **Validates: Requirements 4.3, 8.4**

- [x] 5.3 Write property test for empty file rejection
  - **Property 7: Empty File Rejection**
  - **Validates: Requirements 7.2**


- [x] 6. Update File Upload Endpoint
  - Modify `schemaName_file_upload()` in `main/schema_v.py`
  - Add validation for empty files
  - Add validation for image file formats (jpg, jpeg, png)
  - Ensure file is saved to upload directory
  - Return filename in response
  - _Requirements: 7.1, 7.2, 7.3, 7.4, 7.5_

- [x] 6.1 Write property test for valid file storage
  - **Property 8: Valid File Storage**
  - **Validates: Requirements 7.3**

- [x] 6.2 Write property test for filename return
  - **Property 9: Filename Return**
  - **Validates: Requirements 7.4**

- [x] 7. Add URL Routes for New Endpoints
  - Add route for `/file/upload2` (face search) in `main/urls.py`
  - Verify existing `/file/upload` route
  - Test routes are accessible
  - _Requirements: 7.1, 8.1_

- [x] 8. Implement Exam Face Verification Endpoint
  - Create `exampaper_verify_face()` function in `main/Exampaper_v.py`
  - Handle face photo upload
  - Convert to Base64 and call `FaceUtil.find_face()`
  - Compare recognized user_id with logged-in user_id
  - Return verification result (success/failure)
  - Add logging for all verification attempts
  - _Requirements: 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_

- [x] 8.1 Write unit tests for exam verification
  - Test successful verification with matching user
  - Test failed verification with mismatched user
  - Test verification with no face detected
  - Test verification logging
  - _Requirements: 5.4, 5.5, 5.6_

- [x] 8.2 Write property test for exam authentication logging
  - **Property 10: Exam Authentication Logging**
  - **Validates: Requirements 5.6**

- [x] 9. Add Exam Verification Route
  - Add route for `/exampaper/verify_face` in `main/urls.py`
  - Test route is accessible
  - _Requirements: 5.3_

- [x] 10. Implement Attendance Check-in Endpoint
  - Create `xuexitiandi_attendance()` function in `main/Xuexitiandi_v.py`
  - Handle face photo upload
  - Convert to Base64 and call `FaceUtil.find_face()`
  - Compare recognized user_id with logged-in user_id
  - Return check-in result
  - Add TODO comment for future attendance record storage
  - _Requirements: 6.3, 6.4, 6.5, 6.7_

- [x] 10.1 Write unit tests for attendance check-in
  - Test successful check-in with matching user
  - Test failed check-in with mismatched user
  - Test check-in with no face detected
  - _Requirements: 6.4, 6.5_

- [x] 11. Add Attendance Route
  - Add route for `/xuexitiandi/attendance` in `main/urls.py`
  - Test route is accessible
  - _Requirements: 6.7_

- [x] 12. Checkpoint - Ensure all backend tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [x] 13. Update Student Registration Frontend
  - Modify student registration page template
  - Add face photo upload field with file input
  - Add image preview functionality
  - Update form submission to upload face photo first
  - Add face photo filename to registration data
  - Add error handling and user feedback
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [x] 14. Update Teacher Registration Frontend
  - Modify teacher registration page template
  - Add face photo upload field with file input
  - Add image preview functionality
  - Update form submission to upload face photo first
  - Add face photo filename to registration data
  - Add error handling and user feedback
  - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

- [x] 15. Add Face Verification to Exam Page
  - Modify exam list/detail page template
  - Add face verification dialog component
  - Add file input for face photo capture
  - Implement verification logic on exam start
  - Call `/file/upload2` endpoint with face photo
  - Compare returned user_id with logged-in user
  - Show success/error messages
  - Navigate to exam on successful verification
  - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_

- [x] 16. Add Attendance Button to Xuexitiandi Page
  - Modify xuexitiandi page template
  - Add "人脸识别考勤" button
  - Add attendance check-in dialog component
  - Add file input for face photo capture
  - Implement check-in logic
  - Call `/file/upload2` endpoint with face photo
  - Compare returned user_id with logged-in user
  - Show success/error messages
  - Add TODO comment for future attendance API call
  - _Requirements: 11.1, 11.2, 11.3, 11.4, 11.5, 11.6, 11.7_

- [x] 17. Implement Error Messages
  - Add error message constants for face registration failures
  - Add error message constants for face verification failures
  - Add error message constants for user mismatch
  - Add error message constants for API errors
  - Ensure all error messages are user-friendly in Chinese
  - _Requirements: 12.1, 12.2, 12.3, 12.4, 12.5_

- [x] 18. Add Logging Configuration
  - Configure logging for face recognition operations
  - Add log entries for registration attempts
  - Add log entries for verification attempts
  - Add log entries for attendance check-ins
  - Add log entries for API errors
  - _Requirements: 5.6, 12.5_

- [ ] 19. Final Integration Testing
  - Test complete registration flow (student and teacher)
  - Test complete exam verification flow
  - Test complete attendance check-in flow
  - Test error scenarios end-to-end
  - Verify all error messages display correctly
  - Verify logging works correctly

- [ ] 20. Documentation and Deployment Preparation
  - Update README with face recognition feature description
  - Document API endpoints and parameters
  - Document configuration requirements
  - Add deployment notes for production
  - Add security considerations documentation

## Notes

- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- Frontend tasks focus on user experience and integration
- All error messages should be in Chinese for user-friendliness
- All tasks are required for comprehensive implementation
