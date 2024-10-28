// Login.js
import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import "./Login.css"


const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');

    const handleLogin = async (e) => {
        e.preventDefault();

        const response = await fetch('http://localhost:5000/users/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        });

        const data = await response.json();

        if (response.ok) {
            // Handle successful login (e.g., set user session)
            alert(`Login successful: ${data.msg}`);
            // You can store user_id in sessionStorage or handle it as needed
        } else {
            alert(data.msg); // Set error message
        }

    };

    return (
        <div class="login">
            <h2>Login</h2>
            <form onSubmit={handleLogin}>
                <input
                    type="text"
                    placeholder="Username"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <input
                    type="password"
                    placeholder="Password"
                    value={password}
                    onChange={(e) => setPassword(e.target.value)}
                />
                <button type="submit">Login</button>

                <p>
                    Don't have an account? 
                    <Link to="/register"> Register here</Link>
                </p>
            </form>
        </div>
    );
};

export default Login;
