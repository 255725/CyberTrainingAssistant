import { useState } from 'react'
//Zdjecia

import headerImg from './assets/headerIMG.png'
import personIcon from './assets/personIcon.png'
//Ikony do bottom-navbar
import IkonaKontakt from './icons/IkonaKontakt';
import IkonaStronaGlowna from './icons/IkonaStronaGlowna';
import IkonaStatystyki from './icons/IkonaStatystyki';
import IkonaPerson from './icons/IkonaPerson';
import IkonaTrening from './icons/IkonaTrening';
//CSS
import './App.css'

function App() {
  const [count, setCount] = useState(0)
  //Pobiera aktualny adres strony do .active
  const aktualnyAdres = window.location.pathname;

  return (
    <>
      <header className="navbar">
        <div className='left-right-header'>
          <img src={headerImg} className="base2" width="60" height="80" alt="logo stony"/>
          <p className="tekstHeader">WITRUALNY TRENER FITNESS</p>
        </div>
        <div className='left-right-header'>
          <img className='personIcon'src={personIcon}/>
          ⌵
          <ul className='profilehamburger'>
            <li>Zaloguj się</li>
            <li>Zarejestruj sie</li>
          </ul>
        </div>
      </header>
      <section id="center">
        <button
          type="button"
          className="counter"
          onClick={() => setCount((count) => count + 1)}
        >
          Count is {count}
        </button>
      </section>

      <div className="ticks"></div>

      <section id="next-steps">
       
      </section>
      <footer className='bottom-navbar'>
        <div className='nav-bottom-div'>
          <ul>
            <li>
              <a href='/statystyki' className={`nav-link ${aktualnyAdres === '/statystyki' ? 'active' : ''}`}>
              <IkonaStatystyki />
              <span>Statystki</span>
              </a>
            </li>
            <li>
              <a href='/trening' className={`nav-link ${aktualnyAdres === '/trening' ? 'active' : ''}`}>
                <IkonaTrening />
                <span>Treningi</span>
              </a>
            </li>
            <li>
              <a href='/strona-glowna' className={`nav-link ${aktualnyAdres === '/strona-glowna' ? 'active' : ''}`}>
                <IkonaStronaGlowna />
                <span>Strona głowna</span>
              </a>
            </li>
            <li>
              <a href='/pomoc' className={`nav-link ${aktualnyAdres === '/pomoc' ? 'active' : ''}`}>
                <IkonaKontakt />
                <span>Kontakt</span>
              </a>
            </li>
            <li>
              <a href='/profil' className={`nav-link ${aktualnyAdres === '/profil' ? 'active' : ''}`}>
                <IkonaPerson />
                <span>Profil</span>
              </a>
            </li>
          </ul>
        </div>
      </footer>
    </>
  )
}

export default App
