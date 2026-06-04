import { useState } from 'react'
import '../App.css'


function KartaCwiczen({icon, title, describe, exerciseId}){
    const[isCameraActive, setIsCameraActive] = useState(false);

    const wlaczKamere = () => setIsCameraActive(true);
    const wylaczKamere = async () => {
        setIsCameraActive(false);

        try{
            await fetch('http://localhost:8000/api/stop-exercise', {
                method: 'POST'
            });
            console.log("Wysłano sygnał zatrzymania kamer.");
        }catch (error){
            console.error("Błą podczas wyłączania kamer:", error)
        }
    };

    return(
        <>
            <div className='exercise-card-look'>
                <img src={icon}/>
                <h3>{title}</h3>
                <p>{describe}</p>
                <button className='button-general-blue' onClick={wlaczKamere}>
                    Rozpocznij ćwiczenie
                </button>
            </div>

            {isCameraActive && (
                <div className='fullscreen-video-overlay'>
                    <button className='close-video-btn' onClick={wylaczKamere}>
                        Zakończ trening (X)
                    </button>
                    <img 
                        src={`http://localhost:8000/api/video-stream/${exerciseId}`} 
                        alt="Kamera Treningowa"
                        className="fullscreen-video-stream"
                    />
                </div>
            )

            }
        </>
    )
}
export default KartaCwiczen