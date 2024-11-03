import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './components/Header';
import Home from './pages/Home';
import Login from './pages/Login';
import Logout from './pages/Logout';
import Notes from './pages/Notes';
import Register from './pages/Register';

function App() {
    return (
        <Router>
            <Header />
            <Routes>
                <Route path="/" component={Home} />
                <Route path="/login" component={Login} />
                <Route path="/notes" component={Notes} />
                <Route path="/register" component={Register} />
                <Route path="/logout" component={Logout} />
            </Routes>
            
        </Router>
    );
}

export default App;
