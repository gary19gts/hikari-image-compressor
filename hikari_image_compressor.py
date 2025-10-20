#!/usr/bin/env python3
"""
Hikari Image Compressor
Version: 1.1.0 stable
Date: September 2025
Author: Gary19gts

Modern image compressor with Apple-style GUI

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <https://www.gnu.org/licenses/>.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import customtkinter as ctk
from PIL import Image, ImageTk, ImageDraw
import os
import sys
import threading
from pathlib import Path
import io
import webbrowser

# Set appearance mode and color theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

# Configure colors for Apple-like appearance
COLORS = {
    'bg_primary': '#FFFFFF',
    'bg_secondary': '#F8F9FA',
    'bg_card': '#FFFFFF',
    'text_primary': '#1D1D1F',
    'text_secondary': '#86868B',
    'accent': '#007AFF',
    'border': '#E5E5E7',
    'success': '#34C759',
    'warning': '#FF9500',
    'error': '#FF3B30'
}

class ImageCompressor:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("Hikari Image Compressor")
        self.root.geometry("1280x750")
        self.root.minsize(800, 650)
        
        # Set application icon
        self.create_app_icon()
        
        # Variables
        self.loaded_images = []
        self.output_folder = tk.StringVar()
        self.quality_var = tk.StringVar(value="High (80%)")
        self.engine_var = tk.StringVar(value="Pillow")
        self.format_var = tk.StringVar(value="JPEG")
        self.resize_enabled = tk.BooleanVar(value=False)
        self.resize_scale = tk.StringVar(value="50")
        
        # Bind quality change to update previews
        self.quality_var.trace('w', self.on_settings_change)
        self.format_var.trace('w', self.on_settings_change)
        self.resize_enabled.trace('w', self.on_settings_change)
        
        self.setup_ui()
    
    def create_app_icon(self):
        """Create a minimalist blue icon for the application"""
        try:
            # Create a 64x64 icon with PIL
            icon_size = 64
            icon = Image.new('RGBA', (icon_size, icon_size), (0, 0, 0, 0))
            
            # Create a simple minimalist icon - a blue circle with a white image symbol
            draw = ImageDraw.Draw(icon)
            
            # Blue circle background
            margin = 4
            draw.ellipse([margin, margin, icon_size-margin, icon_size-margin], 
                        fill='#007AFF', outline='#0056CC', width=2)
            
            # White image/photo symbol in the center
            center = icon_size // 2
            # Mountain shape
            points = [
                (center-12, center+8),  # bottom left
                (center-8, center-2),   # peak 1
                (center-2, center+2),   # valley
                (center+6, center-8),   # peak 2
                (center+12, center+8),  # bottom right
            ]
            draw.polygon(points, fill='white')
            
            # Sun/circle in top right
            draw.ellipse([center+4, center-8, center+8, center-4], fill='white')
            
            # Convert to PhotoImage and set as icon
            photo = ImageTk.PhotoImage(icon)
            self.root.iconphoto(True, photo)
            
        except Exception as e:
            print(f"Could not create icon: {e}")
        
    def setup_ui(self):
        # Configure root window
        self.root.configure(fg_color=COLORS['bg_primary'])
        
        # Main container
        main_frame = ctk.CTkFrame(self.root, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Create two columns
        left_column = ctk.CTkFrame(
            main_frame, 
            width=420, 
            corner_radius=15,
            fg_color=COLORS['bg_card'],
            border_width=1,
            border_color=COLORS['border']
        )
        left_column.pack(side="left", fill="both", expand=False, padx=(0, 10))
        left_column.pack_propagate(False)
        
        right_column = ctk.CTkFrame(
            main_frame, 
            corner_radius=15,
            fg_color=COLORS['bg_card'],
            border_width=1,
            border_color=COLORS['border']
        )
        right_column.pack(side="right", fill="both", expand=True)
        
        self.setup_left_column(left_column)
        self.setup_right_column(right_column)
        
    def setup_left_column(self, parent):
        # Title
        title_label = ctk.CTkLabel(
            parent, 
            text="Hikari Image Compressor",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(pady=(20, 10))
        
        # Load Images Section
        load_frame = ctk.CTkFrame(
            parent, 
            corner_radius=10,
            fg_color=COLORS['bg_secondary'],
            border_width=1,
            border_color=COLORS['border']
        )
        load_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        load_title = ctk.CTkLabel(
            load_frame,
            text="Load Images",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLORS['text_primary']
        )
        load_title.pack(pady=(15, 10))
        
        load_btn = ctk.CTkButton(
            load_frame,
            text="Select Images",
            command=self.load_images,
            height=35,
            corner_radius=8,
            fg_color=COLORS['accent'],
            hover_color="#0056CC"
        )
        load_btn.pack(pady=(0, 15))
        
        # Settings Section
        settings_frame = ctk.CTkFrame(
            parent, 
            corner_radius=10,
            fg_color=COLORS['bg_secondary'],
            border_width=1,
            border_color=COLORS['border']
        )
        settings_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        settings_title = ctk.CTkLabel(
            settings_frame,
            text="Compression Settings",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLORS['text_primary']
        )
        settings_title.pack(pady=(15, 10))
        
        # Quality selector with info button
        quality_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        quality_frame.pack(fill="x", padx=15, pady=5)
        
        quality_label = ctk.CTkLabel(
            quality_frame, 
            text="Quality:",
            text_color=COLORS['text_primary']
        )
        quality_label.pack(side="left")
        
        quality_info_btn = ctk.CTkButton(
            quality_frame,
            text="i",
            width=25,
            height=25,
            corner_radius=12,
            command=lambda: self.show_info("quality"),
            fg_color=COLORS['text_secondary'],
            hover_color=COLORS['accent']
        )
        quality_info_btn.pack(side="right")
        
        quality_menu = ctk.CTkOptionMenu(
            quality_frame,
            values=["Low (30%)", "Medium (60%)", "High (80%)", "Maximum (95%)"],
            variable=self.quality_var,
            width=200,
            fg_color=COLORS['bg_card'],
            button_color=COLORS['accent'],
            button_hover_color="#0056CC",
            text_color=COLORS['text_primary'],
            font=ctk.CTkFont(size=12, weight="bold")
        )
        quality_menu.pack(side="right", padx=(0, 10))
        
        # Format selector with info button
        format_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        format_frame.pack(fill="x", padx=15, pady=5)
        
        format_label = ctk.CTkLabel(
            format_frame, 
            text="Format:",
            text_color=COLORS['text_primary']
        )
        format_label.pack(side="left")
        
        format_info_btn = ctk.CTkButton(
            format_frame,
            text="i",
            width=25,
            height=25,
            corner_radius=12,
            command=lambda: self.show_info("format"),
            fg_color=COLORS['text_secondary'],
            hover_color=COLORS['accent']
        )
        format_info_btn.pack(side="right")
        
        format_menu = ctk.CTkOptionMenu(
            format_frame,
            values=["JPEG", "WebP", "PNG"],
            variable=self.format_var,
            width=200,
            fg_color=COLORS['bg_card'],
            button_color=COLORS['accent'],
            button_hover_color="#0056CC",
            text_color=COLORS['text_primary'],
            font=ctk.CTkFont(size=12, weight="bold")
        )
        format_menu.pack(side="right", padx=(0, 10))
        
        # Engine selector with info button
        engine_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
        engine_frame.pack(fill="x", padx=15, pady=(5, 15))
        
        engine_label = ctk.CTkLabel(
            engine_frame, 
            text="Engine:",
            text_color=COLORS['text_primary']
        )
        engine_label.pack(side="left")
        
        engine_info_btn = ctk.CTkButton(
            engine_frame,
            text="i",
            width=25,
            height=25,
            corner_radius=12,
            command=lambda: self.show_info("engine"),
            fg_color=COLORS['text_secondary'],
            hover_color=COLORS['accent']
        )
        engine_info_btn.pack(side="right")
        
        engine_menu = ctk.CTkOptionMenu(
            engine_frame,
            values=["Pillow", "Imageio"],
            variable=self.engine_var,
            width=200,
            fg_color=COLORS['bg_card'],
            button_color=COLORS['accent'],
            button_hover_color="#0056CC",
            text_color=COLORS['text_primary'],
            font=ctk.CTkFont(size=12, weight="bold")
        )
        engine_menu.pack(side="right", padx=(0, 10))
        
        # Resize Section
        resize_frame = ctk.CTkFrame(
            parent, 
            corner_radius=10,
            fg_color=COLORS['bg_secondary'],
            border_width=1,
            border_color=COLORS['border']
        )
        resize_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        # Resize header with checkbox
        resize_header_frame = ctk.CTkFrame(resize_frame, fg_color="transparent")
        resize_header_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        self.resize_checkbox = ctk.CTkCheckBox(
            resize_header_frame,
            text="Resize Images",
            variable=self.resize_enabled,
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLORS['text_primary'],
            command=self.toggle_resize_options
        )
        self.resize_checkbox.pack(side="left")
        
        resize_info_btn = ctk.CTkButton(
            resize_header_frame,
            text="i",
            width=25,
            height=25,
            corner_radius=12,
            command=lambda: self.show_info("resize"),
            fg_color=COLORS['text_secondary'],
            hover_color=COLORS['accent']
        )
        resize_info_btn.pack(side="right")
        
        # Resize options frame (initially hidden)
        self.resize_options_frame = ctk.CTkFrame(resize_frame, fg_color="transparent")
        
        # Scale/Percentage frame
        scale_frame = ctk.CTkFrame(self.resize_options_frame, fg_color="transparent")
        scale_frame.pack(fill="x", padx=15, pady=(5, 10))
        
        scale_label = ctk.CTkLabel(
            scale_frame, 
            text="Scale:",
            text_color=COLORS['text_primary']
        )
        scale_label.pack(side="left")
        
        self.scale_entry = ctk.CTkEntry(
            scale_frame,
            textvariable=self.resize_scale,
            width=80,
            height=30
        )
        self.scale_entry.pack(side="left", padx=(10, 5))
        
        scale_unit_label = ctk.CTkLabel(
            scale_frame, 
            text="%",
            text_color=COLORS['text_primary']
        )
        scale_unit_label.pack(side="left", padx=(5, 0))
        
        # Initially hide resize options
        self.toggle_resize_options()
        
        # Output folder section
        output_frame = ctk.CTkFrame(
            parent, 
            corner_radius=10,
            fg_color=COLORS['bg_secondary'],
            border_width=1,
            border_color=COLORS['border']
        )
        output_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        output_title = ctk.CTkLabel(
            output_frame,
            text="Output Folder",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLORS['text_primary']
        )
        output_title.pack(pady=(15, 10))
        
        # Buttons frame for output folder actions
        output_buttons_frame = ctk.CTkFrame(output_frame, fg_color="transparent")
        output_buttons_frame.pack(pady=(0, 10))
        
        output_btn = ctk.CTkButton(
            output_buttons_frame,
            text="Select Output Folder",
            command=self.select_output_folder,
            height=35,
            width=140,
            corner_radius=8,
            fg_color=COLORS['accent'],
            hover_color="#0056CC"
        )
        output_btn.pack(side="left", padx=(0, 8))
        
        self.open_folder_btn = ctk.CTkButton(
            output_buttons_frame,
            text="📁 Open Folder",
            command=self.open_output_folder,
            height=35,
            width=110,
            corner_radius=8,
            fg_color=COLORS['text_secondary'],
            hover_color=COLORS['accent']
        )
        self.open_folder_btn.pack(side="left")
        
        self.output_label = ctk.CTkLabel(
            output_frame,
            text="Same as source folder",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['text_secondary']
        )
        self.output_label.pack(pady=(5, 15))
        
        # Compress button
        compress_btn = ctk.CTkButton(
            parent,
            text="Start Compression",
            command=self.start_compression,
            height=45,
            font=ctk.CTkFont(size=16, weight="bold"),
            corner_radius=10,
            fg_color=COLORS['success'],
            hover_color="#28A745"
        )
        compress_btn.pack(fill="x", padx=20, pady=(0, 10))
        
        # Progress bar
        self.progress = ctk.CTkProgressBar(parent)
        self.progress.pack(fill="x", padx=20, pady=(0, 10))
        self.progress.set(0)
        

        
    def setup_right_column(self, parent):
        # Preview header with title and clear button
        header_frame = ctk.CTkFrame(parent, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        preview_title = ctk.CTkLabel(
            header_frame,
            text="Image Preview",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=COLORS['text_primary']
        )
        preview_title.pack(side="left")
        
        self.clear_btn = ctk.CTkButton(
            header_frame,
            text="Clear All",
            command=self.clear_images,
            height=30,
            width=80,
            corner_radius=8,
            fg_color=COLORS['error'],
            hover_color="#CC2E24"
        )
        self.clear_btn.pack(side="right")
        self.clear_btn.pack_forget()  # Hide initially
        
        # Scrollable frame for images (reduced height)
        self.preview_frame = ctk.CTkScrollableFrame(
            parent, 
            corner_radius=10,
            fg_color=COLORS['bg_secondary'],
            border_width=1,
            border_color=COLORS['border'],
            height=350
        )
        self.preview_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        # Initial message (centered)
        self.no_images_label = ctk.CTkLabel(
            self.preview_frame,
            text="No images loaded\nClick 'Select Images' to get started",
            font=ctk.CTkFont(size=14),
            text_color=COLORS['text_secondary']
        )
        self.no_images_label.pack(expand=True, pady=(120, 0))
        
        # Support Development section
        support_frame = ctk.CTkFrame(
            parent, 
            corner_radius=10,
            fg_color=COLORS['bg_card'],
            border_width=1,
            border_color=COLORS['border']
        )
        support_frame.pack(fill="x", padx=20, pady=(0, 10))
        
        # Support header with emoji
        support_header_frame = ctk.CTkFrame(support_frame, fg_color="transparent")
        support_header_frame.pack(fill="x", padx=20, pady=(12, 5))
        
        support_title = ctk.CTkLabel(
            support_header_frame,
            text="🤝 Support Development",
            font=ctk.CTkFont(size=16, weight="bold"),
            text_color=COLORS['text_primary']
        )
        support_title.pack()
        
        # Support description
        support_desc = ctk.CTkLabel(
            support_frame,
            text="If you find Hikari useful, consider supporting its development!",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['text_secondary']
        )
        support_desc.pack(pady=(0, 8))
        
        # Ko-fi button (large and prominent)
        kofi_btn = ctk.CTkButton(
            support_frame,
            text="☕ Buy me a coffee on Ko-fi",
            command=lambda: webbrowser.open("https://ko-fi.com/gary19gts"),
            height=45,
            corner_radius=10,
            fg_color="#FF5E5B",
            hover_color="#E04E4B",
            text_color="white",
            font=ctk.CTkFont(size=14, weight="bold")
        )
        kofi_btn.pack(fill="x", padx=20, pady=(0, 6))
        
        # Thank you message
        thank_you_label = ctk.CTkLabel(
            support_frame,
            text="Thank you for your support! 🖤",
            font=ctk.CTkFont(size=11),
            text_color=COLORS['text_secondary']
        )
        thank_you_label.pack(pady=(0, 12))
        
        # Credits section (single line)
        credits_frame = ctk.CTkFrame(
            parent, 
            corner_radius=10,
            fg_color=COLORS['bg_secondary'],
            border_width=1,
            border_color=COLORS['border']
        )
        credits_frame.pack(fill="x", padx=20, pady=(5, 20))
        
        # Credits content in horizontal layout
        credits_content_frame = ctk.CTkFrame(credits_frame, fg_color="transparent")
        credits_content_frame.pack(fill="x", padx=15, pady=12)
        
        credits_text = ctk.CTkLabel(
            credits_content_frame,
            text="Hikari Image Compressor v1.1.0 • Created by Gary19gts",
            font=ctk.CTkFont(size=12),
            text_color=COLORS['text_primary']
        )
        credits_text.pack(side="left")
        
        # Buttons on the right
        buttons_frame = ctk.CTkFrame(credits_content_frame, fg_color="transparent")
        buttons_frame.pack(side="right")
        
        about_btn = ctk.CTkButton(
            buttons_frame,
            text="About",
            command=self.show_about,
            height=40,
            width=75,
            corner_radius=8,
            fg_color=COLORS['accent'],
            hover_color="#0056CC",
            font=ctk.CTkFont(size=12)
        )
        about_btn.pack(side="left", padx=(0, 8))
        
        credits_btn = ctk.CTkButton(
            buttons_frame,
            text="Credits",
            command=self.show_credits,
            height=40,
            width=75,
            corner_radius=8,
            fg_color=COLORS['text_secondary'],
            hover_color=COLORS['accent'],
            font=ctk.CTkFont(size=12)
        )
        credits_btn.pack(side="left") 
       
    def load_images(self):
        """Load images from file dialog"""
        filetypes = [
            ("Image files", "*.png *.jpg *.jpeg *.bmp *.tiff *.webp"),
            ("PNG files", "*.png"),
            ("JPEG files", "*.jpg *.jpeg"),
            ("All files", "*.*")
        ]
        
        files = filedialog.askopenfilenames(
            title="Select Images to Compress",
            filetypes=filetypes
        )
        
        if files:
            self.loaded_images = list(files)
            # Set default output folder to same as first image
            if not self.output_folder.get():
                self.output_folder.set(os.path.dirname(files[0]))
                self.output_label.configure(text=f"Output: {os.path.basename(self.output_folder.get())}")
            
            self.update_preview()
            self.clear_btn.pack(side="right")  # Show clear button
    
    def select_output_folder(self):
        """Select output folder"""
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder.set(folder)
            self.output_label.configure(text=f"Output: {os.path.basename(folder)}")
    
    def open_output_folder(self):
        """Open the output folder in file explorer"""
        output_dir = self.output_folder.get()
        
        # If no output folder is set, use the source folder of the first image
        if not output_dir and self.loaded_images:
            output_dir = os.path.dirname(self.loaded_images[0])
        
        if output_dir and os.path.exists(output_dir):
            try:
                # Open folder in file explorer (cross-platform)
                if os.name == 'nt':  # Windows
                    os.startfile(output_dir)
                elif os.name == 'posix':  # macOS and Linux
                    if sys.platform == 'darwin':  # macOS
                        os.system(f'open "{output_dir}"')
                    else:  # Linux
                        os.system(f'xdg-open "{output_dir}"')
            except Exception as e:
                messagebox.showerror("Error", f"Could not open folder: {e}")
        else:
            messagebox.showwarning("No Folder", "No output folder selected or folder doesn't exist.")
    
    def update_preview(self):
        """Update the preview panel with loaded images"""
        # Clear existing previews
        for widget in self.preview_frame.winfo_children():
            widget.destroy()
        
        if not self.loaded_images:
            self.no_images_label = ctk.CTkLabel(
                self.preview_frame,
                text="No images loaded\nClick 'Select Images' to get started",
                font=ctk.CTkFont(size=14),
                text_color=COLORS['text_secondary']
            )
            self.no_images_label.pack(expand=True, pady=(120, 0))
            self.clear_btn.pack_forget()  # Hide clear button
            return
        
        # Show loaded images
        for i, image_path in enumerate(self.loaded_images):
            self.create_image_preview(image_path, i)
    
    def create_image_preview(self, image_path, index):
        """Create a preview card for an image"""
        # Image card frame
        card_frame = ctk.CTkFrame(
            self.preview_frame, 
            corner_radius=10,
            fg_color=COLORS['bg_card'],
            border_width=1,
            border_color=COLORS['border']
        )
        card_frame.pack(fill="x", padx=10, pady=5)
        
        # Image info frame
        info_frame = ctk.CTkFrame(card_frame, fg_color="transparent")
        info_frame.pack(fill="x", padx=15, pady=10)
        
        try:
            # Load and resize image for thumbnail
            with Image.open(image_path) as img:
                # Calculate thumbnail size
                img.thumbnail((150, 150), Image.Resampling.LANCZOS)
                
                # Convert to PhotoImage
                photo = ImageTk.PhotoImage(img)
                
                # Image thumbnail
                img_label = tk.Label(info_frame, image=photo, bg=COLORS['bg_card'], bd=0)
                img_label.image = photo  # Keep a reference
                img_label.pack(side="left", padx=(0, 15))
                
                # Image details
                details_frame = ctk.CTkFrame(info_frame, fg_color="transparent")
                details_frame.pack(side="left", fill="both", expand=True)
                
                # File name
                filename = os.path.basename(image_path)
                name_label = ctk.CTkLabel(
                    details_frame,
                    text=filename,
                    font=ctk.CTkFont(size=14, weight="bold"),
                    anchor="w",
                    text_color=COLORS['text_primary']
                )
                name_label.pack(fill="x", pady=(0, 5))
                
                # File size
                file_size = os.path.getsize(image_path)
                size_text = self.format_file_size(file_size)
                
                # Get image dimensions
                original_img = Image.open(image_path)
                dimensions = f"{original_img.width}x{original_img.height}"
                
                size_label = ctk.CTkLabel(
                    details_frame,
                    text=f"Size: {size_text} • {dimensions}",
                    font=ctk.CTkFont(size=12),
                    text_color=COLORS['text_secondary'],
                    anchor="w"
                )
                size_label.pack(fill="x", pady=(0, 5))
                
                # Estimated compression (store reference for updates)
                estimated_size = self.estimate_compressed_size(file_size, original_img.width, original_img.height)
                compression_ratio = ((file_size - estimated_size) / file_size) * 100
                
                estimate_label = ctk.CTkLabel(
                    details_frame,
                    text=f"Estimated: {self.format_file_size(estimated_size)} ({compression_ratio:.1f}% reduction)",
                    font=ctk.CTkFont(size=12),
                    text_color=COLORS['success'],
                    anchor="w"
                )
                estimate_label.pack(fill="x")
                
                # Store reference for updating estimates
                estimate_label.original_size = file_size
                estimate_label.original_width = original_img.width
                estimate_label.original_height = original_img.height
                estimate_label.update_estimate = lambda: self.update_estimate_label(estimate_label)
                
                # Delete button (X) on the right side
                delete_btn = ctk.CTkButton(
                    info_frame,
                    text="✕",
                    width=30,
                    height=30,
                    corner_radius=15,
                    fg_color=COLORS['error'],
                    hover_color="#CC2E24",
                    font=ctk.CTkFont(size=16, weight="bold"),
                    command=lambda idx=index: self.remove_image(idx)
                )
                delete_btn.pack(side="right", padx=(10, 0))
                
        except Exception as e:
            # Error loading image
            error_label = ctk.CTkLabel(
                info_frame,
                text=f"Error loading: {os.path.basename(image_path)}",
                font=ctk.CTkFont(size=12),
                text_color=COLORS['error']
            )
            error_label.pack(pady=10)
    
    def format_file_size(self, size_bytes):
        """Format file size in human readable format"""
        if size_bytes < 1024:
            return f"{size_bytes} B"
        elif size_bytes < 1024 * 1024:
            return f"{size_bytes / 1024:.1f} KB"
        else:
            return f"{size_bytes / (1024 * 1024):.1f} MB"
    
    def estimate_compressed_size(self, original_size, original_width=None, original_height=None):
        """Estimate compressed file size based on quality setting and resize options"""
        quality_map = {
            "Low (30%)": 0.3,
            "Medium (60%)": 0.5,
            "High (80%)": 0.7,
            "Maximum (95%)": 0.9
        }
        
        format_map = {
            "JPEG": 0.6,
            "WebP": 0.4,
            "PNG": 0.8
        }
        
        quality_factor = quality_map.get(self.quality_var.get(), 0.7)
        format_factor = format_map.get(self.format_var.get(), 0.6)
        
        # Calculate resize factor if dimensions are provided
        resize_factor = 1.0
        if self.resize_enabled.get() and original_width and original_height:
            new_width, new_height = self.calculate_resize_dimensions(original_width, original_height)
            original_pixels = original_width * original_height
            new_pixels = new_width * new_height
            resize_factor = new_pixels / original_pixels if original_pixels > 0 else 1.0
        
        return int(original_size * quality_factor * format_factor * resize_factor)
    
    def update_estimate_label(self, label):
        """Update estimate label with current settings"""
        width = getattr(label, 'original_width', None)
        height = getattr(label, 'original_height', None)
        estimated_size = self.estimate_compressed_size(label.original_size, width, height)
        compression_ratio = ((label.original_size - estimated_size) / label.original_size) * 100
        label.configure(text=f"Estimated: {self.format_file_size(estimated_size)} ({compression_ratio:.1f}% reduction)")
    
    def on_settings_change(self, *args):
        """Called when quality or format settings change"""
        # Update all estimate labels
        for widget in self.preview_frame.winfo_children():
            if hasattr(widget, 'winfo_children'):
                for child in widget.winfo_children():
                    if hasattr(child, 'winfo_children'):
                        for grandchild in child.winfo_children():
                            if hasattr(grandchild, 'winfo_children'):
                                for ggchild in grandchild.winfo_children():
                                    if hasattr(ggchild, 'update_estimate'):
                                        ggchild.update_estimate()
    
    def clear_images(self):
        """Clear all loaded images"""
        if not self.loaded_images:
            return
            
        # Show confirmation dialog
        result = messagebox.askyesno(
            "Clear All Images", 
            f"Are you sure you want to remove all {len(self.loaded_images)} images?",
            icon="warning"
        )
        
        if result:
            self.loaded_images = []
            self.update_preview()
    
    def remove_image(self, index):
        """Remove a specific image from the list"""
        if 0 <= index < len(self.loaded_images):
            self.loaded_images.pop(index)
            self.update_preview()
    
    def toggle_resize_options(self):
        """Toggle visibility of resize options"""
        if self.resize_enabled.get():
            self.resize_options_frame.pack(fill="x", pady=(0, 10))
        else:
            self.resize_options_frame.pack_forget()
    
    def calculate_resize_dimensions(self, original_width, original_height):
        """Calculate new dimensions based on resize settings"""
        if not self.resize_enabled.get():
            return original_width, original_height
        
        try:
            scale = float(self.resize_scale.get()) / 100.0
            new_width = int(original_width * scale)
            new_height = int(original_height * scale)
            return new_width, new_height
        except (ValueError, ZeroDivisionError):
            # Return original dimensions if there's an error
            return original_width, original_height
    
    def show_info(self, info_type):
        """Show information tooltips"""
        info_texts = {
            "quality": """Quality Settings:

