import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import App from './App';
import reportWebVitals from './reportWebVitals';
import {
  createBrowserRouter,
  RouterProvider,
} from "react-router-dom";


import Home from './pages/Home';
import Login from './pages/Login';
import Logout from './pages/Logout';
import Notes from './pages/Notes';
import Register from './pages/Register';
import ErrorPage from "./error-page";


const router = createBrowserRouter([
  {
    path: "/notes",
    element: <Notes/>,
  },
  {
    path: "/login",
    element: <Login/>,
  },
  {
    path: "/register",
    element: <Register/>,
  },
  {
    path: "/logout",
    element: <Logout/>,
  },
  {
    path: "/",
    element: <Home/>,
    errorElement: <ErrorPage />,
  },
]);


const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <App />
    <RouterProvider router={router} />
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
