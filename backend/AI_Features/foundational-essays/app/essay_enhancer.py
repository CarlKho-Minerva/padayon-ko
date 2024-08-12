from config import model


def process_essay_by_type(essay_type: str, cleaned_essay: str) -> str:
    processing_functions = {
        "tell_us_about_you": process_tell_us_about_you_essay,
        "how_are_you_unique": process_how_are_you_unique_essay,
        "failure_and_learning": process_failure_and_learning_essay,
        "academic_and_career_goals": process_academic_and_career_goals_essay,
        "community_contribution": process_community_contribution_essay,
        "deserve_scholarship": process_deserve_scholarship_essay,
        "scholarship_help": process_scholarship_help_essay,
        "sports_impact": process_sports_impact_essay,
        "why_study_pursue": process_why_study_pursue_essay,
        "belief_challenged": process_belief_challenged_essay,
    }

    if essay_type in processing_functions:
        return processing_functions[essay_type](cleaned_essay)
    else:
        return "Invalid essay type"


def refine_and_optimize_essay(essay, prompt_type):
    refinePrompt = f"""
    Refine and optimize this essay for a scholarship application. Tailor it to the "{prompt_type}" prompt while maintaining the original tone and voice. Ensure it doesn't sound artificial and it being able to be read by an academic and professional audience but not lose character.

    Guidelines:
    1. Enhance the narrative structure
    2. Emphasize personal growth and challenges overcome
    3. Maintain authenticity and original voice
    4. Ensure relevance to the specific prompt
    5. Avoid clichés and overly formal language

    Essay: {essay}

    Refined essay:
    """
    response = model.generate_content(refinePrompt)
    return response.text


# Define all the process_*_essay functions here
def process_tell_us_about_you_essay(userInput):
    prompt = f"""
    Enhance this "Tell Us About You" scholarship essay. Focus on:
    1. Personal challenges and how they were overcome
    2. Responsibilities taken on within family or community
    3. Significant achievements
    4. Future aspirations and their connection to past experiences

    Essay: {userInput}

    Enhanced essay:
    """
    response = model.generate_content(prompt)
    return response.text


def process_how_are_you_unique_essay(userInput):
    prompt = f"""
    Enhance this "How Are You Unique?" scholarship essay. Focus on:
    1. Unique aspects of background, identity, interests, or talents
    2. Significance of these unique qualities
    3. Specific examples demonstrating uniqueness
    4. How these qualities contribute to academic or personal goals

    Essay: {userInput}

    Enhanced essay:
    """
    response = model.generate_content(prompt)
    return response.text


def process_failure_and_learning_essay(userInput):
    prompt = f"""
    Enhance this "Tell Us About a Time You Failed and What You Learned From It" essay. Focus on:
    1. Description of the failure
    2. Impact of the failure
    3. Emotions and needs that arose from the experience
    4. Actions taken to address the failure
    5. Lessons learned and how they've been applied

    Essay: {userInput}

    Enhanced essay:
    """
    response = model.generate_content(prompt)
    return response.text


def process_academic_and_career_goals_essay(userInput):
    prompt = f"""
    Enhance this "What Are Your Academic and Career Goals?" essay. Focus on:
    1. Specific academic goals
    2. Career aspirations
    3. Challenges that shaped these goals
    4. Steps taken or planned to achieve these goals
    5. How these goals align with personal values or experiences

    Essay: {userInput}

    Enhanced essay:
    """
    response = model.generate_content(prompt)
    return response.text


def process_community_contribution_essay(userInput):
    prompt = f"""
    Enhance this "How Have You Contributed to Your Community?" essay. Focus on:
    1. Specific community service project or contribution
    2. Problem or challenge addressed
    3. Actions taken and individual role
    4. Impact on the community
    5. Personal growth and lessons learned

    Essay: {userInput}

    Enhanced essay:
    """
    response = model.generate_content(prompt)
    return response.text


def process_deserve_scholarship_essay(userInput):
    prompt = f"""
    Enhance this "Why Do You Deserve This Scholarship?" essay. Focus on:
    1. Personal qualities that make you a strong candidate
    2. Academic or extracurricular achievements
    3. Challenges overcome
    4. Future potential and how the scholarship will help
    5. Alignment with the scholarship's mission or values

    Essay: {userInput}

    Enhanced essay:
    """
    response = model.generate_content(prompt)
    return response.text


def process_scholarship_help_essay(userInput):
    prompt = f"""
    Enhance this "How Will This Scholarship Help You?" essay. Focus on:
    1. Specific ways the scholarship will be used
    2. Financial challenges or needs
    3. Academic or career goals supported by the scholarship
    4. Potential impact on your future
    5. How you plan to pay it forward or contribute to society

    Essay: {userInput}

    Enhanced essay:
    """
    response = model.generate_content(prompt)
    return response.text


def process_sports_impact_essay(userInput):
    prompt = f"""
    Enhance this "What Impact Has Sports Had on Your Life?" essay. Focus on:
    1. Specific sport or athletic activity
    2. Life lessons learned through sports
    3. Personal growth and character development
    4. Challenges overcome through sports
    5. How sports have influenced other areas of life

    Essay: {userInput}

    Enhanced essay:
    """
    response = model.generate_content(prompt)
    return response.text


def process_why_study_pursue_essay(userInput):
    prompt = f"""
    Enhance this "Why Do You Want to Study/Pursue [X]?" essay. Focus on:
    1. Specific field of study or career path
    2. Experiences that sparked interest in this field
    3. Relevant skills or knowledge already acquired
    4. Future goals related to this field
    5. Potential impact or contribution to the field

    Essay: {userInput}

    Enhanced essay:
    """
    response = model.generate_content(prompt)
    return response.text


def process_belief_challenged_essay(userInput):
    prompt = f"""
    Enhance this "Tell Us About a Time When You Had a Belief or Idea Challenged" essay. Focus on:
    1. Initial belief or idea
    2. Situation or experience that challenged this belief
    3. Thought process and emotions during the challenge
    4. How the belief or idea changed (if it did)
    5. Lessons learned or personal growth from this experience

    Essay: {userInput}

    Enhanced essay:
    """
    response = model.generate_content(prompt)
    return response.text
