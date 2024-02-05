<html>
<head>
    <!-- Include any necessary meta tags, stylesheets, or scripts here -->
</head>
<body>
    <h1>Congressional Legislation API Data Interactive Application 🦅</h1>
    <p>This project involved the collection, modification, and visualization of data on US Congressional Bills and Members. Data was collected from the Congressional API, and was collected/modified using Python. Javascript and HTML were used to create the application. 
      More information on the project can be found in the presentation PDF.</p>
    <h2>Files Included in this Repository 📁</h2>
    <ul>
        <li><code>Sample Data 📊</code> - Includes sample data collected from the Congressional API that can be viewed more easily and used in the code</li>
            <ul>
                <li><code>bills_with_details.json</code> - sample data on bills</li>
                <li><code>members_with_details.json</code> - sample data on congressional members</li>
            </ul>
        <li><code>backend 🐍</code> - Python files used in backend</li>
            <ul>
                <li><code>app.py</code> - simple Flask web application that provides various routes to retrieve information about members</li>
                <li><code>members.py</code> - defines a set of functions that return JSON responses indicating that graphs or information related to members are expected to be available at those points</li>
            </ul>
        <li><code>clients 🖥️</code> </li>
            <ul>
                <li><code>public</code> </li>
                    <ul>
                        <li><code>index.html</code> - basic structure of an HTML file for a web application</li>
                    </ul>
                <li><code>src</code> - </li>
                    <ul>
                        <li><code>App.js</code> - simple React application using the React Router library for navigation</li>
                        <li><code>index.js</code> - entry point of a React application</li>
                        <li><code>pages.js</code> - defines two React functional components, Home and About, which are components for two different pages in the React application</li>
                    </ul>
            </ul>
        <li><code>scripts 📜</code> </li>
            <ul>
                <li><code>data</code> </li>
                    <ul>
                        <li><code>bill_data_collection.py</code> - file used to API call and collect congressional bill data</li>
                        <li><code>congressperson_images.py</code> - file used to API call and collect congressperson data</li>
                        <li><code>member_data_collection.py</code> - file used to webscrape Wikipedia to collect congressperson photos</li>
                    </ul>
                <li><code>preprocessing</code> </li>
                    <ul>
                        <li><code>bill_length.py</code> - preprocessing data to find how long the bill was in Congress for</li>
                        <li><code>members.py</code> - preprocessing on member-related data</li>
                    </ul>
            </ul>
    </ul>
</body>
</html>

