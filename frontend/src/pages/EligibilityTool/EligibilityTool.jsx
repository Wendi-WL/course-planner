import CourseTable from '../../components/CourseTable/CourseTable'; 

function EligibilityTool() {
  return (
    <div>
      <h2>buffer</h2> {/* temporary to make it show beyond header, currently blocked */}
      <h1>Eligibility Tool</h1>
      <CourseTable /> {/* This renders the CourseTable component */}
    </div>
  );
}
export default EligibilityTool;
