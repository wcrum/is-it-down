import React from 'react';
import logo from './logo.svg';
import './App.css';
import Button from '@mui/material/Button';

import { render } from "react-dom";
import {
	BrowserRouter,
	Routes,
	Route
} from "react-router-dom";

export const App = () => {
	return (
		<BrowserRouter>
		<Routes>
			<Route path="/" element={<main> home </main> }/>
			<Route path="/catagories" element={ <main> test 2</main>} />
		</Routes>
		</BrowserRouter>
	);
}

export default App;
