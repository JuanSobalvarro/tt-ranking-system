import React, { useState } from "react";
import { Label, TextInput } from "flowbite-react";
import { getCurrentDateTime } from "services/helpers.js";

const MatchDateTimeInput = ({ matchDateTime, setMatchDateTime }) => {
  const [error, setError] = useState("");

  // Handle manual changes
  const handleDateChange = (e) => {
    const selectedDateTime = e.target.value;
    // if (selectedDateTime < getCurrentDateTime()) {
    //   setError("La fecha y hora no pueden estar en el pasado.");
    // } else {
    //   setError("");
    //   setMatchDateTime(selectedDateTime);
    // }
    setMatchDateTime(selectedDateTime);
  };

  // Automatically select current date-time when pressing Enter or OK
  const handleKeyPress = (e) => {
    if (e.key === "Enter") {
        const selectedDateTime = getCurrentDateTime();
        console.log(selectedDateTime);
        setMatchDateTime(selectedDateTime);
    }
  };

  return (
    <div className="mb-6 w-full max-w-md">
      <Label htmlFor="matchDateTime" className="block mb-2 text-sm font-medium text-gray-100">
        Fecha y Hora del Partido
      </Label>

      <TextInput
        type="datetime-local"
        id="matchDateTime"
        value={matchDateTime}
        onChange={handleDateChange}
        onKeyDown={handleKeyPress} // Automatically set current date-time on Enter
        required
        // min={getCurrentDateTime()} // Prevent past dates
        className={`w-full ${error ? "border-red-500" : "border-gray-300"} focus:ring-green-500`}
      />

      {error && <p className="text-red-500 text-sm mt-1">{error}</p>}
    </div>
  );
};

export default MatchDateTimeInput;
