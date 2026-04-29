# graphic-editor-python
# Python Graphic Editor

This is a student project for the system programming course.  
The project is implemented as a complete graphic editor based on previous laboratory works related to graphics programming.

## Project Goal

The goal of this project is to design and implement a simple but complete graphic editor with a user-friendly graphical interface, basic drawing tools, image editing operations, help documentation, and example images.

The program combines and extends the topics from previous laboratory works:

- Lab 8: basic graphic editor structure and drawing primitives;
- Lab 9: graphic operations, undo, canceling actions, selection and copy/paste operations;
- Lab 10: additional image operations, scrolling for large images, filters, rotation and mirroring.

## Main Features

The project is planned to include:

- graphical user interface built with Python and Tkinter;
- drawing canvas;
- pencil tool;
- line tool;
- rectangle tool;
- ellipse/oval tool;
- color selection;
- line width selection;
- fill color selection where applicable;
- new image creation;
- opening image files;
- saving images as PNG;
- undo last operation;
- cancel current drawing operation with Esc;
- clear canvas with confirmation;
- selection of image area;
- copy and paste selected area;
- moving pasted image fragments;
- scrollbars for working with large images;
- grayscale filter;
- color inversion filter;
- horizontal mirror operation;
- vertical mirror operation;
- rotation by 90 degrees;
- toolbar grouped by functionality;
- option to show or hide tool groups;
- built-in help menu;
- external `help.html` documentation file;
- examples folder with sample images and comments;
- project report materials.

## Technologies

- Python
- Tkinter
- Pillow

## Project Structure

```text
graphic-editor-python/
│
├── main.py
├── requirements.txt
├── README.md
├── PROJECT_REQUIREMENTS.md
├── help.html
│
├── examples/
│   ├── comments.txt
│   └── sample images
│
└── docs/
    └── notes_for_report.md
