// document.getElementById('examScheduleInput').addEventListener('change', function(event) {
//   const file = event.target.files[0];
//   const reader = new FileReader();

//   reader.onload = function(e) {
//     const csv = e.target.result;
//     const processedData = processData(csv);
//     displayData(processedData);
//     createExamSchedule(processedData);
//   };

//   reader.readAsText(file);
// });

function loadSchedule() {
  fetch('/get_csv')  
    .then(response => response.text())  
    .then(data => {
      const processedData = processData(data);  // Process the fetched CSV data
      displayData(processedData);  // Display the processed data
      createExamSchedule(processedData);  // Use the processed data to create an exam schedule
        })
    .catch(error => {
      console.error("Error loading CSV:", error);  // Log errors if any during the fetch process
    });
}

function processData(csv) {
  // console.log(csv);
  // Parse CSV data into structured format
  const rows = csv.split('\n');
  const data = [];
  for (let i = 1; i < rows.length; i++) {
    const row = rows[i].split(',');
    const department = row[0];
    const classNumber = row[1];
    const courseCode = row[2];
    const numberOfStudents = row[3];
    const lecturer = row[4];
    const room = row[5];
    const day = row[6];
    const startTime = row[7];
    const endTime = row[8];
    if (department && classNumber && courseCode && numberOfStudents && lecturer && room && day && startTime && endTime) {
      data.push({
        department,
        classNumber,
        courseCode,
        numberOfStudents,
        lecturer,
        room,
        day,
        startTime,
        endTime
      });
    }
  }

  return data;
}



function displayData(data) {
   // Log each row of processed data
  data.forEach(row => {
    console.log("Department:", row.department);
    console.log("Class Number:", row.classNumber);
    console.log("Course Code:", row.courseCode);
    console.log("Number of Students:", row.numberOfStudents);
    console.log("Lecturer:", row.lecturer);
    console.log("Room:", row.room);
    console.log("Day:", row.day);
    console.log("Start Time:", row.startTime);
    console.log("End Time:", row.endTime);
    console.log("-----------------------------");
  });
}

count = 0;  

function translateDepartment(departmentName) {
  // Map Turkish department names to English
  const turkishToEnglish = {
    "İNŞAAT MÜH.(İNG)": "Civil Engineering",
    "ENDÜSTRİ MÜH.": "Industrial Engineering",
    "BİLGİSAYAR MÜH.": "Computer Engineering",
    "MET. VE MALZ. MÜH.": "Metallurgical and Materials Engineering",
    "MAKİNE MÜH.": "Mechanical Engineering",
    "MATEMATİK": "Mathematics",
    "ELEKTRİK-ELEKTRONİK  MÜH.": "Electrical-Electronics Engineering",
    "ENERJİ SİS. MÜH.": "Energy Systems Engineering",
    "YAZILIM MÜH.": "Software Engineering"
  };

  return turkishToEnglish[departmentName] || departmentName; // Return the translated name or the original if not found
}

function createExamSchedule(data) {
  // Generate HTML for exam schedule display
  const departments = getDepartments(data);  // Retrieve unique departments from data
  let countDayColor = 0;  // To alternate row colors in the table
  departments.forEach(department => {
    const classes = ['1.', '2.', '3.', '4.'];
    const schedule = createEmptySchedule();  // Create an empty schedule grid
    
    let html = `<p class="depName">${translateDepartment(department)}</p>`;
    html += '<table><tr style="background-color:#03043699;" ><th style="width: 13%;">DAYS</th><th style="width: 7%;">TIME</th>';
    for (let i = 0; i < 4; i++) {
      html += `<th style="width: 20%;">${classes[i]}</th>`;
    }
    html += '</tr>';
    const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    
    days.forEach((day) => {
      // Alternate row color logic
      if (countDayColor % 2 == 0) {
        // Specific day row setup
        html += `<td style="background-color: #182b4fad;" rowspan="7">${day}</td><tr>`;
        for (let timeIndex = 0; timeIndex < 6; timeIndex++) {
          html += `<td style="background-color: #182b4fad;">${getTimeSlot(timeIndex)}</td>`;
        
        for (let classIndex = 0; classIndex < 4; classIndex++) {
          const suitableClass = findSuitableClass(schedule, data, department, day, timeIndex, classIndex);
          if (suitableClass) {
            html += `<td style="background-color: #182b4fad;">${suitableClass.courseCode} (${suitableClass.numberOfStudents}) <br> ${suitableClass.room}</td>`;
            count++;
            for (let k = timeIndex; k < timeIndex + suitableClass.duration; k++) {
              schedule[k][classIndex] = suitableClass.courseCode; // Mark time slots in the schedule as occupied
            }
          } else {
            html += '<td style="background-color: #182b4fad;"></td>';
          }
        }
        html += '</tr>';
      }

    } else {
      // Non-colored row setup
      html += `<td rowspan="7">${day}</td><tr>`;
      for (let timeIndex = 0; timeIndex < 6; timeIndex++) {
        html += `<td>${getTimeSlot(timeIndex)}</td>`;
      for (let classIndex = 0; classIndex < 4; classIndex++) {
        const suitableClass = findSuitableClass(schedule, data, department, day, timeIndex, classIndex);
        if (suitableClass) {
          html += `<td style="width: 20%;">${suitableClass.courseCode} (${suitableClass.numberOfStudents}) <br> ${suitableClass.room}</td>`;
          count++;
          for (let k = timeIndex; k < timeIndex + suitableClass.duration; k++) {
            schedule[k][classIndex] = suitableClass.courseCode;
          }
        } else {
          html += '<td></td>';
        }
      }
      html += '</tr>';
    }
    }
    countDayColor++;
  
    
  });

  html += '</table>';
    document.getElementById('examScheduleTable').innerHTML += html;
  });
  document.getElementById('count').innerHTML = count + " exams scheduled.";
}

function createEmptySchedule() {
  const schedule = [];
  for (let i = 0; i < 36; i++) {
    schedule.push(['', '', '', '']);
  }
  return schedule;
}

function getTimeSlot(slotIndex) {
  // Calculate the start time for a given time slot index
  let hour = Math.floor(slotIndex * 1.5) + 9; // Start at 9:00 and go in half-hour increments
  const minute = (slotIndex % 2 === 0) ? '00' : '30';
  
  if (hour < 10) {
    hour = `0${hour}`;
  }
  return `${hour}.${minute}`;
}

function getEndTime(currentTime) {
  const [hour, minute] = currentTime.split('.').map(Number);
  const totalMinutes = hour * 60 + minute + 90;
  const newHour = Math.floor(totalMinutes / 60); 
  const newMinute = totalMinutes % 60;
  return `${newHour}.${newMinute < 10 ? '0' + newMinute : newMinute}`;
}

function getDepartments(data) {
  // Extract a unique list of departments from the data
  const departments = [];
  data.forEach(course => {
    if (!departments.includes(course.department)) {
      departments.push(course.department);
    }
  });
  return departments;
}

// Find an available class from the data that fits the current schedule slot
function findSuitableClass(schedule, data, department, day, timeSlotIndex, classIndex) {
  const currentTime = getTimeSlot(timeSlotIndex);
  const currentDay = day;
  const suitableClasses = data.filter(course => 
    course.department === department &&
    course.day === currentDay &&
    course.startTime === currentTime &&
    course.endTime >= getEndTime(currentTime) &&
    course.classNumber === (classIndex + 1).toString()
  );
  for (const suitableClass of suitableClasses) {
    return suitableClass;
  }
  return null;
}
