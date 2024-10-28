import React, { useState } from 'react';
import './Notes.css'; // Importing the CSS file

const Notes = () => {
    const notes = [
        { "title": "title 1", "content": "content one", "id": 1 },
        { "title": "title 2", "content": "content two", "id": 2 },
        { "title": "title 3", "content": "content three", "id": 3 },
        { "title": "title 4", "content": "content four", "id": 4 },
    ];

    const [displayedNoteId, setDisplayedNoteId] = useState(-1);
    const [noteContent, setNoteContent] = useState("");
    const [noteTitle, setNoteTitle] = useState("");

    function handleTile(noteId) {
        const selectedNote = notes.find(note => note.id === noteId);
        if (selectedNote) {
            setNoteTitle(selectedNote.title);
            setNoteContent(selectedNote.content);
            setDisplayedNoteId(noteId);
        } else {
            console.error("Note not found");
        }
    }

    const handleSave = () => {
        alert(`Saving note titled "${noteTitle}" with content: "${noteContent}"`);
    };

    const leftPanelList = notes.map(note => (
        <li
            key={note.id}
            className="note-tile"
            onClick={() => handleTile(note.id)}
        >
            {note.title}
        </li>
    ));

    return (
        <div className="clearfix">
            <div className="left-col">
                <h2>Your notes</h2>
                <ul>
                    {leftPanelList}
                </ul>
            </div>
            <div className="right-col">
                <h3>
                    <input
                        type="text"
                        value={noteTitle}
                        onChange={(e) => setNoteTitle(e.target.value)}
                    />
                </h3>
                <textarea
                    id="notecontent"
                    name="content"
                    value={noteContent}
                    onChange={(e) => setNoteContent(e.target.value)}
                />
                <button onClick={handleSave}>Save</button>
            </div>
        </div>
    );
};

export default Notes;
