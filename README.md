# Digital Notes Management System


A console application in Python 3 to write, view, search, edit and delete text
notes. All notes are saved permanently in a text file.

**Concepts used:** Strings, Files, Search, CRUD

## Features
- Add a note with a title and content (empty titles are rejected)
- View all notes
- Search notes by keyword (case-insensitive, checks title and content)
- Edit the content of a note by its ID
- Delete a note by its ID
- Shows a message when a note ID does not exist
- Notes are saved in notes.txt and loaded again at program start

## Note Format
Each note is stored on one line in notes.txt as:

    ID|Title|Content

Example:

    N1|Python|Learn loops
    N2|Maths|Revise algebra

The first note ID is N1.

## Project Structure
    code base/
    |-- one.py            Python solution
    |-- notes.txt         Notes storage (created by the program)
    |-- code_output.pdf   Code and terminal output
    `-- README.md         This file

## Requirements
- Python 3.x (no external libraries needed)

## How to Run
    python one.py

Menu:

    1. Add note
    2. View all notes
    3. Search notes
    4. Edit note
    5. Delete note
    6. Exit

## Test Cases
1. Normal input - Add, Title: Python, Content: Learn loops
   Output: Note saved. ID: N1 | Python
2. Boundary input - notes.txt is empty, View all
   Output: No notes found.
3. Invalid input - Add with an empty title
   Output: Title cannot be empty. Note not saved.
4. Different valid scenario - notes.txt has N1 and N2
   (a) Search "python"  ->  N1 | Python | Learn loops
   (b) Edit N2          ->  Note N2 updated.
   (c) Delete N1        ->  Note N1 deleted. Notes left: 1

## Notes
- The "|" character is replaced with "/" in titles and content so it cannot
  break the file format.
- IDs are never reused: the next ID is one more than the highest existing ID.
