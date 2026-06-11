import "../App.css"

function KartaInformacyjna({icon, title, descrie}){
    return(
        <div className="card-look">
            <img src={icon}/>
            <h3>{title}</h3>
            <p>{descrie}</p>
        </div>
    )
} export default KartaInformacyjna