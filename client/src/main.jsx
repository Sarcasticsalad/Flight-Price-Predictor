import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App.jsx'
import './index.css'
import Root from './routes/root.jsx'
import ErrorPage from './error-page.jsx'
import { createBrowserRouter, RouterProvider } from 'react-router-dom';
import "./index.css";
import FormPage from './routes/form.jsx'
import Prediction from './routes/predict.jsx'
import Test from './routes/test.jsx'

const router = createBrowserRouter([
  {
    path: "/",
    
    element: <FormPage/>
  },


  {
    path: "/prediction",
    element: <Prediction/>
  }

]);

ReactDOM.createRoot(document.getElementById('root')).render(
  <React.StrictMode>
    <RouterProvider router={router}/>
    {/* <App/> */}
  </React.StrictMode>,
)
