import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './components/Header';
import Footer from './components/Footer';
import Home from './pages/Home';
import Login from './pages/Login';
import Notes from './pages/Notes';

function App() {
    return (
        <Router>
            <Header />
            <Routes>
                <Route path="/" component={Home} />
                <Route path="/login" component={Login} />
                <Route path="/notes" component={Notes} />
            </Routes>
            
        </Router>
    );
}

export default App;
