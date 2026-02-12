Jungian Dream Visualizer - Project Report
Live Demo: https://cart498-a04.onrender.com
GitHub Repository: https://github.com/jercabaneros/CART498_A04

Implementation Report

Implementing Jungian Psychology in AI Prompts

The core challenge of this project was translating Carl Jung's complex psychological theories into effective prompts that could guide AI models to think like a Jungian analyst. For the dream interpretation, I designed a system prompt that explicitly references Jung's key concepts: archetypes, the shadow, anima/animus, symbols, the collective unconscious, and individuation. This approach works because it gives GPT-4 a specific analytical framework rather than letting it default to generic dream interpretation. The prompt instructs the model to identify archetypal figures like the Wise Old Man or the Great Mother, recognize how dreams compensate for one-sided conscious attitudes, and explore symbolic meanings that connect to humanity's shared psychological inheritance. I found that keeping the prompt concise but comprehensive was crucial—longer prompts made the AI too complicated, while shorter ones lost the Jungian specificity.

For image generation, I crafted prompts that transform dream narratives into symbolic visual representations. The key was using language like "surreal, dreamlike, symbolic artistic representation" and explicitly mentioning "Jungian psychology" to bias the model toward archetypal, mythological imagery rather than literal interpretations. I also added "mystical, cosmic, constellation-like elements" to align with Jung's concept of the collective unconscious—the idea that dreams connect us to something larger than our individual experience. The cosmic theme in the application's design reinforces this concept, with animated stars representing the countless archetypal symbols floating in humanity's shared psychological space.
User Guide

Using the application is straightforward. Users visit the web app and describe their dream in the text area, including as much detail as possible about people, settings, emotions, and specific symbols. After clicking "Analyze Dream," the system generates both a Jungian interpretation and a visual representation. The text analysis appears first, followed by the AI-generated image after 15-30 seconds. For best results, users should provide at least 20 characters of description and include emotional content, as Jung emphasized the importance of feelings in dream work.
Reflection and Insights

One significant insight I gained is that free hosting services like Render have strict memory and timeout limitations that directly impact what you can deploy. Initially, for personal reasons, I used gpt-4 with high-resolution images, which caused the server to crash with "Worker was sent SIGKILL! Perhaps out of memory?" log errors. After an hour of debugging, I realized the issue wasn't my code, it was Render's free tier killing processes that consumed too much RAM or took too long. The solution was implementing a fallback system that tries different models in sequence and reducing image resolution to 512x512. This taught me that production environments require thinking beyond "does it work on my laptop?" you need to design for the constraints of your deployment platform.

Another challenge was mastering the OpenAI API. My initial implementation used non-existent methods and incorrect parameter names, which led to cryptic error messages. Reading the official documentation carefully and testing each endpoint separately made all the difference. It's a reminder that assuming you know how an API works versus actually reading the docs can cost you hours of debugging time. If I could improve this project, I'd add a dream journal feature for tracking error patterns over time and upgrade to paid hosting to support higher-quality image generation without timeout constraints.

Author: Jerwin Cabaneros
Course: CART 498 - Assignment 04
Date: Winter 2026
