import {useEffect} from 'react'
//Zdjecia

import headerImg from './assets/headerIMG.png'
import personIcon from './assets/personIcon.png'
//Ikony do bottom-navbar
import IkonaStronaGlowna from './icons/IkonaStronaGlowna';
import IkonaStatystyki from './icons/IkonaStatystyki';
import IkonaPerson from './icons/IkonaPerson';
//Formularz
import FormularzRejestracji from './pages/FormularzRejestracji';
import FormularzLogowania from './pages/FormularzLogowania';
//CSS
import './App.css'

function App() {
  //Pobiera aktualny adres strony do .active
  const aktualnyAdres = window.location.pathname;

  useEffect(()=> {
    if(window.location.pathname === '/'){
      window.location.replace('/strona-glowna');
    }
  }, []);

  let stronaDoWyswietlenia;
  if(aktualnyAdres==="/profil-rejestracja"){
    stronaDoWyswietlenia=<FormularzRejestracji/>
  }else if(aktualnyAdres==="/profil-logowanie"){
    stronaDoWyswietlenia=<FormularzLogowania/>
  }

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
            <li>
              <a href='/profil-logowanie'>
                Zaloguj się
              </a>
            </li>
            <li>
              <a href='/profil-rejestracja'>
                Zarejestruj sie
              </a>    
            </li>
          </ul>
        </div>
      </header>

      {stronaDoWyswietlenia}


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
              <a href='/strona-glowna' className={`nav-link ${aktualnyAdres === '/strona-glowna' ? 'active' : ''}`}>
                <IkonaStronaGlowna />
                <span>Strona głowna</span>
              </a>
            </li>
            <li>
              <a href='/profil-logowanie' className={`nav-link ${aktualnyAdres === '/profil-rejestracja' ? 'active' : ''}`}>
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
