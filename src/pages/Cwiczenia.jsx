import '../App.css'
import ExerciseCard from '../components/KartaCwiczen.jsx'
import wznosyHatnliBokiem from '../assets/exercise-icon/wznosyHantliBokiem.png'
import skokDosiezny from '../assets/exercise-icon/skokDosiezny.png'
import uginanieRamionZHantlami from '../assets/exercise-icon/uginanieRamionZHantlami.png'
function Cwiczenia (){
    return(
        <>
            <div className='excercise-card'>
                <ExerciseCard
                icon={wznosyHatnliBokiem}
                title='Wznosy hatli bokiem'
                describe='Stań stabilnie, trzymając hantle wzdłuż tułowia. 
                Utrzymując lekkie zgięcie w łokciach, unieś ramiona na boki do wysokości 
                barków. Powoli i pod pełną kontrolą opuść hantle do pozycji wyjściowej.'
                exerciseId="2"
                />
                <ExerciseCard
                icon={uginanieRamionZHantlami}
                title='Uginanie ramion z hantlami'
                describe='Stań stabilnie, trzymając hantle wzdłuż tułowia. 
                Utrzymując łokcie nieruchomo blisko ciała, ugnij ramiona, 
                unosząc hantle w kierunku barków. Powoli i pod pełną kontrolą 
                opuść hantle do pozycji wyjściowej.'
                exerciseId="1"
                />
                <ExerciseCard
                icon={skokDosiezny}
                title='Skok dosiężny'
                describe='Stań stabilnie ze stopami rozstawionymi na szerokość bioder. 
                Wykonaj dynamiczny zamach ramionami w dół schodząc do półprzysiadu, 
                a następnie wybij się mocno w górę, wyciągając ramię jak najwyżej. 
                Wyląduj miękko na ugiętych kolanach, w pełni amortyzując skok.'
                exerciseId="3"
                />
            </div>
            <div style={{ height: '120px', width: '100%' }}></div>
        </>
    )
}
export default Cwiczenia