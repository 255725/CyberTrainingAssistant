import "../App.css"

function StatystykiUzytkownika(){
    return(
        <>
            <div>
                <div className="statistic-text">
                    <p>Aby wyświetlić informacje o swoich statystykach musisz być ZALOGOWANY!</p>
                    <div className="button-class">
                        <button className="button-general-blue">
                            <a href="/profil-logowanie">Przejdź do logowania</a>
                        </button>
                        <button className="button-general-blue">
                            <a href="/profil-rejestracja">Przejdź do rejestracji</a>
                        </button>
                    </div>
                </div>
            </div>
        </>
    )
}
export default StatystykiUzytkownika