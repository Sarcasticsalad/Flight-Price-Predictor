import React from 'react'
import {useState, useEffect} from 'react'




const Test = () => {

    const [name, setName] = useState("")
    const [password, setPassword] = useState("")

    const handleSubmit = (event) => {
        event.preventDefault();
    
        // Get the values of the input fields
        const name = event.target.elements.name.value;
        const password = event.target.elements.password.value;
    
        // Create a JSON object
        const formData = {
          name: name,
          password: password,
        };
    
        // Log the JSON object in the console
        console.log(formData);
      };

    
    return (
        <>
            <form action="/formPage" method='POST' onSubmit={handleSubmit}>
                <label htmlFor="">Enter the Name</label>
                <br />
                <input type="text" name="name" id="name" />
                <br />
                <label htmlFor="">Enter the Password</label>
                <br />
                <input type="password" name="password" id="password" />
                <br />
                <button type="submit">Submit</button>
            </form>
        </>
    )
}

export default Test