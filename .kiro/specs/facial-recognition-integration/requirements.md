# Requirements Document

## Introduction

This document specifies the requirements for integrating Baidu Face Recognition API into the intelligent learning management system. The system will enable facial recognition for user registration, exam authentication, and attendance tracking in the learning platform (xuexitiandi).

## Glossary

- **System**: The intelligent learning management system (Django backend + Vue frontend)
- **Face_Recognition_Service**: The Baidu Face Recognition API integration service
- **Student**: A registered student user in the system
- **Teacher**: A registered teacher user in the system
- **Exam_Paper**: An examination that requires identity verification
- **Xuexitiandi**: The learning platform/community page where attendance is tracked
- **Face_Image**: A Base64-encoded image containing a human face
- **User_ID**: The unique identifier for a student or teacher in the system
- **Group_ID**: The Baidu Face API group identifier (fixed as "aabb")
- **Access_Token**: The authentication token for Baidu Face API
- **Attendance_Record**: A record of a user's presence verified by facial recognition

## Requirements

### Requirement 1: Baidu Face API Integration

**User Story:** As a system administrator, I want to integrate Baidu Face Recognition API, so that the system can perform facial recognition operations.

#### Acceptance Criteria

1. THE System SHALL store Baidu API credentials (API_KEY and SECRET_KEY) securely
2. WHEN the System needs to call Baidu Face API, THE System SHALL obtain a valid access token
3. THE System SHALL use the fixed group_id "aabb" for all face registration and search operations
4. WHEN API calls fail, THE System SHALL return descriptive error messages
5. THE System SHALL handle Base64 image encoding and decoding for all face operations

### Requirement 2: Student Registration with Face Binding

**User Story:** As a student, I want to upload my face photo during registration, so that my identity can be verified later.

#### Acceptance Criteria

1. WHEN a student registers, THE System SHALL require a face photo upload
2. WHEN a face photo is uploaded, THE System SHALL convert it to Base64 format
3. WHEN registration is submitted, THE System SHALL call Baidu Face API to register the face with the student's user_id
4. IF face registration fails, THEN THE System SHALL rollback the user registration and return an error
5. WHEN face registration succeeds, THE System SHALL complete the student registration
6. THE System SHALL store the face photo file path in the student record

### Requirement 3: Teacher Registration with Face Binding

**User Story:** As a teacher, I want to upload my face photo during registration, so that my identity can be verified later.

#### Acceptance Criteria

1. WHEN a teacher registers, THE System SHALL require a face photo upload
2. WHEN a face photo is uploaded, THE System SHALL convert it to Base64 format
3. WHEN registration is submitted, THE System SHALL call Baidu Face API to register the face with the teacher's user_id
4. IF face registration fails, THEN THE System SHALL rollback the user registration and return an error
5. WHEN face registration succeeds, THE System SHALL complete the teacher registration
6. THE System SHALL store the face photo file path in the teacher record

### Requirement 4: Face Recognition Verification

**User Story:** As a system, I want to verify user identity through facial recognition, so that I can authenticate users for secure operations.

#### Acceptance Criteria

1. WHEN a face image is submitted for verification, THE System SHALL convert it to Base64 format
2. WHEN verification is requested, THE System SHALL call Baidu Face API search endpoint
3. WHEN a face is found, THE System SHALL return the matched user_id
4. WHEN no face is found or confidence is too low, THE System SHALL return null or error
5. THE System SHALL handle multiple faces in an image by using the first detected face

### Requirement 5: Exam Pre-Authentication

**User Story:** As a student, I want to verify my identity through facial recognition before starting an exam, so that exam integrity is maintained.

#### Acceptance Criteria

1. WHEN a student attempts to start an exam, THE System SHALL require face verification first
2. WHEN face verification is requested, THE System SHALL prompt the student to upload a face photo
3. WHEN the face photo is submitted, THE System SHALL call the face recognition verification endpoint
4. IF the recognized user_id matches the logged-in student, THEN THE System SHALL allow exam access
5. IF the recognized user_id does not match or recognition fails, THEN THE System SHALL deny exam access with an error message
6. THE System SHALL log all exam authentication attempts

### Requirement 6: Attendance Check-in via Face Recognition

