import { useState } from "react";
import "../App.css"; // lub Twój plik z profilowym CSS

function ProfilZalogowany() {
    const [nickname] = useState(() => {
        const zapisanyNick = localStorage.getItem('user_nickname');
        if (zapisanyNick) {
            return zapisanyNick;
        }
        return "Użytkownik"; 
    });

    const [wzrost, setWzrost] = useState("180");
    const [waga, setWaga] = useState("80");
    const [asystentGlosowy, setAsystentGlosowy] = useState(true);
    const [buttonActive, setButtonActive] = useState(true);

    const wyloguj = () => {
        localStorage.removeItem('token');
        localStorage.removeItem('user_nickname');
        window.location.href = '/profil-logowanie';
    };

    return (
        <div className="profile-container">
            <h2 className="stats-header">Panel Dowodzenia</h2>

            <div className="profile-grid">
                {/* SEKCJA 1: WIZYTÓWKA */}
                <div className="profile-card">
                    <div className="avatar-placeholder">
                        {nickname.charAt(0).toUpperCase()}
                    </div>
                    <h3>{nickname}</h3>
                    <p className="status-badge">Konto Aktywne</p>
                    <button className="button-general-logout" onClick={wyloguj}>Wyloguj się</button>
                </div>

                {/* SEKCJA 2: BIOMETRIA I CELE */}
                <div className="profile-card">
                    <h3>Twoje Parametry</h3>
                    <div className="input-group">
                        <label>Wzrost (cm):</label>
                        <input 
                            type="number" 
                            value={wzrost} 
                            onChange={(e) => setWzrost(e.target.value)} 
                        />
                    </div>
                    <div className="input-group">
                        <label>Cel Wagi (kg):</label>
                        <input 
                            type="number" 
                            value={waga} 
                            onChange={(e) => setWaga(e.target.value)} 
                        />
                    </div>
                    <button className="button-general-blue">Zapisz parametry</button>
                </div>

                {/* SEKCJA 3: USTAWIENIA CYBERTRAINERA */}
                <div className="profile-card">
                    <h3>Ustawienia Aplikacji</h3>
                    <div className="toggle-group">
                        <label>Asystent Głosowy (trening):</label>
                        <button 
                            className={asystentGlosowy ? "toggle-btn active" : "toggle-btn"}
                            onClick={() => setAsystentGlosowy(!asystentGlosowy)}
                        >
                            {asystentGlosowy ? "WŁĄCZONY" : "WYŁĄCZONY"}
                        </button>
                    </div>
                    <div className="toggle-group" style={{marginTop: '20px'}}>
                        <label>Powiadomienia o suplementacji:</label>
                        <button className={buttonActive ? "toggle-btn active" : "toggle-btn"}
                        onClick={() => setButtonActive(!buttonActive)}
                        >
                            {buttonActive ? "WŁĄCZONY" : "WYŁĄCZONY"}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    );
}

export default ProfilZalogowany;