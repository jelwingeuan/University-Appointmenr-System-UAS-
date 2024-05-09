document.addEventListener("DOMContentLoaded", function () {
  const passwordField = document.getElementById("passwordField");
  const showPasswordCheckbox = document.getElementById("showPasswordCheckbox");

  showPasswordCheckbox.addEventListener("change", function () {
    if (showPasswordCheckbox.checked) {
      passwordField.type = "text";
    } else {
      passwordField.type = "password";
    }
  });
});

function printInvoice(){
    window.print();
}

document.addEventListener("DOMContentLoaded", function() {
  setTimeout(function() {
      document.querySelector(".messagecontainer").classList.add("active");
  }, 100); // Adjust the delay as needed
});


//Graph for admin
document.addEventListener("DOMContentLoaded", function() {
  setTimeout(function() {
      document.querySelector(".messagecontainer").classList.add("active");
  }, 100); // Adjust the delay as needed

  // Data for the bar chart
  const barChartData = {
      labels: ['Student', 'Lecturer', 'Appointment', 'User'],
      datasets: [{
          label: 'Data',
          backgroundColor: ['rgba(255, 99, 132, 0.5)', // Red
                           'rgba(54, 162, 235, 0.5)', // Blue
                           'rgba(255, 206, 86, 0.5)', // Yellow
                           'rgba(75, 192, 192, 0.5)'], // Green
          borderColor: ['rgba(255, 99, 132, 1)', // Red
                        'rgba(54, 162, 235, 1)', // Blue
                        'rgba(255, 206, 86, 1)', // Yellow
                        'rgba(75, 192, 192, 1)'], // Green
          borderWidth: 1,
          data: [54, 65, 20, 120]
      }]
  };

  // Additional chart configuration options for the bar chart
  const barChartOptions = {
      scales: {
          yAxes: [{
              ticks: {
                  beginAtZero: true
              }
          }]
      }
  };

  // Get the canvas element for the bar chart
  const barChartCanvas = document.getElementById('barChart');

  // Initialize the bar chart
  new Chart(barChartCanvas, {
      type: 'bar',
      data: barChartData,
      options: barChartOptions
  });

  // Data for the line chart
  const lineChartData = {
      labels: ['January', 'February', 'March', 'April', 'May'],
      datasets: [{
          label: 'Appointment',
          backgroundColor: 'rgba(255, 99, 132, 0.5)',
          borderColor: 'rgba(255, 99, 132, 1)',
          borderWidth: 1,
          data: [7, 8, 12, 15, 18]
      }]
  };

  // Options for the line chart
  const lineChartOptions = {
      scales: {
          yAxes: [{
              ticks: {
                  beginAtZero: true
              }
          }]
      }
  };

  // Get the canvas element for the line chart
  const lineChartCanvas = document.getElementById('lineChart');

  // Initialize the line chart
  new Chart(lineChartCanvas, {
      type: 'line',
      data: lineChartData,
      options: lineChartOptions
  });
});


document.addEventListener('DOMContentLoaded', function() {
    let next = document.querySelector('.next');
    let prev = document.querySelector('.prev');

    next.addEventListener('click', function() {
        let items = document.querySelectorAll('.item');
        document.querySelector('.slide').appendChild(items[0]);
    });

    prev.addEventListener('click', function() {
        let items = document.querySelectorAll('.item');
        document.querySelector('.slide').prepend(items[items.length - 1]);
    });
});

document.addEventListener('DOMContentLoaded', function() {
    const nameInput = document.getElementById('nameInput');
    const emailInput = document.getElementById('emailInput');
    const phoneInput = document.getElementById('phoneInput');
    const updateButton = document.getElementById('updateButton');
    const cancelButton = document.getElementById('cancelButton');
    const editButton = document.getElementById('editButton');

    // Function to toggle edit mode
    function toggleEditMode() {
        nameInput.toggleAttribute('readonly');
        emailInput.toggleAttribute('readonly');
        phoneInput.toggleAttribute('readonly');
    }

    // Edit button click event listener
    updateButton.addEventListener('click', function() {
        toggleEditMode();
    });

    // Update button click event listener
    editButton.addEventListener('click', function() {
        toggleEditMode();

        // Get updated data
        const updatedData = {
            name: nameInput.value,
            email: emailInput.value,
            phone: phoneInput.value
        };

        // Send updated data to Flask route using fetch API
        fetch('/update-profile', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(updatedData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to update profile');
            }
            return response.json();
        })
        .then(data => {
            // Handle response from Flask (if needed)
            console.log('Profile updated successfully');
        })
        .catch(error => {
            console.error('Error updating profile:', error.message);
            // Revert changes or show error message to user
        });
    });

    // Cancel button click event listener
    cancelButton.addEventListener('click', function() {
        toggleEditMode();
        // Reset input values to original data (if needed)
    });
});




