# Padayon Ko - Scholarships for Filipino

[Click me to access the solution on Notion](https://cvk-minerva.notion.site/Padayun-Ko-Scholarships-for-Filipinos-7095196f76e14daab9a37a910b5a70ed).

### ‼️ FOR JUDGES ‼️

**Edit @ aug 13 2024 9pm GMT+8**: I will continue working on this project for the coming government testing. Please [click here](https://github.com/CarlKho-Minerva/padayon-ko/tree/70c5b20280b6cac0e711e466f8ccacb9c8b96fa8) to use the code committed on the **AUG 13 5AM GMT+8** *(2 hours before the deadline)*.

This entry is prototyped in Notion given its popularity amongst students. I will be moving towards a dedicated frontend + DB infrastructure on GCP later. This will be then be piloted in Lapu-Lapu City, Cebu, Philippines in the next few days.

Please view `.env.example` for the API keys needed for you to run the demo.

## 📹 Introduction Video

[![Watch the video](https://i.imgur.com/3IRuTDq.png)](https://youtu.be/MorvT9I0M9I)

---

## Overview

Padayon Ko (Short for "I will continue" in Cebuano Visayan) is a comprehensive platform designed to help Filipino students secure scholarships from start to finish. By leveraging cutting-edge AI tools and integrations, our platform aims to reduce barriers and provide equal opportunities for all students.

## Features

### 1. **Scholarship Repository**

- **Description**: Lists available scholarships with detailed information including eligibility requirements, document requirements (e.g., English proficiency tests, SAT results), and benefits.
- **Technology**: Data extracted from Notion and displayed via a user-friendly interface. Information is disseminated through Facebook using automated posting scripts.
- **Benefits**: Provides students with easy access to a wide range of scholarship opportunities, ensuring they have all necessary information in one place.

### 2. **Profile Building**

- **Achievement Tracker**
  - **Description**: Allows students to enter their achievements, which are then refined into resume-ready bullet points and descriptions by the AI.
  - **Technology**: Google Gemini API for transforming raw data into polished achievements. Integration with Notion for storing and managing achievements.
  - **Benefits**: Helps students present their achievements in a professional format that highlights their impact and skills.

- **Essay Writing Assistance**
  - **Description**: Assists students in crafting responses to common scholarship application questions, ensuring they maintain their unique voice while meeting application standards.
  - **Technology**: Google Gemini API for AI-assisted essay rewriting and tailoring. Integrated with Notion for managing and storing essays.
  - **Benefits**: Reduces the stress of writing essays and ensures that applications are well-prepared and compelling.

### 3. **Personalized Recommendations**

- **Description**: Provides tailored scholarship recommendations based on the student's profile and interests.
- **Technology**: Google Gemini API for semantic embedding and profile matching. Recommendations are processed and presented via Notion.
- **Benefits**: Increases the relevance of scholarship opportunities, improving the likelihood of successful applications.

### 4. **Test Preparation**

- **MathyYou**
  - **Description**: An AI-powered math tutor that converts abstract math problems into interest-aligned scenarios.
  - **Technology**: Google Gemini API for generating and validating math questions. Integration with Python code execution for practice validation.
  - **Benefits**: Makes studying for math tests engaging and relevant, tailored to the student's interests.

- **Fluent**
  - **Description**: Enhances English proficiency through verbal communication practice, including question formation, storytelling, and debate.
  - **Technology**: Google Chirp for speech-to-text transcription, Google Gemini API for interactive conversation, and Google Synthesize for text-to-speech.
  - **Benefits**: Improves English skills through practical exercises and real-time feedback.

### 5. **Application Tracker**

- **Description**: Tracks the status of scholarship applications from submission to acceptance/rejection.
- **Technology**: Integration with Notion for managing application statuses and updates.
- **Benefits**: Keeps students informed about their application progress and helps manage deadlines and follow-ups.

## Technical Aspects

- **Google Gemini API**: Used for essay rewriting, profile matching, and generating personalized scholarship recommendations. It processes and enhances user data through semantic embeddings and AI-driven prompts.
- **Notion**: Serves as the primary database and user interface for managing scholarship information, user profiles, achievements, and essays.
- **Facebook Integration**: Automated posting of scholarship opportunities and updates to reach a wider audience on a platform popular in the Philippines.
- **Google Chirp and Synthesize**: For speech-to-text and text-to-speech functionalities, facilitating verbal communication practice and essay dictation.
- **Python**: Employed for code execution and validation of math practice questions.

## Benefits to Users

- **Equal Access**: Reduces barriers to scholarship opportunities by providing a structured, accessible platform for all students.
- **Comprehensive Support**: Guides users through every step of the scholarship process, from finding opportunities to preparing applications and tests.
- **Personalized Experience**: Offers tailored recommendations and tools based on individual profiles and interests.
- **Enhanced Learning**: Provides tools for improving academic and communication skills through engaging, AI-driven methods.
