import React from 'react';
import { SearchBar } from '../components/SearchBar';
import { SummaryList } from '../components/SummaryList';
import Sidebar from '../components/Sidebar';

const HomePage = () => {
    return (
        <div className="home-page">
            <div className="main-content">
                <SearchBar />
                <SummaryList />
            </div>
            <Sidebar />
        </div>
    );
};

export default HomePage;
