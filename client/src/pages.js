import React, { useState, useEffect } from 'react';
import Plot from 'react-plotly.js';

function Home() {
  const [todo, setTodo] = useState(null);

  useEffect(() => {
    fetch('https://jsonplaceholder.typicode.com/todos/1')
      .then(response => response.json())
      .then(data => setTodo(data));
  }, []);

  const generatePlot = () => {
    const data = [
      {
        x: ['Task'],
        y: [todo.completed ? 1 : 0],
        type: 'bar',
      },
    ];

    const layout = {
      title: 'Completed Task',
      xaxis: { title: 'Task' },
      yaxis: { title: 'Completed' },
    };

    return <Plot data={data} layout={layout} />;
  };

  return (
    <div>
      {todo ? (
        <div>
          <h2>{todo.title}</h2>
          <p>Completed: {todo.completed.toString()}</p>
          {generatePlot()}
        </div>
      ) : (
        <p>Loading...</p>
      )}
    </div>
  );
}

function About() {
  return <h1>About Page</h1>;
}

export { Home, About };
