# Labs Summary

This file summarizes the previous graphics programming laboratory works that are used as the basis for the final graphic editor project.

The final project should not be three separate laboratory works.  
It should be one complete graphic editor that combines and extends the ideas from Lab 8, Lab 9 and Lab 10.

---

## Lab 8: Basic Graphic Editor Structure

Lab 8 is used as the base of the final project.

Main ideas from Lab 8:

- create the main application window;
- create a drawing area;
- add menus and toolbars;
- implement basic drawing tools;
- work with mouse events;
- add file operations;
- add color and line width settings.

Features from Lab 8 that should be included in the final project:

- drawing canvas;
- pencil or free drawing tool;
- line tool;
- rectangle tool;
- ellipse/oval tool;
- line color selection;
- fill color selection;
- line width selection;
- new image;
- open image;
- save image;
- save as.

In the final Python project, raster graphics should be used.  
The image itself should be stored using Pillow, and the Tkinter canvas should display the current image.

---

## Lab 9: Editing Operations

Lab 9 adds editing operations to the graphic editor.

Main ideas from Lab 9:

- cancel an unfinished drawing operation;
- undo completed operations;
- select an image area;
- copy and paste selected parts of the image;
- manage user mistakes during editing.

Features from Lab 9 that should be included in the final project:

- undo last operation;
- cancel current unfinished operation with Esc;
- rectangular selection;
- copy selected area;
- paste copied area;
- clear canvas with confirmation;
- delete or clear selected area if possible.

A simplified implementation is acceptable.  
For example, the program can save full image snapshots before each operation and restore the previous image for Undo.

---

## Lab 10: Additional Image Operations

Lab 10 adds extra graphic operations and support for larger images.

Main ideas from Lab 10:

- work with large images;
- use scrollbars;
- correctly calculate mouse coordinates after scrolling;
- apply image filters;
- rotate images;
- mirror images;
- add extra image processing operations.

Features from Lab 10 that should be included in the final project:

- horizontal and vertical scrollbars for large images;
- correct mouse coordinates with canvas scrolling;
- grayscale filter;
- color inversion filter;
- rotate 90 degrees;
- mirror horizontally;
- mirror vertically;
- one additional operation if possible, for example blur, sharpen, resize or text insertion.

---

## Connection with the Final Project

The final project is a complete Python graphic editor.

It combines:

- Lab 8: base editor interface, canvas, drawing tools and file operations;
- Lab 9: undo, cancel, selection, copy and paste;
- Lab 10: filters, rotation, mirroring and support for large images.

The program should also satisfy the final teacher requirements:

1. User-friendly external interface.
2. Help subsystem through `help.html`.
3. Examples folder with images and comments.
4. Commands divided into functional groups.
5. Improved external design and software ergonomics.

---

## Recommended Final Feature Set

The final editor should include:

- main window;
- drawing canvas;
- pencil;
- line;
- rectangle;
- ellipse;
- line color;
- fill color;
- line width;
- new image;
- open image;
- save image;
- save as;
- undo;
- Esc cancel;
- clear canvas with confirmation;
- rectangular selection;
- copy selected area;
- paste selected area;
- grayscale filter;
- color inversion;
- rotate 90 degrees;
- mirror horizontally;
- mirror vertically;
- scrollbars for large images;
- toolbar grouped by functionality;
- option to show or hide the toolbar;
- help menu;
- external `help.html`;
- `examples/comments.txt`;
- `docs/notes_for_report.md`.

---

## Submission Reminder

The final submission should contain:

1. The Python project files or project archive.
2. A separate non-archived report file.
3. Screenshots in the report for the key project functions.

The working files for Codex, such as this summary and reference laboratory PDFs, do not have to be included in the final clean submission archive.
