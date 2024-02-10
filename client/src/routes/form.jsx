// import { Form } from "react-router-dom";

import { useState } from "react"

import { useNavigate } from "react-router-dom";
export default function FormPage() {
    const navigate = useNavigate()
    const [data, setData] = useState({
        "departure_date": "",
        "departure": "",
        "arrival_date": "",
        "destination": "",
        "airline": "",
        "flight_class": "",
        "stops": "",
        "travel_time": ""
    });

    // const history = useHistory();

    const handleInputChange = ((event) => {
        const result = data;
        result[event.target.name] = event.target.value;
        setData(result);
    });


    const handleSubmit = async(event, error) => {
        event.preventDefault();
        event.preventDefault();
        const res = await fetch("http://127.0.0.1:8000/predict",{
            method: 'POST',
            body: JSON.stringify({data}),
            headers: {'Content-Type': 'application/json'}
        })
        
        const predict_price = await res.json();
        
        
        navigate('/prediction', {state: {data:predict_price}})
    };
    return (
        <>
            <div>
                <nav className="bg-blue-500 p-4 w-screen">
                    <ul>
                        <li><h1 className="text-white text-2xl font-bold">Flight Price Predictor</h1></li>
                    </ul>
                </nav>
                
            </div>
            <div className="flex items-center justify-center h-screen" >    
                <form className="bg-white p-8 rounded-md shadow-md max-w-xl w-full mt-8 min-h-96" method="post" onSubmit={handleSubmit} >
                <div className="flex flex-wrap -mx-4">      
                    <div className="w-full md:w-1/2 px-4 mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2">Departure Date</label>
                    <input type="date" name="departure_date" className="w-full border p-2 rounded-md" onChange={handleInputChange}/>
                    </div>
                    <div className="w-full md:w-1/2 px-4 mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2" >Departure City</label>
                    <input type="text" name="departure" className="w-full border p-2 rounded-md mb-4" onChange={handleInputChange}/>
                    </div>
                    <div className="w-full md:w-1/2 px-4 mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2">Arrival Date</label>
                    <input type="date" name="arrival_date" className="w-full border p-2 rounded-md mb-4" onChange={handleInputChange}/>
                    </div>
                    <div className="w-full md:w-1/2 px-4 mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2">Destination City</label>
                    <input type="text" name="destination" className="w-full border p-2 rounded-md mb-4" onChange={handleInputChange} />
                    </div>
                    <div className="w-full md:w-1/2 px-4 mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2">Airline</label>
                    <input type="text" name="airline" className="w-full border p-2 rounded-md mb-4" onChange={handleInputChange} />
                    </div>
                    <div className="w-full md:w-1/2 px-4 mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2">Flight Class</label>
                    <input type="text" name="flight_class" className="w-full border p-2 rounded-md mb-4"  onChange={handleInputChange}/>
                    </div>
                    <div className="w-full md:w-1/2 px-4 mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2">Stops</label>
                    <input type="number" name="stops"  className="w-full border p-2 rounded-md mb-4" onChange={handleInputChange} />
                    </div>
                    <div className="w-full md:w-1/2 px-4 mb-4">
                    <label className="block text-gray-700 text-sm font-bold mb-2">Travel Time</label>
                    <input type="number" name="travel_time" className="w-full border p-2 rounded-md mb-4"  onChange={handleInputChange}/>
                    </div>
                    </div>
                    <div className="flex items-center justify-center mt-4">
                    <button className="bg-blue-500 text-white p-2 rounded-full w-32 hover:bg-blue-600 focus:outline-none focus:shadow-outline-blue">Predict</button>
                    </div>
                </form>
            </div>
        </>
    );
}