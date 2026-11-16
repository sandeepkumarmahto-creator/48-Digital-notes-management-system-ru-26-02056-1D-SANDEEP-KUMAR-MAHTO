"""Digital Notes Management System (PS No. 48)

Console application to add, view, search, edit and delete text notes.
Notes are stored permanently in notes.txt, one note per line, in the format:
    ID|Title|Content
The first note ID is N1.
"""

NOTES_FILE = "notes.txt"


def load_notes():
    """Load all notes from notes.txt into a list of [id, title, content]."""
    notes = []
    try:
        with open(NOTES_FILE, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line == "":
                    continue
                parts = line.split("|", 2)
                if len(parts) == 3:
                    notes.append([p.strip() for p in parts])
    except FileNotFoundError:
        pass  # no file yet, start with no notes
    return notes


def save_notes(notes):
    """Write all notes back to notes.txt."""
    with open(NOTES_FILE, "w", encoding="utf-8") as f:
        for note_id, title, content in notes:
            f.write(f"{note_id}|{title}|{content}\n")


def next_id(notes):
    """Return the next note ID (N1 for the first note)."""
    highest = 0
    for note in notes:
        num = note[0][1:]
        if num.isdigit() and int(num) > highest:
            highest = int(num)
    return f"N{highest + 1}"


def clean(text):
    """Remove the '|' separator so it cannot break the file format."""
    return text.strip().replace("|", "/")


def add_note(notes):
    title = clean(input("Title: "))
    content = clean(input("Content: "))
    if title == "":
        print("Title cannot be empty. Note not saved.")
        return
    note_id = next_id(notes)
    notes.append([note_id, title, content])
    save_notes(notes)
    print(f"Note saved. ID: {note_id} | {title}")


def view_notes(notes):
    if len(notes) == 0:
        print("No notes found.")
        return
    for note_id, title, content in notes:
        print(f"{note_id} | {title} | {content}")


def search_notes(notes):
    keyword = input("Keyword: ").strip().lower()
    found = False
    for note_id, title, content in notes:
        # case-insensitive search in both title and content
        if keyword in title.lower() or keyword in content.lower():
            print(f"{note_id} | {title} | {content}")
            found = True
    if not found:
        print("No notes found.")


def find_note(notes, note_id):
    for note in notes:
        if note[0].lower() == note_id.lower():
            return note
    return None


def edit_note(notes):
    note_id = input("Enter note ID: ").strip()
    note = find_note(notes, note_id)
    if note is None:
        print(f"Note {note_id} does not exist.")
        return
    new_content = clean(input("New content: "))
    note[2] = new_content
    save_notes(notes)
    print(f"Note {note[0]} updated.")


def delete_note(notes):
    note_id = input("Enter note ID: ").strip()
    note = find_note(notes, note_id)
    if note is None:
        print(f"Note {note_id} does not exist.")
        return
    notes.remove(note)
    save_notes(notes)
    print(f"Note {note[0]} deleted. Notes left: {len(notes)}")


def main():
    print("=== Digital Notes Management System ===")
    while True:
        notes = load_notes()  # load again so the file is always the source
        print("\nMenu:")
        print("1. Add note")
        print("2. View all notes")
        print("3. Search notes")
        print("4. Edit note")
        print("5. Delete note")
        print("6. Exit")
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            add_note(notes)
        elif choice == "2":
            view_notes(notes)
        elif choice == "3":
            search_notes(notes)
        elif choice == "4":
            edit_note(notes)
        elif choice == "5":
            delete_note(notes)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
