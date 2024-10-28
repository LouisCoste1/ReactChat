// Header.js
import React from 'react';
import "./Header.css"

const Header = () => {
    return (
        <header>
            <h1>Secure Notes App</h1>
            <nav>
                <a href="/">Home</a>
                <a href="/login">Login</a>
                <a href="/logout">logout</a>
                <a href="/notes">My Notes</a>
            </nav>
        </header>
    );
};

export default Header;
