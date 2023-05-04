
import React, { useEffect, useState } from 'react';
import {
  AreaChart,
  Area,
  XAxis,
  YAxis, 
  CartesianGrid,
  Tooltip,
  LineChart,
  ResponsiveContainer,
  Legend,
  Line,
  Label // linted as unnecessary, yet required
} from 'recharts';
import './App.css';

const BACKEND_URL = 'http://localhost:8000';
const START_DEFAULT = '2022-01-01';
const END_DEFAULT = new Date().toISOString().substring(0, 10);

const PortfoliosInput = (props) => {
  const {portfolios, onChange} = props;
  return (
    <>
      <label style={{marginLeft: '1em'}} for="portfolio">Choose a portfolio:</label>
      <select  style={{marginLeft: '1em'}} id="portfolio_id" name="portfolio" onChange={onChange}>
        {portfolios.map( portfolio => {
          return (<option key={portfolio.name} value={portfolio.id}>{portfolio.name}</option>)
        })}
      </select>
    </>
  )
}

const DateInput = ({name, max, min, onChange}) => {
  return (
    <>
      <label style={{marginLeft: '1em'}} for="cars">{name}:</label>
      <input
        style={{marginLeft: '1em'}}
        type="date"
        id="start"
        name="viz-start"
        onChange={onChange}
        min={min ? min : START_DEFAULT}
        max={max ? max : END_DEFAULT}></input>
    </>
  )
}

function App() {
  const [portfolioId, setPortfolioId] = useState(1);
  const [startDate, setStartDate] = useState(START_DEFAULT);
  const [endDate, setEndDate] = useState(END_DEFAULT);
  const [portfolios, setPortfolios] = useState([]);
  const [portfolioValues, setPortfolioValues] = useState([]);
  
  const data = [
    {
      name: 'Page A',
      uv: 4000,
      pv: 2400,
      amt: 2400,
    },
    {
      name: 'Page B',
      uv: 3000,
      pv: 1398,
      amt: 2210,
    },
    {
      name: 'Page C',
      uv: 2000,
      pv: 9800,
      amt: 2290,
    },
    {
      name: 'Page D',
      uv: 2780,
      pv: 3908,
      amt: 2000,
    },
    {
      name: 'Page E',
      uv: 1890,
      pv: 4800,
      amt: 2181,
    },
    {
      name: 'Page F',
      uv: 2390,
      pv: 3800,
      amt: 2500,
    },
    {
      name: 'Page G',
      uv: 3490,
      pv: 4300,
      amt: 2100,
    },
    
  ];

  useEffect( () => {
    fetch(BACKEND_URL+'/portfolios/')
      .then(response => response.json())
      .then( ({instances}) => {
        setPortfolios(instances);
      })
  }, []);
  
  useEffect(() => {
    fetch(BACKEND_URL+`/portfolio/${portfolioId}/value?from=${startDate}&to=${endDate}`)
      .then( response => response.json())
      .then(function({values}) {
        setPortfolioValues(values);
      }).catch(function(err) {
        console.log('Fetch Error :-S', err);
      })
  }, [portfolioId, startDate, endDate]);

  const tickFormatter = (tickValue) => {
    const [year, month, day] = tickValue.split('-');
    return `${month} - ${year.substring(2, 4)}`;
  };
  
  return (
    <div style={{display: "flex", flexDirection: "column", justifyContent: "space-between", alignItems: "center"}}>
      <h1 className="text-heading">
        Portfolio Visualization
      </h1>

      <div style={{
          display: 'flex', 
          marginBottom: '1em',
          marginRight: '1em',
          flexDirection: "row"
        }}>
        <PortfoliosInput portfolios={portfolios} onChange={(selection) => {
          setPortfolioId(selection.target.value);
        }} />
        <DateInput name={"Start"} max={endDate} onChange={(newValue) => {
          setStartDate(newValue.target.value);
        }}/>
        <DateInput name={"End"} min={startDate} onChange={(newValue) => {
          setEndDate(newValue.target.value);
        }}/>
      </div>
      
      <div style={{width: "75%", alignSelf: "center"}}>
        <h2 className="text-heading">
          Market value of Portfolio { portfolioId ? portfolioId : 1}
        </h2>
        <ResponsiveContainer width="100%" aspect={2}>
            <LineChart data={portfolioValues}
              margin={{ left: 50, right: 50, bottom: 50 }}
              padding={{bottom: 100}}>
                <CartesianGrid />
                <XAxis dataKey="date" 
                  interval={ 32} angle={0}
                  tickFormatter={tickFormatter}
                  tick={{ fontSize: 8, lineHeight: 30 }}
                  margin={{top: 3, bottom: 30}}>
                </XAxis>
                <YAxis tickCount={10}></YAxis>
                <Legend />
                <Tooltip />
                <Line dataKey="amount"
                    stroke="black" dot={false}/>
            </LineChart>
        </ResponsiveContainer>
      </div>

      <div style={{width: "75%", alignSelf: "center"}}>
        <h2 className="text-heading">
          Distribution by weights
        </h2>
      </div>
      
      <div style={{
        display: "flex",
        flexDirection: "row",
        marginTop: '2em',
        justifyContent: "center"
      }}>
        <div>
          <ResponsiveContainer width={720} aspect={1}>
            <AreaChart
              data={data}
              margin={{
                top: 10,
                right: 30,
                left: 0,
                bottom: 0,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Area type="monotone" dataKey="uv" stackId="1" stroke="#8884d8" fill="#8884d8" />
              <Area type="monotone" dataKey="pv" stackId="1" stroke="#82ca9d" fill="#82ca9d" />
              <Area type="monotone" dataKey="amt" stackId="1" stroke="#ffc658" fill="#ffc658" />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}

export default App;