• Low (30%): Smallest file size, noticeable quality loss
• Medium (60%): Good balance of size and quality
• High (80%): Excellent quality with good compression
• Maximum (95%): Best quality, minimal compression

💡 Tip: High (80%) is recommended for the best balance 
between excellent compression and good quality.""",
            
            "format": """Output Formats:

• JPEG: Best for photos, good compression, no transparency
• WebP: Modern format, excellent compression, supports transparency
• PNG: Lossless compression, supports transparency, larger files

💡 Tip: WebP offers the best compression while maintaining 
excellent quality for most use cases.""",
            
            "engine": """Compression Engines:

• Pillow: Fast, reliable, good for general use
• Imageio: Advanced options, better for specific formats

💡 Tip: Pillow is recommended for most users as it provides 
excellent compression with good performance.""",
            
            "resize": """Resize Options:

Scale images by percentage while maintaining aspect ratio:
• 50% = Half the original size
• 25% = Quarter the original size  
• 75% = Three-quarters the original size
• 100% = Original size (no change)

💡 Tip: Use 50% for web images, 25% for thumbnails, or 75% for 
moderate size reduction while keeping good quality."""
        }
        
        messagebox.showinfo("Information", info_texts.get(info_type, "No information available"))
    
    def show_about(self):
        """Show about dialog"""
        about_text = """Hikari Image Compressor v1.1.0 stable

