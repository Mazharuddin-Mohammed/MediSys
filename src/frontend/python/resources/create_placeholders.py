#!/usr/bin/env python3
"""
MediSys Hospital Management System - Placeholder Image Generator

This script creates placeholder images for patients and doctors to be used
when no actual photo is available. It generates simple silhouette images
with different colors for patients and doctors.

Author: Mazharuddin Mohammed
"""

from PIL import Image, ImageDraw, ImageFont
import os

def create_placeholder(filename, text, bg_color, text_color):
    """Create a placeholder image with text"""
    # Create a 200x200 image with the specified background color
    img = Image.new('RGB', (200, 200), bg_color)
    draw = ImageDraw.Draw(img)
    
    # Draw a silhouette
    # Head
    draw.ellipse((75, 40, 125, 90), fill=text_color)
    # Body
    draw.rectangle((85, 90, 115, 150), fill=text_color)
    # Arms
    draw.rectangle((65, 90, 85, 130), fill=text_color)  # Left arm
    draw.rectangle((115, 90, 135, 130), fill=text_color)  # Right arm
    # Legs
    draw.rectangle((85, 150, 95, 180), fill=text_color)  # Left leg
    draw.rectangle((105, 150, 115, 180), fill=text_color)  # Right leg
    
    # Add text at the bottom
    try:
        font = ImageFont.truetype("DejaVuSans.ttf", 16)
    except IOError:
        # Fallback to default font if DejaVuSans is not available
        font = ImageFont.load_default()
    
    # Calculate text position to center it
    text_width = draw.textlength(text, font=font)
    text_position = ((200 - text_width) // 2, 180)
    
    # Draw the text
    draw.text(text_position, text, fill=text_color, font=font)
    
    # Save the image
    img.save(filename)
    print(f"Created placeholder image: {filename}")

def main():
    # Create directory if it doesn't exist
    placeholder_dir = "src/frontend/python/resources/images/placeholders"
    os.makedirs(placeholder_dir, exist_ok=True)
    
    # Create patient placeholder
    patient_file = os.path.join(placeholder_dir, "patient_placeholder.png")
    create_placeholder(patient_file, "Patient", "#E0F7FA", "#006064")
    
    # Create doctor placeholder
    doctor_file = os.path.join(placeholder_dir, "doctor_placeholder.png")
    create_placeholder(doctor_file, "Doctor", "#E8F5E9", "#1B5E20")

if __name__ == "__main__":
    main()
