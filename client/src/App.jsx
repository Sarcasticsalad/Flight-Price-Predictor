import { useState } from 'react'
import { ReactDOM } from 'react-dom/client';
import './App.css'
import Test from './routes/test';
function App() {

  return (
    <BrowserRouter>
      <Routes>
        <Route path="/home" element={<Form />}>
          <Route index element={<Home />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
