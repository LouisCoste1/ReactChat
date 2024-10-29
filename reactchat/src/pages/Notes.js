import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Notes.css'; // Importing the CSS file

const Notes = () => {
    const isAuthenticated = document.cookie.split('; ').some(row => row.startsWith('session='));
    const navigate = useNavigate()
    useEffect(() => {
        if (isAuthenticated === false) {
            navigate("/login", {replace: true})
        }
    }, [isAuthenticated, navigate]);

    const [noteContent, setNoteContent] = useState("");
    const [currentNoteID, setcurrentNoteID] = useState(-1);
    const [noteTitle, setNoteTitle] = useState("");
    const [notes, setNotes] = useState([]);

    useEffect(() => {
        const fetchNotes = async () => {
            try {
                const response = await fetch('http://localhost:5000/notes', {
                    method: 'GET',
                    credentials: 'include'
                });
                const data = await response.json();
                console.log(data.notes)
                setNotes(data.notes);
            } catch (error) {
                console.error("Failed to fetch notes:", error);
            }
        };

        fetchNotes();
    }, []);

    

    function handleTile(noteId) {
        const selectedNote = notes.find(note => note.id === noteId);
        if (selectedNote) {
            setNoteTitle(selectedNote.title);
            setNoteContent(selectedNote.content);
            setcurrentNoteID(selectedNote.id);
        } else {
            console.error("Note not found");
        }
    }

    const handleSave = async () => {
        if (currentNoteID === -1) { // -2 in id to say it is new
            // user is creating a new note, save it a a new note
            const response = await fetch("http://localhost:5000/notes/create", {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({"content": noteContent, "title": noteTitle}),
                credentials: "include"
            })
            const data = await response.json()
            if (response.ok) {
                setNotes([...notes, { id: data["id_created"], title: noteTitle, content: noteContent }]);
                setNoteTitle(noteTitle);
                setNoteContent(noteContent);
                setcurrentNoteID(data["id_created"]);
            }
            else {
                alert("error: ", data['msg'])
            }
        }
        else {
            // user is just saving a note that already existed
            const response = await fetch("http://localhost:5000/notes/note", {
                method: "PUT",
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({"id": currentNoteID, "content": noteContent, "title": noteTitle}),
                credentials: "include"
            })
            const data = await response.json()
            if (response.ok) {
                setNotes(notes.map(note => note.id === currentNoteID ? { ...note, title: noteTitle } : note));
                setNoteTitle(noteTitle);
                setNoteContent(noteContent);
            }
            else {
                alert("error: ", data['msg'])
            }
        }
    };
    const handleDelete = async () => {
        if (currentNoteID === -1) {
            // use didn't click on any note, just the delte button: do nothing
            return
        }
        const response = await fetch("http://localhost:5000/notes/note?" + new URLSearchParams({note_id: currentNoteID}).toString(), {
            method: "DELETE",
            credentials: "include"
        })
        const data = await response.json()
        if (response.ok) {
            setNotes(notes.filter(note => note.id !== currentNoteID));
            setNoteTitle("");
            setNoteContent("");
            setcurrentNoteID(-1);
        }
        else {
            alert("error: ", data['msg'])
        }
    };
    const handleNew = async () => {
        setNoteTitle("");
        setNoteContent("");
        setcurrentNoteID(-1); // minus two means we are creating a new note and don't know the id yet

    };

    const leftPanelList = notes.length > 0 ? notes.map(note => (
        <li
            key={note.id}
            className="note-tile"
            onClick={() => handleTile(note.id)}
        >
            {note.title}
        </li>
    )) : <li>No notes available</li>; // Fallback if no notes are found



    return (
        <div className="clearfix">
            <div className="left-col">
                <div class="left-col-title">
                    <h2>Your notes</h2>
                    <button onClick={handleNew}>New</button>
                </div>
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
                <button onClick={handleDelete}>Delete</button>
            </div>
        </div>
    );
};

export default Notes;
