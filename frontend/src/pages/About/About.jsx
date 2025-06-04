import TeamMemberCard from "../../components/ui/TeamMemberCard";

function About() {
  const teamMembers = [
        {
            name: 'Christine',
            role: 'Product Manager, Frontend Developer',
            description:
                'Lorem ipsum dolor sit amet consectetur. Euismod quis diam elementum rhoncus dolor. Ut turpis commodo interdum quisque faucibus.'
        },
        {
            name: 'Dani',
            role: 'QA Developer',
            description:
                'Lorem ipsum dolor sit amet consectetur. Euismod quis diam elementum rhoncus dolor. Ut turpis commodo interdum quisque faucibus.'
        },
        {
            name: 'Enora',
            role: 'Backend Developer',
            description:
                'Lorem ipsum dolor sit amet consectetur. Euismod quis diam elementum rhoncus dolor. Ut turpis commodo interdum quisque faucibus.'
        },
        {
            name: 'Livia',
            role: 'UX/UI Designer, Frontend Developer',
            description:
                'Lorem ipsum dolor sit amet consectetur. Euismod quis diam elementum rhoncus dolor. Ut turpis commodo interdum quisque faucibus.'
        },
        {
            name: 'Wendi',
            role: 'Backend Developer, API',
            description:
                'Lorem ipsum dolor sit amet consectetur. Euismod quis diam elementum rhoncus dolor. Ut turpis commodo interdum quisque faucibus.'
        }
    ]

  return (
    <div className="Page">
      <div className="Page-header">About</div>
      <p>UBCCoursePlanner is meant to help students pick courses and electives for their degree. It offers 2 tools: </p>
      <p>1. Degree Tracker aims to help students ... </p>
      <p>2. Eligibility Tool aims to help students ... </p>
      <p>Disclaimer: UBCCoursePlanner is not affiliated with the University of British Columbia. UBC Course Planner is not responsible for...</p>

      <h1>Data</h1>
      <p>- Pre-requisite information is updated prior to course registration.</p>
      
      <h1>Motivation</h1>
      <p>Lorem ipsum dolor sit amet consectetur. Scelerisque pharetra ullamcorper dolor lacus justo vel. Facilisis vitae auctor aenean dictumst tincidunt malesuada. A nulla et neque eu odio faucibus mi pellentesque. Varius interdum scelerisque et pharetra eget nulla. Nec hac laoreet diam gravida consequat magnis egestas gravida. Egestas erat quis nunc dictum. Sed ipsum volutpat est nunc. Faucibus dolor etiam risus a sed cursus. Varius platea eget sem diam nec vulputate magna.</p>
      
      <h1>Meet the Team</h1>
      <div className="team-member-cards">
          {teamMembers.map((mem) => (
            <TeamMemberCard name={mem.name} role={mem.role} description={mem.description}></TeamMemberCard>
          ))}
      </div>
    </div>
  )
}

export default About;
