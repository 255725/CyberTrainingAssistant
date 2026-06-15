import {useEffect} from 'react'
//Zdjecia
import headerImg from './assets/headerIMG.png'
//Ikony do bottom-navbar
import IkonaStronaGlowna from './icons/IkonaStronaGlowna';
import IkonaStatystyki from './icons/IkonaStatystyki';
import IkonaPerson from './icons/IkonaPerson';
//Formularze
import FormularzRejestracji from './pages/FormularzRejestracji';
import FormularzLogowania from './pages/FormularzLogowania';
//Komponenty
import MenuUzytownika from './components/MenuUzytkownika';
//CSS
import './App.css'
//Podstrony
import StronaGlowna from './pages/StronaGlowna';
import Cwiczenia from './pages/Cwiczenia';

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
  }else if(aktualnyAdres==="/strona-glowna"){
    stronaDoWyswietlenia=<StronaGlowna/>
  }else if(aktualnyAdres==="/cwiczenia-gosc"){
    stronaDoWyswietlenia=<Cwiczenia/>
  }

  return (
    <>
      <header className="navbar">
        <div className='left-right-header'>
          <img src={headerImg} className="base2" width="60" height="80" alt="logo stony"/>
          <p className="tekstHeader">WITRUALNY TRENER FITNESS</p>
        </div>
        <MenuUzytownika />
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
              <a href='/profil-logowanie' className={`nav-link ${aktualnyAdres === '/profil-rejestracja' || aktualnyAdres ==='/profil-logowanie' ? 'active' : ''}`}>
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