**User Story:** As a student, I want to check in for attendance using facial recognition on the xuexitiandi page, so that my presence is recorded.

#### Acceptance Criteria

1. WHEN a student visits the xuexitiandi page, THE System SHALL display a face recognition attendance button
2. WHEN the attendance button is clicked, THE System SHALL prompt the student to upload a face photo
3. WHEN the face photo is submitted, THE System SHALL call the face recognition verification endpoint
4. IF the recognized user_id matches the logged-in student, THEN THE System SHALL record the attendance
5. IF the recognized user_id does not match or recognition fails, THEN THE System SHALL display an error message
6. THE System SHALL display attendance check-in status to the user
7. THE System SHALL reserve an attendance API endpoint for future attendance record storage

### Requirement 7: File Upload Endpoint

**User Story:** As a developer, I want a dedicated file upload endpoint, so that face images can be uploaded and processed.

#### Acceptance Criteria

1. THE System SHALL provide a file upload endpoint at /file/upload
2. WHEN a file is uploaded, THE System SHALL validate that the file is not empty
3. WHEN a valid file is uploaded, THE System SHALL save it to the upload directory
4. THE System SHALL return the saved filename to the client
5. THE System SHALL support image file formats (jpg, jpeg, png)

### Requirement 8: Face Search Endpoint

**User Story:** As a developer, I want a face search endpoint, so that uploaded face images can be matched against registered users.

#### Acceptance Criteria

1. THE System SHALL provide a face search endpoint at /file/upload2
2. WHEN a face image is uploaded to this endpoint, THE System SHALL convert it to Base64
3. THE System SHALL call Baidu Face API search with the Base64 image
4. THE System SHALL return the matched user_id in the response
5. IF no match is found, THE System SHALL return null in the result field

### Requirement 9: Frontend Registration Integration

**User Story:** As a frontend developer, I want to integrate face upload into registration forms, so that users can register with facial recognition.

#### Acceptance Criteria

1. THE Student_Registration_Page SHALL include a face photo upload field
2. THE Teacher_Registration_Page SHALL include a face photo upload field
3. WHEN a user selects a face photo, THE System SHALL preview the image
4. WHEN registration is submitted, THE System SHALL include the face photo in the request
5. THE System SHALL display success or error messages based on registration result

### Requirement 10: Frontend Exam Authentication Integration

**User Story:** As a frontend developer, I want to add face verification before exams, so that students must verify identity before starting.

#### Acceptance Criteria

1. WHEN a student clicks to start an exam, THE System SHALL display a face verification dialog
2. THE Face_Verification_Dialog SHALL allow the student to upload or capture a face photo
3. WHEN the face photo is submitted, THE System SHALL call the face search endpoint
4. IF verification succeeds, THE System SHALL close the dialog and start the exam
5. IF verification fails, THE System SHALL display an error and prevent exam access

### Requirement 11: Frontend Attendance Button Integration

**User Story:** As a frontend developer, I want to add an attendance button to xuexitiandi page, so that students can check in with facial recognition.

#### Acceptance Criteria

1. THE Xuexitiandi_Page SHALL display a face recognition attendance button
2. WHEN the attendance button is clicked, THE System SHALL display a face capture dialog
3. THE Face_Capture_Dialog SHALL allow the student to upload or capture a face photo
4. WHEN the face photo is submitted, THE System SHALL call the face search endpoint
5. IF the recognized user matches the logged-in user, THE System SHALL display success message
6. IF recognition fails or user mismatch, THE System SHALL display error message
7. THE System SHALL provide visual feedback during the recognition process

### Requirement 12: Error Handling and User Feedback

**User Story:** As a user, I want clear error messages when facial recognition fails, so that I understand what went wrong.

#### Acceptance Criteria

1. WHEN face registration fails, THE System SHALL display "Face registration failed, please try again"
2. WHEN face verification fails, THE System SHALL display "Face verification failed, please ensure your face is clearly visible"
3. WHEN user mismatch occurs, THE System SHALL display "Face does not match logged-in user"
4. WHEN API errors occur, THE System SHALL display "Service temporarily unavailable, please try again later"
5. THE System SHALL log all errors for debugging purposes
