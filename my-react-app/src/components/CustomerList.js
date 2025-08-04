import React, { useState, useEffect } from "react";

const CustomerList = () => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [searchTerm, setSearchTerm] = useState("");

    useEffect(() => {
        fetch("http://localhost:8000/users")
            .then((response) => response.json())
            .then((data) => {
                setUsers(data);
                setLoading(false);
            })
            .catch((error) => {
                console.error("Error fetching users:", error);
                setLoading(false);
            });
    }, []);

    const handleSearch = (event) => {
        setSearchTerm(event.target.value);
    };

    const filteredUsers = users.filter((user) => 
        user.name.toLowerCase().includes(searchTerm.toLowerCase()) || 
        user.email.toLowerCase().includes(searchTerm.toLowerCase())
    );

    if (loading) {
        return <div>Loading...</div>;
    }

    return (
        <div>
            <h1>Customer List</h1>
            <div style={{ marginBottom: "20px" }}>
                <input
                    type="text"
                    placeholder="Search by name or email"
                    value={searchTerm}
                    onChange={handleSearch}
                    style={{
                        padding: "8px",
                        width: "300px",
                        borderRadius: "4px",
                        border: "1px solid #ccc"
                    }}
                />
            </div>
            {filteredUsers.length > 0 ? (
                <ul>
                    {filteredUsers.map((user) => (
                        <li key={user.id}>
                            {user.name} - {user.email}
                        </li>
                    ))}
                </ul>
            ) : (
                <p>No customers found matching your search.</p>
            )}
        </div>
    );
}

export default CustomerList;