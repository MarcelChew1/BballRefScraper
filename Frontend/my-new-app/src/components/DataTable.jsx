import React from 'react';
const colStyle = {
  minWidth: '75px',
  textAlign: 'center',
  height: '30px',
};

const DataTable = ({ playerData }) => {
  console.log(playerData)
  if (playerData.length === 0) return <div>No data available</div>;
  const { data, columnsOrder } = playerData;

  return (
    <div>
      <h1>Data Table</h1>
      <table>
        <thead>
          <tr>
            {columnsOrder.map((key, colIndex) => (
              <th 
                key={`header-${key}-${colIndex}`}
                style={{ ...colStyle, ...{ backgroundColor: colIndex % 2 === 0 ? '#f2f2f2' : '#ffffff' }}}
              >
                {key}
              </th>
            ))}
          </tr>
        </thead>
        <tbody>
          {data.map((row, rowIndex) => (
            <tr key={`row-${rowIndex}`}>
              {columnsOrder.map((key, colIndex) => (
                <td 
                  key={`${colIndex}-cell-${rowIndex}`}
                  style={{ ...colStyle, ...{ backgroundColor: colIndex % 2 === 0 ? '#f2f2f2' : '#ffffff' }}}
                >
                  {row[key]}
                </td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default DataTable;
