import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import threading
from bs4 import BeautifulSoup
import requests
import os
import time

class ImageScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("HTML Image Scraper")
        self.root.geometry("800x600")
        self.root.minsize(600, 500)
        
        # Create frames
        self.main_frame = tk.Frame(self.root, padx=10, pady=10)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # HTML Input section
        tk.Label(self.main_frame, text="Enter HTML with image tags:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        self.html_text = scrolledtext.ScrolledText(self.main_frame, height=15, wrap=tk.WORD)
        self.html_text.pack(fill=tk.BOTH, expand=True, pady=(5, 10))
        
        # Output directory selection
        self.dir_frame = tk.Frame(self.main_frame)
        self.dir_frame.pack(fill=tk.X, pady=(5, 10))
        
        tk.Label(self.dir_frame, text="Output Directory:").pack(side=tk.LEFT)
        
        self.dir_var = tk.StringVar()
        self.dir_entry = tk.Entry(self.dir_frame, textvariable=self.dir_var, width=50)
        self.dir_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(5, 5))
        
        self.browse_btn = tk.Button(self.dir_frame, text="Browse...", command=self.browse_directory)
        self.browse_btn.pack(side=tk.RIGHT)
        
        # Image class selector
        self.class_frame = tk.Frame(self.main_frame)
        self.class_frame.pack(fill=tk.X, pady=(0, 10))
        
        tk.Label(self.class_frame, text="Image Class (optional):").pack(side=tk.LEFT)
        
        self.class_var = tk.StringVar(value="origin_image")
        self.class_entry = tk.Entry(self.class_frame, textvariable=self.class_var, width=20)
        self.class_entry.pack(side=tk.LEFT, padx=(5, 0))
        
        # Action buttons
        self.button_frame = tk.Frame(self.main_frame)
        self.button_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.download_btn = tk.Button(self.button_frame, text="Download Images", command=self.start_download, bg="#4CAF50", fg="white", height=2)
        self.download_btn.pack(fill=tk.X)
        
        # Log output
        tk.Label(self.main_frame, text="Download Progress:", font=("Arial", 10, "bold")).pack(anchor=tk.W)
        
        self.log_text = scrolledtext.ScrolledText(self.main_frame, height=10, wrap=tk.WORD)
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=(5, 0))
        
        # Set default directory to desktop
        desktop = os.path.join(os.path.expanduser("~"), "Desktop")
        self.dir_var.set(desktop)

    def browse_directory(self):
        dir_path = filedialog.askdirectory()
        if dir_path:
            self.dir_var.set(dir_path)

    def log(self, message):
        self.log_text.insert(tk.END, message + "\n")
        self.log_text.see(tk.END)
        self.log_text.update_idletasks()

    def start_download(self):
        # Clear log
        self.log_text.delete(1.0, tk.END)
        
        # Get inputs
        html_string = self.html_text.get(1.0, tk.END)
        target_dir = self.dir_var.get()
        img_class = self.class_var.get()
        
        if not html_string.strip():
            messagebox.showerror("Error", "Please enter HTML content")
            return
            
        if not target_dir:
            messagebox.showerror("Error", "Please select an output directory")
            return
            
        # Disable download button during process
        self.download_btn.config(state=tk.DISABLED, text="Downloading...")
            
        # Start download in a separate thread to keep UI responsive
        threading.Thread(target=self.download_images, args=(html_string, target_dir, img_class), daemon=True).start()

    def download_images(self, html_string, target_dir, img_class):
        try:
            # Ensure the target directory exists
            if not os.path.exists(target_dir):
                try:
                    os.makedirs(target_dir)
                    self.log(f"Created directory: {target_dir}")
                except Exception as e:
                    self.log(f"Failed to create directory {target_dir}: {e}")
                    self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to create directory: {e}"))
                    self.root.after(0, lambda: self.download_btn.config(state=tk.NORMAL, text="Download Images"))
                    return

            # Parse the HTML with BeautifulSoup
            soup = BeautifulSoup(html_string, 'html.parser')

            # Find images based on class if provided, otherwise get all images
            if img_class:
                imgs = soup.find_all('img', class_=img_class)
                self.log(f"Found {len(imgs)} images with class '{img_class}'")
            else:
                imgs = soup.find_all('img')
                self.log(f"Found {len(imgs)} images in the HTML")

            if not imgs:
                self.log("No images found to download!")
                self.root.after(0, lambda: self.download_btn.config(state=tk.NORMAL, text="Download Images"))
                return

            # Set headers to mimic a browser
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'
            }

            # Download each image with retry mechanism
            successful = 0
            for i, img in enumerate(imgs, 1):
                try:
                    # Use 'data-original' or 'src' depending on the HTML structure
                    url = img.get('data-original') or img.get('src')
                    
                    if not url:
                        self.log(f"Image {i}: No URL found in the image tag")
                        continue
                    
                    # Clean URL if needed
                    if url.startswith('//'):
                        url = 'https:' + url
                        
                    filename = f"{i}.jpg"
                    file_path = os.path.join(target_dir, filename)
                    self.log(f"Downloading image {i}: {url}")
                    
                    # Retry up to 3 times if download fails
                    for attempt in range(3):
                        try:
                            response = requests.get(url, headers=headers, timeout=10)
                            if response.status_code == 200:
                                with open(file_path, 'wb') as f:
                                    f.write(response.content)
                                self.log(f"Saved {filename} to {target_dir}")
                                successful += 1
                                break
                            else:
                                self.log(f"Failed to download {url}, status code: {response.status_code}")
                        except requests.exceptions.RequestException as e:
                            self.log(f"Attempt {attempt+1} failed: {e}")
                            time.sleep(2)  # Wait before retrying
                    else:
                        self.log(f"Failed to download {url} after 3 attempts.")
                except Exception as e:
                    self.log(f"Error processing image {i}: {e}")
            
            self.log(f"\nDownload complete. Successfully downloaded {successful} of {len(imgs)} images.")
            
        except Exception as e:
            self.log(f"An error occurred: {e}")
        finally:
            # Re-enable download button
            self.root.after(0, lambda: self.download_btn.config(state=tk.NORMAL, text="Download Images"))

if __name__ == "__main__":
    root = tk.Tk()
    app = ImageScraperApp(root)
    root.mainloop()