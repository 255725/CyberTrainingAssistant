import { useState, useEffect } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';


function StatystykiUzytkownikaZalogowany() {
    const [dane, setDane] = useState([]);

    useEffect(() => {
        const pobierzDane = async() => {
            const token = localStorage.getItem('token');
            const response = await fetch('http://localhost:8000/stats/me', {
                headers: { 'Autorization': `Bearer ${token}`}
            });
            const json = await response.json();
            setDane(json);
        };
        pobierzDane();
    }, []);

    return(
        <div style={{width}}
    )
}
export default StatystykiUzytkownikaZalogowany;