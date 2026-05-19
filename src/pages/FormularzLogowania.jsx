import '../App.css'

function FormularzLogowania (){
    return(
        <>
            <p className="generalFontP">Formularz do logowania</p>
            <section className='forms'>
                <form>
                    <label htmlFor='nick'>Login:</label>
                    <input type='text' id='nick' required maxLength={15}></input>
                    
                    <label htmlFor='password'>Hasło:</label>
                    <input type='password' id='password' required></input>

                    <button>Zaloguj się</button>

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