A modern, user-friendly image compression tool with an Apple-style interface.

Created by: Gary19gts
License: GNU Affero General Public License v3.0
GitHub: https://github.com/Gary19gts/hikari-image-compressor

Features:
• Multiple format support (JPEG, WebP, PNG)
• Quality presets for easy compression
• Batch processing capabilities
• Real-time compression estimates
• Modern, intuitive interface

This software is free and open source. You can redistribute it and/or modify it under the terms of the AGPL v3 license."""
        
        messagebox.showinfo("About Hikari Image Compressor", about_text)
    
    def show_credits(self):
        """Show credits and acknowledgments dialog"""
        credits_window = ctk.CTkToplevel(self.root)
        credits_window.title("Credits & Acknowledgments")
        credits_window.geometry("600x500")
        credits_window.resizable(False, False)
        credits_window.transient(self.root)
        credits_window.grab_set()
        
        # Center the window
        credits_window.update_idletasks()
        x = (credits_window.winfo_screenwidth() // 2) - (600 // 2)
        y = (credits_window.winfo_screenheight() // 2) - (500 // 2)
        credits_window.geometry(f"600x500+{x}+{y}")
        
        # Main frame
        main_frame = ctk.CTkFrame(credits_window, fg_color="transparent")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Title
        title_label = ctk.CTkLabel(
            main_frame,
            text="Credits & Acknowledgments",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        title_label.pack(pady=(0, 20))
        
        # Scrollable frame for credits
        credits_frame = ctk.CTkScrollableFrame(main_frame)
        credits_frame.pack(fill="both", expand=True, pady=(0, 20))
        
        # Credits content
        credits_content = """
