# Project Specification: Python Graphic Editor

## 1. General Description

This project is a student graphic editor implemented in Python.  
It is developed as a final project for the graphics programming section of the system programming course.

The project combines and extends the ideas from previous laboratory works. Instead of submitting separate small laboratory programs, the result should be a single complete desktop application with a graphical interface, drawing tools, image editing operations, help documentation, examples, and materials for the final report.

The application should be simple enough for a student project, but complete enough to look like a finished program.

## 2. Technologies

The project should use:

- Python;
- Tkinter for the graphical user interface;
- Pillow for image processing, opening, editing and saving image files.

The application interface should be in Ukrainian.

## 3. Project Goal

The goal of the project is to design and implement a small graphic editor that allows the user to create, edit, process and save simple images.

The editor should include:

- a main application window;
- a drawing area;
- grouped tool panels;
- standard file operations;
- basic drawing tools;
- editing operations;
- image processing operations;
- help subsystem;
- examples folder;
- documentation for the final report.

## 4. Connection with Previous Laboratory Works

The project is based on the content of previous laboratory works related to graphics programming.

### Lab 8: Basic Graphic Editor Elements

The project should include the basic editor structure and drawing tools:

- main window;
- drawing canvas;
- mouse-based drawing;
- pencil tool;
- line tool;
- rectangle tool;
- ellipse/oval tool;
- line color selection;
- fill color selection;
- line width selection;
- creating a new image;
- opening an existing image;
- saving the image to a file.

### Lab 9: Graphic Operations and Editing

The project should include editing operations:

- undo last operation;
- cancel current unfinished operation with Esc;
- rectangular area selection;
- copy selected area;
- paste copied area;
- delete or clear selected area, if possible;
- clear canvas with confirmation.

A simplified implementation is acceptable, for example storing image snapshots for undo.

### Lab 10: Additional Image Operations

The project should include additional image processing operations:

- grayscale filter;
- color inversion;
- horizontal mirror operation;
- vertical mirror operation;
- rotation by 90 degrees;
- support for large images with scrollbars;
- one additional operation if possible, for example blur, sharpen, resize or text insertion.

## 5. Main Functional Requirements

The graphic editor should support the following features:

### File Operations

- New image;
- Open image;
- Save image;
- Save image as;
- Exit.

The program should ask for confirmation before losing unsaved changes.

### Drawing Tools

- Pencil;
- Line;
- Rectangle;
- Ellipse/Oval.

The user should be able to choose:

- line color;
- fill color;
- line width.

### Editing Operations

- Undo;
- Cancel current operation with Esc;
- Select rectangular area;
- Copy selected area;
- Paste copied area;
- Clear canvas with confirmation.

### Image Operations

- Grayscale;
- Invert colors;
- Rotate 90 degrees;
- Mirror horizontally;
- Mirror vertically.

### View Options

- Scrollbars for large images;
- show or hide the toolbar;
- clear indication of the current selected tool.

### Help

- Help menu;
- About dialog;
- external `help.html` file opened from the program.

## 6. Interface Requirements

The user interface should be clear, logical and user-friendly.

The visible interface should use Ukrainian labels that are understandable to a regular user.

Examples:

- Новий;
- Відкрити;
- Зберегти;
- Олівець;
- Лінія;
- Прямокутник;
- Еліпс;
- Колір лінії;
- Колір заливки;
- Товщина;
- Скасувати;
- Очистити;
- Довідка.

The interface should not use technical or internal programming terms for user-visible commands.

## 7. Functional Groups

Commands should be divided into logical groups.

Suggested groups:

- File;
- Drawing;
- Shapes;
- Selection and Editing;
- Properties;
- Image Operations;
- View;
- Help.

The user should be able to show or hide at least the main toolbar.  
If possible, separate tool groups can also be shown or hidden.

## 8. Usability Requirements

The editor should follow basic software ergonomics principles:

- commands should be logically grouped;
- similar actions should have similar names;
- destructive actions should require confirmation;
- the user should not have to remember hidden instructions;
- the current tool should be visible;
- help should be easy to access;
- error messages should be clear and understandable.

Examples of confirmation dialogs:

- before clearing the canvas;
- before creating a new image if the current one was modified;
- before exiting if there are unsaved changes.

Examples of user messages:

- "Немає дії для скасування.";
- "Спочатку виберіть область зображення.";
- "Файл не вдалося відкрити.";
- "Зображення успішно збережено.".

## 9. Help Subsystem

The project should include a separate file:

```text
help.html
