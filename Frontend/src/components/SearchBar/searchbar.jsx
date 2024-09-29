import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './searchbar.module.css'; // Import a CSS file for the search bar styles

const SearchBar = () => {
    const [query, setQuery] = useState('');
    const navigate = useNavigate();

    const handleSearch = (e) => {
        e.preventDefault();
        if (query.trim()) {
            navigate(`/lyrics/${query}`);
        }
    };

    return (
        <form onSubmit={handleSearch} className="search-form"> {/* Add a class for styling */}
            <input
                type="text"
                placeholder="Search for a song..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                className="search-input" // Add a class for styling
            />
            <button type="submit" className="search-button">Search</button>
        </form>
    );
};

export default SearchBar;
