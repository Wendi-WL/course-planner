const TeamMemberCard = ({ name,role,description }) =>{
  return (
    <div className='team-member-card'>
        <h2>{name}</h2>
        <h3>{role}</h3>
        <p>{description}</p>
    </div>
  )
}

export default TeamMemberCard;