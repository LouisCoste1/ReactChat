// Login.js
import React, { useState } from 'react';
import { Link, useNavigate  } from 'react-router-dom';
import "./Login.css"


const Login = () => {
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [error_message, setError] = useState('');
    const navigate = useNavigate()


    const handleLogin = async (e) => {
        e.preventDefault();

        const response = await fetch('http://localhost:5000/users/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
            credentials: 'include'
        });

        const data = await response.json();

        if (response.ok) {
            navigate("/notes")
            
        } else {
            setError(data.msg);
            
        }

    };

    return (
        <div class="login">
            <h2>Login</h2>
            {error_message !== "" && <div class="error"><p>{error_message}</p></div>}
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
