import '../App.css'
import { useState } from 'react'

function FormularzRejestracji(){
    const [nickname, setNickname] = useState('')
    const [email, setEmail] = useState('');
    const [haslo, setHaslo] = useState('')
    const [age, setAge] = useState('')
    const [adavancement, setAdvancement] = useState('')
    
    const [bladEmail, setBladEmail] = useState('');
    const [bladHaslo, setBladHaslo] = useState('');
    const [bladOgolny, setBladOgolny] = useState('');

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

        const wzorHasla = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*_+]).{8,}$/;

        if(!wzorHasla.test(haslo)){
            setBladHaslo('Hasło musi mieć min. 8 znaków oraz zawierać co najmniej 1 wielką literę, 1 cyfrę i 1 znak specjalny');
        
        }else{
            setBladHaslo('')
        }
    };

    const wyslijFormularz = async (e) => {
        e.preventDefault();

        sprawdzEmail();
        sprawdzHaslo();

        const wzorEmaila = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const wzorHasla = /^(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*_+]).{8,}$/;

        if(!wzorEmaila.test(email) || !wzorHasla.test(haslo)){
            return;
        }

        try{
            const response = await fetch('http://localhost:8000/register', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    Nickname: nickname,
                    Email: email,
                    Password: haslo,
                    Age: parseInt(age),
                    IDGender: 1,
                    IDAdvancement: parseInt(adavancement)
                })
            });

            const data = await response.json()

            if (!response.ok){
                throw new Error(data.detail || 'Błąd podczas rejestracji')
            }
            alert("Zarejestrowano pomyślnie! Możesz się teraz zalogować.");

            setNickname('')
            setEmail('')
            setHaslo('')
            setAge('')
        } catch (err){
            setBladOgolny(err.message);
        }

    };

    return(
     <>
        <p className='generalFontP'>Formularz do rejestracji</p>
        <section className="forms">
            {bladOgolny && <p className='error-text' style={{color: 'red', textAlign: 'center'}}>{bladOgolny}</p>}
            <form onSubmit={wyslijFormularz}>
                <label htmlFor="nick">Login:</label>
                <input 
                    type="text" 
                    id="nick" 
                    required 
                    maxLength={15}
                    value={nickname}
                    onChange={(e) => setNickname(e.target.value)}
                />

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
                <input 
                    type="number" 
                    id="age" 
                    min="15" 
                    required
                    value={age}
                    onChange={(e) => setAge(e.target.value)}
                />

                <p className='radio-label'>Ile razy w ciągu tygodnia trenujesz?</p>

                <div className='radio-group'>
                    <div className='radio-option'>
                        <input 
                            type='radio' 
                            id="beginner" 
                            name='numberOfTrenings' 
                            value={1}
                            checked={adavancement === 1}
                            onChange={() => setAdvancement(1)}
                            required
                        />
                        <label htmlFor='beginner'>1-2 razy</label>
                    </div>
                    <div className='radio-option'>
                        <input 
                            type='radio' 
                            id="intermediate" 
                            name='numberOfTrenings' 
                            value={2}
                            checked={adavancement === 2}
                            onChange={() => setAdvancement(2)}
                            required
                        />
                        <label htmlFor='intermediate'>3-4 razy</label>
                    </div>
                    <div className='radio-option'>
                        <input 
                            type='radio' 
                            id="advanced" 
                            name='numberOfTrenings' 
                            value={3}
                            checked={adavancement === 3} 
                            required
                        />
                        <label htmlFor='adwanced'>5 i więcej</label>
                    </div>
                </div>

                <button type='submit'>Zarejestruj się</button>
                <p className='p-inside-form'>
                    Masz już konto?
                    <a href='/profil-logowanie'> Zaloguj się!</a>
                </p>
            </form>
        </section>
    </>
    )
}
export default FormularzRejestracji