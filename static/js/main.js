var ctx = document.getElementById('myChart').getContext('2d');
var chart = new Chart(ctx, {
    // The type of chart we want to create
    type: 'line',

    // The data for our dataset
    data: {
        labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
        datasets: [{
            data: [1,10,32,6,35,23,12,31,30,14],
	        label: "Africa",
	        borderColor: "#3e95cd",
	        fill: false
	      }, { 
	        data: [1,10,32,6,35,23,12,31,30,14],
	        label: "Asia",
	        borderColor: "#8e5ea2",
	        fill: false
	      }, { 
	        data: [1,10,32,6,35,23,12,31,30,14],
	        label: "Europe",
	        borderColor: "#3cba9f",
	        fill: false
	      }, { 
	        data: [31,10,3,26,25,1,1,33,30,54],
	        label: "Latin America",
	        borderColor: "#e8c3b9",
	        fill: false
	      }, { 
	        data: [14,10,3,6,35,2,16,31,3,14],
	        label: "North America",
	        borderColor: "#c45850",
	        fill: false
	      }
	    ]
	  },

    // Configuration options go here
    options: {}
});
