import '../App.css'

function KartaCwiczen({icon, title, describe}){
    return(
        <>
            <div className='exercise-card-look'>
                <img src={icon}/>
                <h3>{title}</h3>
                <p>{describe}</p>
                <button className='button-general-blue'>
                    <a href='/cwiczenia'>
                        Rozpocznij ćwiczenie
                    </a>
                </button>
            </div>
        </>
    )
}
export default KartaCwiczen