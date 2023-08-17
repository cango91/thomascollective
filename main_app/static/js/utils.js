const getDate = date =>{
    date = new Date(date);
    return `${(date.getMonth()+1).toString().padStart(2,'0')}/${date.getDate().toString().padStart(2,'0')}/${date.getFullYear()}`;
}

const getDatetime = date => {
  const localDate = new Date(date);
  const options = { 
      year: 'numeric', 
      month: '2-digit', 
      day: '2-digit', 
      hour: '2-digit', 
      minute: '2-digit',
      hour12: false,
      timeZoneName: 'short'
  };
  
  const formattedDatetime = localDate.toLocaleString(undefined, options);
  return formattedDatetime;
};