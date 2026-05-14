import '../App.css'
import { useState } from 'react'

function FormularzRejestracji(){
    const [email, setEmail] = useState('');
    const [bladEmail, setBladEmail] = useState('');

    const aktualizujEmail = (wartosc) => {
        setEmail(wartosc);

        if(bladEmail !==''){
            setBladEmail('');
        }
    };

    const sprawdzEmail = () => {
        if(email===''){
            setBladEmail('');
            return;
            }

        const wzorEmaila = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if(!wzorEmaila.test(email)){
            setBladEmail('Podaj poprawy adres Email (np. jankowalski@gmail.com)');
        }else{
            setBladEmail('');
        }
    };

    const [haslo, setHaslo] = useState('');
    const [bladHaslo, setBladHaslo] = useState('');

    const aktualizujHaslo = (wartosc) => {
        setHaslo(wartosc);
        if(wartosc!==''){
            setBladHaslo('');
        }
    };
    
    const sprawdzHaslo = () => {
        if(haslo===''){
            setBladHaslo('');
            return;
        }

        const wzorHasla = /^(?=.*[A-Z])(?=.*\d)(?=.*$[!@#$%^&*_+]).{8,}$/;

        if(!wzorHasla.test(haslo)){
            setBladHaslo('Hasło musi mieć min. 8 znaków oraz zawierać co najmniej 1 wielką literę, 1 cyfrę i 1 znak specjalny');
        
        }else{
            setBladHaslo('')
        }
    };

    const wyslijFormularz = (e) => {
        e.preventDefault();

        sprawdzEmail();
        sprawdzHaslo();

        const wzorEmaila = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const wzorHasla = /^(?=.*[A-Z])(?=.*\d)(?=.*$[!@#$%^&*_+]).{8,}$/;

        if(!wzorEmaila.test(email) || !wzorHasla.test(haslo)){
            return;
        }
        alert("Zarejestrowano pomyślnie");

        setEmail('');
        setHaslo('')

    };

    return(
     <>
        <p className='generalFontP'>Formularz do rejestracji</p>
        <section className="forms">
            <form onSubmit={wyslijFormularz}>
                <label htmlFor="nick">Login:</label>
                <input type="text" id="nick" required maxLength={15}></input>

                <label htmlFor="email">E-mail:</label>
                <input 
                    type="text" 
                    id="email" 
                    required
                    value={email}
                    onChange={(e) => aktualizujEmail(e.target.value)}
                    onBlur={sprawdzEmail}
                />
                    
                {bladEmail && <span className='error-text'>{bladEmail}</span>}
                

                <label htmlFor="password">Hasło:</label>
                <input 
                    type="password" 
                    id="password" 
                    required
                    value={haslo}
                    onChange={(e) => aktualizujHaslo(e.target.value)}
                    onBlur={sprawdzHaslo}
                />

                {bladHaslo && <span className='error-text'>{bladHaslo}</span>}

                <label htmlFor="age">Wiek:</label>
                <input type="number" id="age" min="15" required></input>

                <p className='radio-label'>Ile razy w ciągu tygodnia trenujesz?</p>

                <div className='radio-group'>
                    <div className='radio-option'>
                        <input type='radio' id="beginner" name='numberOfTrenings' value="1-2" required></input>
                        <label htmlFor='beginner'>1-2 razy</label>
                    </div>
                    <div className='radio-option'>
                        <input type='radio' id="intermediate" name='numberOfTrenings' value="3-4" required></input>
                        <label htmlFor='intermediate'>3-4 razy</label>
                    </div>
                    <div className='radio-option'>
                        <input type='radio' id="advanced" name='numberOfTrenings' value="5+" required></input>
                        <label htmlFor='adwanced'>5 i więcej</label>
                    </div>
                </div>

                <button>Zarejestruj się</button>
            </form>
        </section>
    </>
    )
}
export default FormularzRejestracji