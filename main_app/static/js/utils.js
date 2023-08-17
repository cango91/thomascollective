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

const formatDateWithTimezone = (inputDate) => {
  const timeZoneOffset = (new Date()).getTimezoneOffset();
  const offsetSign = timeZoneOffset > 0 ? "-" : "+";
  const offsetHours = String(Math.floor(Math.abs(timeZoneOffset) / 60)).padStart(2, '0');
  const offsetMinutes = String(Math.abs(timeZoneOffset) % 60).padStart(2, '0');
  const timezone = `${offsetSign}${offsetHours}:${offsetMinutes}`;
  return `${inputDate}T00:00:00${timezone}`;
}

const formatDateForDjango = (date, locale = 'en-US') => {
  const timeZone = Intl.DateTimeFormat().resolvedOptions().timeZone;
  const options = {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    timeZone: timeZone
  };
  const formattedDate = new Intl.DateTimeFormat(locale, options).format(date);

  // Split date and time
  const [month, day, year, ...timeParts] = formattedDate.match(/\d+/g);
  const time = timeParts.join(':');

  // Get timezone offset in the format +/-HH:MM
  const offset = (date.getTimezoneOffset() / 60).toFixed(2);
  const timeZoneOffset = `${offset < 0 ? '+' : '-'}${Math.abs(offset).toString().padStart(2, '0')}:00`;

  return `${year}-${month}-${day}T${time}${timeZoneOffset}`;
}