HIKARI IMAGE COMPRESSOR
Created by Gary19gts

OPEN SOURCE LIBRARIES & ACKNOWLEDGMENTS

This software is built upon the excellent work of many open source developers. We gratefully acknowledge the following libraries and their contributors:

🐍 PYTHON
• License: Python Software Foundation License
• The foundation that makes this application possible
• Website: https://python.org

🖼️ PILLOW (PIL Fork)
• License: HPND License
• Powerful image processing library
• Maintainers: Alex Clark and contributors
• Website: https://pillow.readthedocs.io
• Used for: Core image processing and compression

🎨 CUSTOMTKINTER
• License: MIT License
• Modern and customizable tkinter widgets
• Author: Tom Schimansky
• Website: https://github.com/TomSchimansky/CustomTkinter
• Used for: Modern UI components and styling

📸 IMAGEIO
• License: BSD 2-Clause License
• Versatile image I/O library
• Maintainers: Almar Klein and contributors
• Website: https://imageio.readthedocs.io
• Used for: Advanced image format support

🖥️ TKINTER
• License: Python Software Foundation License
• Standard GUI toolkit for Python
• Part of Python standard library
• Used for: Base GUI framework

SPECIAL THANKS

• The Python Software Foundation for maintaining Python
• All open source contributors who make projects like this possible
• The image processing community for continuous innovation
• Users who provide feedback and help improve the software

