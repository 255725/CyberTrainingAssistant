import { useState } from "react";
import personIcon from '../assets/personIcon.png';
import '../App.css'

function MenuUzytownika(){
    const [zalogowany, setZalogowany] = useState(() => !!localStorage.getItem('token'));
    const [nazwaUzytkownika, setNazwaUzytkownika] = useState(() => localStorage.getItem('user_nickname') || 'Użytkowniku');


    const wyloguj = (e) => {
        e.preventDefault();
        localStorage.removeItem('token');
        localStorage.removeItem('user_nickname');
        setZalogowany(false);
        setNazwaUzytkownika('');
        alert("Wylogowano");
        window.location.href = '/strona-glowna';
    };

    return (
        <div className="left-right-header">
            <img className="personIcon" src={personIcon} alt="Profil"/>
            ⌵
            <ul className='profilehamburger'>
                {zalogowany ? (
                    <>
                        <li className="user-greeting">
                            Witaj, {nazwaUzytkownika}!
                        </li>
                        <li>
                            <a href="/statystyki">Twoje statystyki</a>
                        </li>
                        <li>
                            <a href="#" onClick={wyloguj} className="logout-link">Wyloguj się</a>
                        </li>
                    </>
                ) : (
                    <>
                        <li>
                            <a href="/profil-logowanie">Zaloguj się</a>
                        </li>
                        <li>
                            <a href="/profil-rejestracja">Zarejestruj się</a>
                        </li>
                    </>
                )}
            </ul>
        </div>
    );
}

export default MenuUzytownika;