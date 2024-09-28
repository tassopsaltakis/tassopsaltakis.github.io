import tkinter as tk
from tkinter import messagebox
import json
import os

# Define the path to your JSON file for storing blog posts
BLOG_FILE_PATH = 'blog_posts.json'  # Replace with the actual path if needed


class BlogPostApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tasso's Blog Post Creator")

        # Title label and entry
        self.title_label = tk.Label(root, text="Post Title:")
        self.title_label.pack()
        self.title_entry = tk.Entry(root, width=50)
        self.title_entry.pack()

        # Content label and text area
        self.content_label = tk.Label(root, text="Post Content:")
        self.content_label.pack()
        self.content_text = tk.Text(root, height=10, width=50)
        self.content_text.pack()

        # Submit button
        self.submit_button = tk.Button(root, text="Submit Post", command=self.submit_post)
        self.submit_button.pack()

        # Load existing posts
        self.load_posts()

    def load_posts(self):
        if os.path.exists(BLOG_FILE_PATH):
            with open(BLOG_FILE_PATH, 'r') as blog_file:
                try:
                    self.posts = json.load(blog_file)
                except json.JSONDecodeError:
                    self.posts = []
        else:
            self.posts = []

    def submit_post(self):
        title = self.title_entry.get()
        content = self.content_text.get("1.0", tk.END)

        if not title or not content.strip():
            messagebox.showerror("Error", "Title and content cannot be empty.")
            return

        # Create a new post entry
        new_post = {
            'title': title,
            'content': content.strip(),
            'date': self.get_current_date()
        }

        # Append the new post to the posts list
        self.posts.append(new_post)

        # Save posts to the JSON file
        with open(BLOG_FILE_PATH, 'w') as blog_file:
            json.dump(self.posts, blog_file, indent=4)

        messagebox.showinfo("Success", "Post added! Now push to GitHub using GitHub Desktop.")
        self.clear_entries()

    def clear_entries(self):
        self.title_entry.delete(0, tk.END)
        self.content_text.delete("1.0", tk.END)

    def get_current_date(self):
        from datetime import datetime
        return datetime.now().strftime("%Y-%m-%d")


if __name__ == "__main__":
    root = tk.Tk()
    app = BlogPostApp(root)
    root.mainloop()
