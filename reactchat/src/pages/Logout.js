// Logout.js
import React from 'react';



const Logout = () => {
    fetch('http://localhost/api/users/logout', {
        method: 'POST',
        credentials: 'include'
    }).then((resp) => {
        console.log("logged out")
    });

    return (
        <div class="login">
            <h2>You have been logged out</h2>
        </div>
    );
};

export default Logout;
