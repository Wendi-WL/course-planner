// frontend/src/components/CourseTable.js (or wherever your component is)

import React, { useState, useEffect } from 'react';

function CourseTable() {
    const [courses, setCourses] = useState([]); // State to store fetched course data
    const [loading, setLoading] = useState(true); // State to track loading status
    const [error, setError] = useState(null); // State to track any errors

    useEffect(() => {
        const fetchCourses = async () => {
            try {
                const response = await fetch('http://127.0.0.1:8000/api/courses/');
                if (!response.ok) {
                    throw new Error(`HTTP error! status: ${response.status}`);
                }
                const data = await response.json();
                setCourses(data);
            } catch (error) {
                setError(error);
                console.error("Error fetching courses:", error);
            } finally {
                setLoading(false); // Set loading to false once fetching is done (success or error)
            }
        };

        fetchCourses();
    }, []); // Empty dependency array means this effect runs once after the initial render

    if (loading) {
        return <div>Loading courses...</div>;
    }

    if (error) {
        return <div>Error: {error.message}</div>;
    }

    return (
        <div>
            <h2>Course Catalog</h2>
            <table>
                <thead>
                    <tr>
                        <th>Subject</th>
                        <th>Code</th>
                        <th>Name</th>
                        <th>Credits</th>
                    </tr>
                </thead>
                <tbody>
                    {courses.map(course => (
                        <tr key={course.id}> {/* Use a unique key for each row */}
                            <td>{course.subject}</td>
                            <td>{course.code}</td>
                            <td>{course.name}</td>
                            <td>{course.credit}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}

export default CourseTable;