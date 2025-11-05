# Static Site Generator

**A lightweight static site generator built from scratch in Python that transforms Markdown files into beautiful, responsive HTML websites.**

---

## Architecture
![architecture](https://github.com/user-attachments/assets/549b95cd-8c3f-4187-a4e0-1e33e5188c42)

## The flow of data through the full system is:

- Markdown files are in the ```/content``` directory. A ```template.html``` file is in the root of the project.
- The static site generator (the Python code in ```src/```) reads the Markdown files and the template file.
- The generator converts the Markdown files to a final HTML file for each page and writes them to the /docs directory.
- Start the built-in Python HTTP server (a separate program, unrelated to the generator) to serve the contents of the ```/docs``` directory on ```http://localhost:8888``` (local machine).
- Open a browser and navigate to ```http://localhost:8888``` to view the rendered site.

## How the SSG Works

- Delete everything in the ```/docs``` directory.
- Copy any static assets (HTML template, images, CSS, etc.) to the ```/docs``` directory.
- Generate an HTML file for each Markdown file in the ```/content``` directory. For each Markdown file:
  - Open the file and read its contents.
  - Split the markdown into "blocks" (e.g. paragraphs, headings, lists, etc.).
  - Convert each block into a tree of ```HTMLNode``` objects. For inline elements (like bold text, links, etc.) we will convert:
      - Raw markdown -> ```TextNode``` -> ```HTMLNode```
  - Join all the ```HTMLNode``` blocks under one large parent ```HTMLNode``` for the pages.
  - Use a recursive ```to_html()``` method to convert the ```HTMLNode``` and all its nested nodes to a giant HTML string and inject it in the HTML template.
  - Write the full HTML string to a file for that page in the ```/docs``` directory.
