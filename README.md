1. Clone repo
2. `uv sync`
3. `uv run pdf2img.py <pfds_location> <saving_location>` 

Note : if you want to add metadata to you images (by default only the pdf source and the page number), you can amend main() in pdf2img.py. you can follow the examples there with --author, --project and --department