import "../App.css";
import { useState, useEffect } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';



function StatystykiUzytkownikaZalogowany() {
    const [wszystkieDane, setWszystkieDane] = useState(new Array());
    const [wybraneCwiczenie, setWybraneCwiczenie] = useState("1");

    useEffect(() => {
        const pobierzDane = async() => {
            const token = localStorage.getItem('token');
            if (!token) {
                console.error("Brak tokena! Zaloguj się.");
                return;
            }
            try{
                const response = await fetch('http://localhost:8000/stats/me', {
                    headers: { 'Authorization': `Bearer ${token}`}
                });
                if(response.ok){
                    const json = await response.json();

                    const sformatowaneDane = json.map(element => {
                        const data = new Date(element.DateAdded);

                        const ladnaData = data.toLocaleString('pl-PL', {
                            day: '2-digit',
                            month: '2-digit',
                            year: 'numeric',
                            hour: '2-digit',
                            minute: '2-digit'
                        });
                        return {
                            ...element,
                            DateAdded: ladnaData
                        };
                    });
                    setWszystkieDane(sformatowaneDane);
                }else{
                    console.error("Błąd autoryzacji lub serwera. Status:", response.status);
                }
            }catch(error) {
                console.error("Błąd połączenia z serwerem:", error);
            }
        };
        pobierzDane();
    }, []);

    const daneDoWykresu = wszystkieDane.filter(
        item => item.IDExercise.toString() === wybraneCwiczenie
    );

    const generujKalendarz = () => {
        const dzisiaj = new Date();
        const rok = dzisiaj.getFullYear();
        const miesiac = dzisiaj.getMonth();
        const dniWMiesiacu = new Date(rok, miesiac + 1, 0).getDate();
        const pierwszyDzien = new Date(rok, miesiac, 1).getDay();
        
        const przesuniecie = pierwszyDzien === 0 ? 6 : pierwszyDzien - 1; 

        const komorki = new Array();
        const nazwyDni = new Array("Pn", "Wt", "Śr", "Cz", "Pt", "So", "Nd");

        for (let i = 0; i < 7; i++) {
            komorki.push(
                <div key={`header-${i}`} className="calendar-day-header">
                    {nazwyDni.at(i)}
                </div>
            );
        }

        for (let i = 0; i < przesuniecie; i++) {
            komorki.push(<div key={`empty-${i}`} className="calendar-day empty"></div>);
        }

        for (let i = 1; i <= dniWMiesiacu; i++) {
            const dzienStr = String(i).padStart(2, '0');
            const miesiacStr = String(miesiac + 1).padStart(2, '0');
            const szukanaData = `${dzienStr}.${miesiacStr}.${rok}`;

            const czyTrenowal = wszystkieDane.some(trening => trening.DateAdded.substring(0, 10) === szukanaData);
            const czyDzisiaj = dzisiaj.getDate() === i;

            komorki.push(
                <div
                    key={`day-${i}`}
                    className={`calendar-day ${czyTrenowal ? 'trained' : ''} ${czyDzisiaj ? 'today' : ''}`}
                >
                    {i}
                </div>
            );
        }

        return komorki;
    };

    return(
        <div className="stats-container">
            <h2 className="stats-header">Twoje Postępy</h2>
            <div className="chart-wrapper" style={{ marginBottom: '30px' }}>
                <div className="exercise-selection-container">
                    <label htmlFor="exercise-select" className="exercise-selection-label">
                        Wybierz ćwiczenie:
                    </label>
                    <select
                        id="exercise-select"
                        value={wybraneCwiczenie}
                        onChange={(e) => setWybraneCwiczenie(e.target.value)}
                        className="exercise-selection-dropdown"
                    >
                        <option value="2">Wznosy bokiem (Barki)</option>
                        <option value="1">Uginanie ramion (Biceps)</option>
                        <option value="3">Wyskok dosiężny</option>
                    </select>
                </div>
                <div style={{ width: '100%', height: '400px', marginTop: '20px' }}>
                    <ResponsiveContainer width="100%" height="100%">
                        <LineChart data={daneDoWykresu} margin={{ top: 20, right: 30, left: 0, bottom: 0 }}>
                            <CartesianGrid strokeDasharray="3 3" stroke="#e5e5e5" />
                            <XAxis dataKey="DateAdded" stroke="#555" />
                            <YAxis stroke="#555"/>
                            <Tooltip contentStyle={{backgroundColor: '#fff', borderRadius: '8px', border: '1px solid #e5e5e5', color: '#000', boxShadow: '0 4px 15px rgba(0,0,0,0.05)'}} />
                            <Legend wrapperStyle={{ paddingTop: '20px' }}/>
                                
                            <Line type="monotone" dataKey="RepCount" stroke="#000080" name="Powtórzenia" strokeWidth={3} />
                            {wybraneCwiczenie === "3" ? (
                                <Line type="monotone" dataKey="JumpHeight" stroke="#ffc658" name="Wysokość skoku (cm)" strokeWidth={3} />
                            ) : (
                                <Line type="monotone" dataKey="Weight" stroke="#1e8e3e" name="Waga (kg)" strokeWidth={3} />
                            )}
                            
                        </LineChart>
                    </ResponsiveContainer>
                </div>
            </div>
            <div className="calendar-wrapper">
                <h3 className="calendar-title">Aktywność Treningowa (Bieżący Miesiąc)</h3>
                <div className="calendar-grid">
                    {generujKalendarz()}
                </div>
                
                <div className="calendar-legend">
                    <div className="legend-item">
                        <div className="legend-box empty"></div>
                        <span>Brak treningu</span>
                    </div>
                    <div className="legend-item">
                        <div className="legend-box trained"></div>
                        <span>Zrealizowany</span>
                    </div>
                </div>
            </div>
        </div>
    )
}
export default StatystykiUzytkownikaZalogowany;