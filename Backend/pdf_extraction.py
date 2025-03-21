from docling.document_converter import DocumentConverter

# Source PDF path
source = "/Users/janvichitroda/Documents/Janvi/NEU/Big_Data_Intelligence_Analytics/Assignment 4/Part1_Janvi/PDF_Summarizer_QnA/InputFiles/input.pdf"

# Create a DocumentConverter instance
converter = DocumentConverter()

# Convert the document
result = converter.convert(source)

# Get the markdown content from the converted document
markdown_content = result.document.export_to_markdown()

# Define the output markdown file path
output_md_path = "/Users/janvichitroda/Documents/Janvi/NEU/Big_Data_Intelligence_Analytics/Assignment 4/Part1_Janvi/PDF_Summarizer_QnA/OutputFiles/output.md"

# Write the markdown content to the output file
with open(output_md_path, 'w') as md_file:
    md_file.write(markdown_content)

print(f"Markdown file has been saved to: {output_md_path}")
