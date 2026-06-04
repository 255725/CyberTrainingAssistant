import '../App.css'
import PersonMain from '../assets/persona-strona-glowna.png'
import InformationCard from '../components/KartaInformacyjna'

//zdjecia
import dumbbellIcon from '../assets/main-page/dumbbellIcon.png'
import progressIcon from '../assets/main-page/progressIcon.png'
import skeletonIcon from '../assets/main-page/skeletonIcon.png'
import privacyIcon from '../assets/main-page/privacyIcon.png'

function StronaGlowna (){
    return(
        <>
            <section className='welcome'>
                <div className='welcome-text'>
                    <p className='main-p'>
                        Osiągnij swoją wymarzoną sylwetkę!
                    </p>
                    <p>Wirtualny Trener, który koryguje twoją technike na żywo!</p>
                    <div className='button-class'>
                        <button className='button-general-blue'>
                            <a href='profil-rejestracja'>
                                Załóż konto
                            </a>
                        </button>
                        <button className='button-general-white'>
                            <a href='cwiczenia-gosc'>
                                Wypróbuj jako gość
                            </a>
                        </button>
                    </div>
                </div>
                <div className='welcome-ikon'>
                    <img className='person-main-photo' src={PersonMain}/>
                </div>
            </section>

            <div className='information-card'>
                <InformationCard
                icon={dumbbellIcon}
                title="Różnorodny wybór ćwiczeń"
                descrie="Ćwiczenia z różnych dziedzin"
                />

                <InformationCard
                icon={skeletonIcon}
                title="Korygowanie Postawy na Żywo"
                descrie="Kamera AI w czasie rzeczywistym"
                />

                <InformationCard
                icon={progressIcon}
                title="Śledzenie postępów"
                descrie="Prowadzenie osiągnięć z danych ćwiczeń"
                />
            </div>

            <div className='information-privacy'>
                <img src={privacyIcon}/>
                <p>
                    <b>Twoja prywatność jest bezpieczna.</b> Analiza lokalna na urządzeniu, nie przesyłamy nigdzie obrazu z kamery!
                </p>
            </div>
        
        
        </>

    )
}export default StronaGlowna