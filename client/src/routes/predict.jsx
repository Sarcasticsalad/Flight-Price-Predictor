// Prediction.jsx
import React, {useEffect, useState} from "react";
import { useNavigate, useLocation } from "react-router-dom";


export default function Prediction({ PredictedPrice }) {
  const navigate = useNavigate();  
  const {state} = useLocation();

  const [predictedPrice, setPredictedPrice] = useState(state.data.price);

  

  const handleSubmit = () => {
    navigate("/");
  };

  return (
    <div className="flex items-center justify-center h-screen ml-[30rem]">
      <div className="text-center">
        <h1 className="text-5xl mb-10 font-semibold">Prediction Outcome</h1>
        <p className="text-2xl mb-10">
          Predicted Price<br /><br></br>NRP {predictedPrice}
        </p>
        <button
          onClick={handleSubmit}
          className="bg-blue-500 text-xl text-white p-2 rounded-full w-32 hover:bg-blue-600 focus:outline-none focus:shadow-outline-blue"
        >
          Dashboard
        </button>
      </div>
    </div>
  );
}
