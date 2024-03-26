document.getElementById('examScheduleInput').addEventListener('change', function(event) {
  const file = event.target.files[0];
  const reader = new FileReader();

  reader.onload = function(e) {
    const csv = e.target.result;
    const processedData = processData(csv);
    displayData(processedData);
    createExamSchedule(processedData);
  };

  reader.readAsText(file);
});

function processData(csv) {
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
  data.forEach(row => {
    // console.log("Department:", row.department);
    // console.log("Class Number:", row.classNumber);
    // console.log("Course Code:", row.courseCode);
    // console.log("Number of Students:", row.numberOfStudents);
    // console.log("Lecturer:", row.lecturer);
    // console.log("Room:", row.room);
    // console.log("Day:", row.day);
    // console.log("Start Time:", row.startTime);
    // console.log("End Time:", row.endTime);
    // console.log("-----------------------------");
  });
}

count = 0;  

function translateDepartment(departmentName) {
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

  return turkishToEnglish[departmentName] || departmentName;
}

function createExamSchedule(data) {
  const departments = getDepartments(data);
  let countDayColor = 0;
  departments.forEach(department => {
    const classes = ['1.', '2.', '3.', '4.'];
    const schedule = createEmptySchedule();
    
    let html = `<p class="depName">${translateDepartment(department)}</p>`;
    html += '<table><tr style="background-color:#03043699;" ><th style="width: 13%;">DAYS</th><th style="width: 7%;">TIME</th>';
    for (let i = 0; i < 4; i++) {
      html += `<th style="width: 20%;">${classes[i]}</th>`;
    }
    html += '</tr>';
    const days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'];
    
    days.forEach((day) => {
      if (countDayColor % 2 == 0) {
        html += `<td style="background-color: #182b4fad;" rowspan="7">${day}</td><tr>`;
        for (let timeIndex = 0; timeIndex < 6; timeIndex++) {
          html += `<td style="background-color: #182b4fad;">${getTimeSlot(timeIndex)}</td>`;
        
        for (let classIndex = 0; classIndex < 4; classIndex++) {
          const suitableClass = findSuitableClass(schedule, data, department, day, timeIndex, classIndex);
          if (suitableClass) {
            html += `<td style="background-color: #182b4fad;">${suitableClass.courseCode} <br> ${suitableClass.room}</td>`;
            count++;
            for (let k = timeIndex; k < timeIndex + suitableClass.duration; k++) {
              schedule[k][classIndex] = suitableClass.courseCode;
            }
          } else {
            html += '<td style="background-color: #182b4fad;"></td>';
          }
        }
        html += '</tr>';
      }

    } else {
      html += `<td rowspan="7">${day}</td><tr>`;
      for (let timeIndex = 0; timeIndex < 6; timeIndex++) {
        html += `<td>${getTimeSlot(timeIndex)}</td>`;
      for (let classIndex = 0; classIndex < 4; classIndex++) {
        const suitableClass = findSuitableClass(schedule, data, department, day, timeIndex, classIndex);
        if (suitableClass) {
          html += `<td style="width: 20%;">${suitableClass.courseCode} <br> ${suitableClass.room}</td>`;
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
    document.getElementById('exam_schedule_table').innerHTML += html;
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
  let hour = Math.floor(slotIndex * 1.5) + 9;
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
  const departments = [];
  data.forEach(course => {
    if (!departments.includes(course.department)) {
      departments.push(course.department);
    }
  });
  return departments;
}


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
