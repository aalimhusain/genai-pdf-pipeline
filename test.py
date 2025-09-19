from transformers import pipeline

# Initialize summarizer
summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

# Sample text
text = "Hugging Face provides machine learning tools and is known for the Transformers library."

# Generate summary
summary = summarizer(text, max_length=50, min_length=10, do_sample=False)

# Print the summary
print(summary)