LICENSE INFORMATION

Hikari Image Compressor is licensed under the GNU Affero General Public License v3.0 (AGPL-3.0). This ensures that the software remains free and open source, and that any modifications or network use must also be made available under the same license.

For more information about the AGPL-3.0 license, visit:
https://www.gnu.org/licenses/agpl-3.0.html

CONTRIBUTING

This project is open source and welcomes contributions! Visit our GitHub repository to:
• Report bugs or request features
• Submit pull requests
• View the source code
• Read the full documentation

GitHub: https://github.com/Gary19gts/hikari-image-compressor
        """
        
        credits_text = ctk.CTkLabel(
            credits_frame,
            text=credits_content.strip(),
            font=ctk.CTkFont(size=12),
            justify="left",
            anchor="nw"
        )
        credits_text.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Buttons frame
        buttons_frame = ctk.CTkFrame(main_frame, fg_color="transparent")
        buttons_frame.pack(fill="x")
        
        # GitHub button
        github_btn = ctk.CTkButton(
            buttons_frame,
            text="View on GitHub",
            command=lambda: webbrowser.open("https://github.com/Gary19gts/hikari-image-compressor"),
            height=35,
            corner_radius=8,
            fg_color=COLORS['accent'],
            hover_color="#0056CC"
        )
        github_btn.pack(side="left", padx=(0, 10))
        
        # License button
        license_btn = ctk.CTkButton(
            buttons_frame,
            text="View License",
            command=lambda: webbrowser.open("https://www.gnu.org/licenses/agpl-3.0.html"),
            height=35,
            corner_radius=8,
            fg_color=COLORS['text_secondary'],
            hover_color=COLORS['accent']
        )
        license_btn.pack(side="left", padx=(0, 10))
        
        # Close button
        close_btn = ctk.CTkButton(
            buttons_frame,
            text="Close",
            command=credits_window.destroy,
            height=35,
            corner_radius=8,
            fg_color=COLORS['error'],
            hover_color="#CC2E24"
        )
        close_btn.pack(side="right")
    
    def get_quality_value(self):
        """Convert quality string to numeric value"""
        quality_map = {
            "Low (30%)": 30,
            "Medium (60%)": 60,
            "High (80%)": 80,
            "Maximum (95%)": 95
        }
        return quality_map.get(self.quality_var.get(), 80)
    
    def get_quality_suffix(self):
        """Get quality suffix for filename"""
        quality_suffix_map = {
            "Low (30%)": "-Low",
            "Medium (60%)": "-Medium",
            "High (80%)": "-High",
            "Maximum (95%)": "-Maximum"
        }
        return quality_suffix_map.get(self.quality_var.get(), "-High")
    
    def get_resize_suffix(self):
        """Get resize suffix for filename"""
        if not self.resize_enabled.get():
            return ""
        
        try:
            scale = self.resize_scale.get()
            return f"-{scale}pct"
        except:
            return "-resized"
    
    def start_compression(self):
        """Start the compression process"""
        if not self.loaded_images:
            messagebox.showwarning("No Images", "Please load images first.")
            return
        
        output_dir = self.output_folder.get()
        if not output_dir:
            output_dir = os.path.dirname(self.loaded_images[0])
        
        # Create output directory if it doesn't exist
        os.makedirs(output_dir, exist_ok=True)
        
        # Start compression in a separate thread
        thread = threading.Thread(target=self.compress_images, args=(output_dir,))
        thread.daemon = True
        thread.start()
    
    def compress_images(self, output_dir):
        """Compress images in background thread"""
        total_images = len(self.loaded_images)
        quality = self.get_quality_value()
        output_format = self.format_var.get().lower()
        
        for i, image_path in enumerate(self.loaded_images):
            try:
                # Update progress
                progress = (i + 1) / total_images
                self.root.after(0, lambda p=progress: self.progress.set(p))
                
                # Open and process image
                with Image.open(image_path) as img:
                    # Resize image if enabled
                    if self.resize_enabled.get():
                        original_width, original_height = img.size
                        new_width, new_height = self.calculate_resize_dimensions(original_width, original_height)
                        
                        if (new_width, new_height) != (original_width, original_height):
                            img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
                    
                    # Convert RGBA to RGB for JPEG
                    if output_format == 'jpeg' and img.mode in ('RGBA', 'LA', 'P'):
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                        img = background
                    
                    # Generate output filename with quality and resize suffix
                    base_name = os.path.splitext(os.path.basename(image_path))[0]
                    extension = 'jpg' if output_format == 'jpeg' else output_format
                    quality_suffix = self.get_quality_suffix()
                    resize_suffix = self.get_resize_suffix() if self.resize_enabled.get() else ""
                    output_path = os.path.join(output_dir, f"{base_name}_compressed{quality_suffix}{resize_suffix}.{extension}")
                    
                    # Save compressed image
                    save_kwargs = {'optimize': True}
                    if output_format in ['jpeg', 'webp']:
                        save_kwargs['quality'] = quality
                    
                    img.save(output_path, format=output_format.upper(), **save_kwargs)
                    
            except Exception as e:
                print(f"Error compressing {image_path}: {e}")
        
        # Show completion message
        self.root.after(0, self.compression_complete)
    
    def compression_complete(self):
        """Handle compression completion"""
        self.progress.set(1.0)
        messagebox.showinfo("Complete", "Image compression completed successfully!")
        self.progress.set(0)
    
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = ImageCompressor()
    app.run()