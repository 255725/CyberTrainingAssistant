import '../App.css'
import { useState } from 'react'

function FormularzLogowania (){
    const [loginInput, setLoginInput] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');

    const obslugaLogowania = async (e) => {
        e.preventDefault();
        setError('')
        
        try{
            const response = await fetch('http://localhost:8000/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    Login: loginInput,
                    Password: password
                })
            });
            
            const data = await response.json();
            
            if(!response.ok){
                throw new Error(data.detail || "Błędne dane logowania");
            }

            localStorage.setItem('token', data.access_token);
            localStorage.setItem('user_nickname', data.user);

            alert(`Zalogowano pomyślnie jako: ${data.user}`);

            window.location.href = '/cwiczenia';
        }catch(err){
            setError(err.message);
        }
    };

    return(
        <>
            <p className="generalFontP">Formularz do logowania</p>
            <section className='forms'>
                {error && <p className='error-text' style={{ color: 'red', textAlign: 'center'}}>{error}</p>}

                <form onSubmit={obslugaLogowania}>
                    <label htmlFor='nick'>Login (NickName lub E-mail):</label>
                    <input 
                        type='text' 
                        id='nick' 
                        required 
                        maxLength={15}
                        value={loginInput}
                        onChange={(e) => setLoginInput(e.target.value)}
                    />
                    
                    <label htmlFor='password'>Hasło:</label>
                    <input 
                        type='password' 
                        id='password' 
                        required
                        value={password}
                        onChange={(e) => setPassword(e.target.value)}
                    />

                    <button type='submit'>Zaloguj się</button>

                    <p className='p-inside-form'>
                        Nie masz konta?
                        <a href='/profil-rejestracja'>  Zarejestruj się!</a>
                    </p>
                </form>
            </section>
        </>
    )
}
export default FormularzLogowania