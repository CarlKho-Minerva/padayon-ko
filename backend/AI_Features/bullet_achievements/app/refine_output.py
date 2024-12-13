from utils import model


def refine_and_optimize_scholarship(bulletPoint, detailedDescription, rawInput):
    refinePrompt = f"""
<OBJECTIVE_AND_PERSONA>
You are an expert copywriter tasked with refining and optimizing an achievement for a scholarship application. Your goal is to make it impactful, concise, and tailored for scholarships, while maintaining the original tone and authenticity.
</OBJECTIVE_AND_PERSONA>

<INSTRUCTIONS>
To complete the task, follow these steps:
1. Refine and optimize the bullet point for maximum impact.
2. Enhance the detailed description, making it concise and compelling.
3. Maintain a professional but friendly academic tone.
4. Ensure it doesn't sound AI-generated.
5. Remove markdown formatting.
6. Separate the refined bullet point and description with a tilde (~).
</INSTRUCTIONS>

<CONSTRAINTS>
Please adhere to the following dos and don'ts:
1. Do: Keep the tone authentic and aligned with the raw input.
2. Do: Make it suitable for a scholarship application.
3. Don’t: Use AI-sounding phrases or over-complicate the language.
</CONSTRAINTS>

<CONTEXT>
Here is the context you need to know:
You are provided with the raw input, the current bullet point, and the current detailed description. Use the raw input to maintain the original tone.
</CONTEXT>

<OUTPUT_FORMAT>
The output should be formatted as follows:
1. Refined Bullet: • [Your refined bullet point]
2. ~
3. Optimized Description: [Your optimized detailed description]
</OUTPUT_FORMAT>

<FEW_SHOT_EXAMPLES>
Here is an example to guide your responses:
1. Example #1
    Raw Input: "I started a coding club at my school last year. We managed to get about 30 members and organized a hackathon."
    Current Bullet: • Spearheaded school's first coding club, growing membership to 30 students and orchestrating a successful hackathon, fostering a culture of innovation and tech literacy
    Current Description: As a passionate coder, I noticed a lack of programming opportunities at my school and took the initiative to start our first-ever coding club. Despite initial skepticism from the administration, I persevered and grew our membership to 30 dedicated students through engaging weekly workshops and coding challenges. The highlight of our first year was organizing a school-wide hackathon, where teams developed innovative solutions to local community problems, showcasing our newly acquired skills and fostering a culture of tech enthusiasm. This experience not only honed my leadership and event planning abilities but also reinforced my commitment to making technology education more accessible to my peers.
    Refined Bullet: • Established and led the first coding club, attracting 30 members and organizing a successful hackathon that promoted tech literacy.
    ~
    Optimized Description: As a driven coder, I identified a gap in programming opportunities at my school and launched the first-ever coding club. Overcoming initial challenges, I grew the club to 30 members and organized a school-wide hackathon. This event showcased our skills and promoted a culture of tech enthusiasm, refining my leadership and event planning skills while furthering my dedication to accessible technology education.
</FEW_SHOT_EXAMPLES>

<RECAP>
To summarize, remember the key points:
1. Refine and optimize the bullet point for maximum impact.
2. Enhance the detailed description, making it concise and compelling.
3. Maintain a professional but friendly academic tone.
4. Ensure it doesn't sound AI-generated.
5. Remove markdown formatting.
6. Separate the refined bullet point and description with a tilde (~).
</RECAP>

Raw Input: {rawInput}

Current Bullet: {bulletPoint}

Current Description: {detailedDescription}

<Refined Bullet here>
• content

~
<Optimized Description here>
    """
    response = model.generate_content(refinePrompt)
    return response.text


def separate_bullet_and_description(refined_text):
    parts = refined_text.split("~")
    bullet = parts[0].strip().split("\n")[-1]  # Get the last line of the first part
    description = parts[1].strip()
    return bullet, description
