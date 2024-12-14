from config import model

essay_whtbd = """
What Had to Be Done

At six years old, I stood locked away in the restroom. I held tightly to a tube of toothpaste because I’d been sent to brush my teeth to distract me from the commotion. Regardless, I knew what was happening: my dad was being put under arrest for domestic abuse. He’d hurt my mom physically and mentally, and my brother Jose and I had shared the mental strain. It’s what had to be done.

Living without a father meant money was tight, mom worked two jobs, and my brother and I took care of each other when she worked. For a brief period of time the quality of our lives slowly started to improve as our soon-to-be step-dad became an integral part of our family. He paid attention to the needs of my mom, my brother, and me. But our prosperity was short-lived as my step dad’s chronic alcoholism became more and more recurrent. When I was eight, my younger brother Fernando’s birth complicated things even further. As my step-dad slipped away, my mom continued working, and Fernando’s care was left to Jose and me. I cooked, Jose cleaned, I dressed Fernando, Jose put him to bed. We did what we had to do.

As undocumented immigrants and with little to no family around us, we had to rely on each other. Fearing that any disclosure of our status would risk deportation, we kept to ourselves when dealing with any financial and medical issues. I avoided going on certain school trips, and at times I was discouraged to even meet new people. I felt isolated and at times disillusioned; my grades started to slip.

Over time, however, I grew determined to improve the quality of life for my family and myself.

Without a father figure to teach me the things a father could, I became my own teacher. I learned how to fix a bike, how to swim, and even how to talk to girls. I became resourceful, fixing shoes with strips of duct tape, and I even found a job to help pay bills. I became as independent as I could to lessen the time and money mom had to spend raising me.

 I also worked to apply myself constructively in other ways. I worked hard and took my grades from Bs and Cs to consecutive straight A’s. I shattered my school’s 1ooM breaststroke record, and learned how to play the clarinet, saxophone, and the oboe. Plus, I not only became the first student in my school to pass the AP Physics 1 exam, I’m currently pioneering my school’s first AP Physics 2 course ever.

These changes inspired me to help others. I became president of the California Scholarship Federation, providing students with information to prepare them for college, while creating opportunities for my peers to play a bigger part in our community. I began tutoring kids, teens, and adults on a variety of subjects ranging from basic English to home improvement and even Calculus. As the captain of the water polo and swim team I’ve led practices crafted to individually push my comrades to their limits, and I’ve counseled friends through circumstances similar to mine. I’ve done tons, and I can finally say I’m proud of that.

But I’m excited to say that there’s so much I have yet to do. I haven’t danced the tango, solved a Rubix Cube, explored how perpetual motion might fuel space exploration, or seen the World Trade Center. And I have yet to see the person that Fernando will become.

I’ll do as much as I can from now on. Not because I have to. Because I choose to.
"""


def generate_tell_us_about_you_essay_prompt(userInput):
    essayPrompt = f"""
    <OBJECTIVE_AND_PERSONA>
    You are an expert in writing compelling and impactful scholarship essays. Your task is to help a student write a "Tell Us About You" essay for a scholarship application. The essay should provide a detailed, engaging, and personal narrative that effectively answers the prompt.
    </OBJECTIVE_AND_PERSONA>

    <INSTRUCTIONS>
    To complete the task, follow these steps:
    1. Start by identifying a significant personal experience or story that reveals important aspects of the student's background, personality, and aspirations.
    2. Use descriptive language and specific details to paint a vivid picture of the experience and its impact.
    3. Highlight personal growth, challenges overcome, and the student's contributions to their community or field.
    4. Conclude with a forward-looking statement that shows the student's ambitions and how they plan to use their experiences to achieve future goals.
    5. Ensure the essay is well-structured, coherent, and stays within the word limit (typically 500-700 words).
    </INSTRUCTIONS>

    <CONSTRAINTS>
    Please adhere to the following dos and don'ts:
    1. Do: Use specific and vivid details to bring the story to life.
    2. Do: Reflect on personal growth and learning.
    3. Don’t: Include irrelevant or overly generalized information.
    4. Don’t: Use clichés or overly dramatic language.
    </CONSTRAINTS>

    <CONTEXT>
    Here is the context you need to know:
    - The "Tell Us About You" prompt is an open-ended question designed to learn more about the student's background, experiences, and personal growth.
    - This essay can often overlap with personal statements or other scholarship prompts, so it’s useful to create a versatile draft.
    </CONTEXT>

    <OUTPUT_FORMAT>
    The output should be formatted as follows:
    1. An essay of 500-700 words.
    2. The essay should include an engaging introduction, a detailed body that narrates the experience and reflects on personal growth, and a forward-looking conclusion.
    </OUTPUT_FORMAT>

    <FEW_SHOT_EXAMPLES>
    Here are some examples to guide your responses:

    Example #1:
    Input:
    - Personal experience: Overcoming family challenges and excelling in school despite adversities
    - Details: Domestic abuse, taking care of siblings, achieving academic success, leading community initiatives
    Thoughts: This essay should highlight resilience, responsibility, and leadership.
    Output:
    {essay_whtbd}

    </FEW_SHOT_EXAMPLES>

    <RECAP>
    To summarize, remember the key points:
    1. Use specific, vivid details and descriptive language.
    2. Reflect on personal growth and challenges overcome.
    3. Keep the essay well-structured and within the word limit.
    </RECAP>

    Now, let's start crafting your essay. Process this: {userInput}
    """

    return essayPrompt
