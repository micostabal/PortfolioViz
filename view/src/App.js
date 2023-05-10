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
  Label
} from 'recharts';
import './App.css';

const BACKEND_URL = 'http://localhost:8000';
const START_DEFAULT = '2022-01-01';
const END_DEFAULT = new Date().toISOString().substring(0, 10);

const inventRandomColor = () => {
  return '#'+(Math.random() * 0xFFFFFF << 0).toString(16).padStart(6, '0');
}

const PortfoliosInput = (props) => {
  const {portfolios, onChange} = props;
  return (
    <>
      <label style={{marginLeft: '1em'}} for="portfolio">Choose a portfolio:</label>
      <select  style={{marginLeft: '1em'}} id="portfolio_id" name="portfolio" onChange={onChange}>
        {portfolios.map( ({name, id}) => {
          return (<option key={name} value={id}>{name}</option>)
        })}
      </select>
    </>
  )
}

const DateInput = ({name, max, min, onChange}) => {
  return (
    <>
      <label style={{marginLeft: '1em'}} for="dates">{name}:</label>
      <input
        style={{marginLeft: '1em'}}
        type="date"
        id="start"
        onChange={onChange}
        min={min ? min : START_DEFAULT}
        max={max ? max : END_DEFAULT}></input>
    </>
  )
}

const fetchPortfolios = async () => {
  return fetch(BACKEND_URL+'/portfolios/')
    .then(response => response.json());
}

const fetchPortfolioValues = async (portfolioId, startDate, endDate) => {
  return fetch(BACKEND_URL+
      `/portfolio/${portfolioId}/value?from=${startDate}&to=${endDate}`
    ).then(response => response.json())
}

const fetchWeightDistribution = async (portfolioId, startDate, endDate) => {
  return fetch(BACKEND_URL+
    `/portfolio/${portfolioId}/weights?from=${startDate}&to=${endDate}`)
    .then(response => response.json())
}

function App() {
  const [portfolioId, setPortfolioId] = useState(1);
  const [startDate, setStartDate] = useState(START_DEFAULT);
  const [endDate, setEndDate] = useState(END_DEFAULT);
  const [portfolios, setPortfolios] = useState([]);
  const [portfolioValues, setPortfolioValues] = useState([]);
  const [weights, setWeights] = useState([]);
  
  useEffect( () => {
    fetchPortfolios()
      .then( ({instances}) => {
        setPortfolios(instances);
      });
  }, []);
  
  useEffect(() => {
    fetchPortfolioValues(portfolioId, startDate, endDate)
      .then(function({values}) {
        setPortfolioValues(values);
      });
    fetchWeightDistribution(portfolioId, startDate, endDate)
      .then(function({weights}) {
        setWeights(weights);
      });
  }, [portfolioId, startDate, endDate]);

  const tickFormatter = (tickValue) => {
    const [year, month, day] = tickValue.split('-');
    return `${month} - ${year.substring(2, 4)}`;
  };
  
  return (
    <div style={{
        display: "flex", // TODO: Move to App.css file
        flexDirection: "column",
        justifyContent: "space-between",
        alignItems: "center",
        backgroundColor: '#D4ADFC'}}>

      <h1 className="custom-title">
        Portfolio Visualization
      </h1>

      <div className="custom-title" style={{ // TODO: Move to App.css file
          display: 'flex', 
          marginBottom: '1em',
          marginRight: '1em',
          flexDirection: "row",
          borderRadius: '1em',
          padding: '1em',
          borderColor: "#5C469C"  
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
        <h2 className="custom-title"> 
        Market value of Portfolio { portfolioId ? portfolioId : 1}
        </h2>
      </div>
      
      <div style={{
          width: "75%",
          alignSelf: "center",
          backgroundColor: "white",
          borderRadius: '1em',
          padding: '1em'}}>
        
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
                <YAxis tickCount={10} domain={[
                  750000000, // Harcoded, change
                  1050000000
                ]}></YAxis>
                <Legend />
                <Tooltip />
                <Line dataKey="amount"
                    stroke="black" dot={false}/>
            </LineChart>
        </ResponsiveContainer>
      </div>
      
      <div style={{width: "75%", alignSelf: "center"}}>
        <h2 className="custom-title"> 
          Distribution by weights
        </h2>
      </div>
      
      <div style={{
        display: "flex",
        flexDirection: "row",
        marginTop: '2em',
        justifyContent: "center",
        borderRadius: '1em',
        padding: '1em',
        backgroundColor: "white"
      }}>
        <div>
          <ResponsiveContainer width={720} aspect={1}>
            <AreaChart
              data={weights}
              margin={{ // TODO: Move to App.css file
                top: 10,
                right: 30,
                left: 0,
                bottom: 0,
              }}
            >
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="date"
                interval={ 32} angle={0}
                tickFormatter={tickFormatter}
                tick={{ fontSize: 8, lineHeight: 30 }}
              />
              <YAxis domain={[0, 1.0001]} />
              <Tooltip />
              {
                weights.length>0 ? Object.keys(weights[0])
                  .filter( key => key!=="date")
                  .map(key => {
                  const inventedColor = inventRandomColor();
                  return (<Area
                    type="monotone"
                    dataKey={key}
                    stackId="1"
                    stroke={inventedColor}
                    fill={inventedColor}
                  />)
                }) : null
              }
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </div>
      <div style={{height: '4em'}}>
      </div>
    </div>
  );
}

export default App;
