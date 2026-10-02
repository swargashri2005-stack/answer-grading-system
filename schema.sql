-- Create the database
CREATE DATABASE IF NOT EXISTS answer_grading;
USE answer_grading;

-- Table 1: students
CREATE TABLE students (
    id INT AUTO_INCREMENT PRIMARY KEY,
    roll_number VARCHAR(50) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_students_roll_number (roll_number)
);

-- Table 2: questions
CREATE TABLE questions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_text TEXT NOT NULL,
    max_marks DECIMAL(5,2) NOT NULL CHECK (max_marks >= 0),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_questions_created_at (created_at)
);

-- Table 3: answers (both reference AND student answers live here)
CREATE TABLE answers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT NOT NULL,
    student_id INT NULL,
    answer_type ENUM('reference', 'student') NOT NULL,
    answer_text TEXT NULL,
    marks_obtained FLOAT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (question_id) REFERENCES questions(id),
    FOREIGN KEY (student_id) REFERENCES students(id),
    INDEX idx_answers_question_type (question_id, answer_type),
    INDEX idx_answers_student_question (student_id, question_id)
);

-- Table 4: results
CREATE TABLE results (
    id INT AUTO_INCREMENT PRIMARY KEY,
    question_id INT NOT NULL,
    student_id INT NOT NULL,
    algorithm VARCHAR(50) NOT NULL,
    similarity_score FLOAT NOT NULL,
    marks FLOAT NOT NULL,
    letter_grade CHAR(1) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (question_id) REFERENCES questions(id),
    FOREIGN KEY (student_id) REFERENCES students(id),
    INDEX idx_results_question_student_algorithm (question_id, student_id, algorithm)
);