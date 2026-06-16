import { useState } from 'react'
import '../App.css'


function KartaCwiczen({icon, title, describe, exerciseId}){
    const[isCameraActive, setIsCameraActive] = useState(false);

    const [showWeightModel, setShowWeightModel] = useState(false);
    const [currentWeight, setCurrentWeight] = useState('')
    const [repCount, setRepCount] = useState(0);
    const [jumpHeight, setJumpHeight] = useState(0);

    const wlaczKamere = () => setIsCameraActive(true);
    const wylaczKamere = async () => {
        setIsCameraActive(false);
        try{
            const stopResponse = await fetch(`http://localhost:8000/api/stop-exercise/${exerciseId}`, {
                method: 'POST'
            });
            const stopData = await stopResponse.json();
            console.log("Kamera wyłączona. Odebrane dane:", stopData);

            setRepCount(stopData.powtorzenia || 0);
            setJumpHeight(stopData.jumpHeight || 0);
            setShowWeightModel(true);
            
        }catch (error){
            console.error("Błąd podczas wyłączania kamer:", error)
        }
    };
    const zapiszWynikDoBazy = async () => {
        const token = localStorage.getItem('token');
        if(!token && (
            <p style={{fontSize: '0.8em', color: 'gray'}}>
                Zaloguj się, aby zapisywać postępy!
            </p>
        )){
            alert('Trening zakończony! (Nie jesteś zalogowany, wynik nie został zapisany w bazie)');
            setShowWeightModel(false);
            return;
        }

        const daneTreningu = {
            IDExercise: exerciseId,
            RepCount: repCount,
            Weight: parseInt(exerciseId) === 3 ? 0.0 : parseFloat(currentWeight) || 0.0,
            JumpHeight: parseInt(exerciseId) === 3 ? jumpHeight : 0.0
        };

        try {
            const odpowiedzBazy = await fetch('http://localhost:8000/stats', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify(daneTreningu)
            });

            if(odpowiedzBazy.ok){
                alert('Świetna robota! Wynik został zapisany');
            }else{
                console.log("Błąd zapisu w bazie");
            }
        }catch (error){
            console.error("Błąd sieci:", error);
        }

        setShowWeightModel(false);
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
            )}
            {showWeightModel && (
                <div className='modal-overlay'>
                    <div className='weight-modal'>
                        <h3>Trening zakończony!</h3>
                        <p>Policzono: {repCount} powtórzeń</p>

                        {parseInt(exerciseId) === 3 ? (
                            <p>Twój najwyższy skok: <b>{jumpHeight} cm</b></p>
                        ) : (
                            <input
                                type="number"
                                placeholder='Podaj wagę (kg)'
                                value={currentWeight}
                                onChange={(e) => setCurrentWeight(e.target.value)}
                            />
                        )}

                        <button className='button-general-blue' onClick={zapiszWynikDoBazy}>
                            Zapisz wynik
                        </button>
                    </div>
                </div>
            )}
        </>
    )
}
export default KartaCwiczen